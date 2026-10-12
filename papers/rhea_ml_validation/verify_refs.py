"""Check every entry in refs.bib against Crossref (DOI) or the arXiv API (eprint / arXiv note).

Compares title, year, first-author family name, volume and first page. Prints one line per entry and
exits non-zero if any entry fails. Run: python papers/rhea_ml_validation/verify_refs.py
"""
import json
import re
import sys
import time
import unicodedata
import urllib.request
from difflib import SequenceMatcher
from pathlib import Path

BIB = Path(__file__).with_name("refs.bib")
# Known, documented differences from the registry record (key -> check name to skip).
KNOWN = {"rasmussen2006gaussian": "year"}  # Crossref issued 2005-11-23; print edition and usual citation 2006
UA = {"User-Agent": "aero-opt-research/verify_refs (mailto:daksshinganesh@gmail.com)"}


def norm(s):
    s = re.sub(r"<[^>]+>", " ", s)  # MathML/JATS tags in Crossref titles
    s = unicodedata.normalize("NFKD", s)
    s = re.sub(r"\\['\"`^~=.]\{?(\w)\}?", r"\1", s)  # LaTeX accents
    s = re.sub(r"[{}$\\]", "", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def parse(text):
    out = []
    for m in re.finditer(r"@(\w+)\{([^,]+),(.*?)\n\}", text, re.S):
        fields = dict((k.lower(), v.strip()) for k, v in re.findall(r"(\w+)\s*=\s*\{(.*?)\}\s*,?\s*$", m.group(3), re.M | re.S))
        out.append((m.group(2), m.group(1).lower(), fields))
    return out


def get(url):
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                return r.read().decode()
        except Exception:
            time.sleep(2 ** (attempt + 1))
    return None


def first_family(author_field):
    a = author_field.split(" and ")[0]
    return norm(a.split(",")[0] if "," in a else a.split()[-1])


def check_crossref(f):
    raw = get("https://api.crossref.org/works/" + f["doi"])
    if raw is None:
        return ["crossref unreachable"]
    m = json.loads(raw)["message"]
    probs = []
    title = (m.get("title") or [""])[0]
    if SequenceMatcher(None, norm(title), norm(f.get("title", ""))).ratio() < 0.85:
        probs.append(f"title: crossref '{title}'")
    years = {str(m.get(k, {}).get("date-parts", [[None]])[0][0]) for k in ("published-print", "published-online", "issued")}
    if f.get("year") not in years:
        probs.append(f"year: crossref {sorted(y for y in years if y != 'None')}")
    auth = m.get("author") or []
    if auth and "author" in f and norm(auth[0].get("family", "")) != first_family(f["author"]):
        probs.append(f"first author: crossref {auth[0].get('family')}")
    if "volume" in f and m.get("volume") and m["volume"] != f["volume"]:
        probs.append(f"volume: crossref {m['volume']}")
    page = m.get("page") or m.get("article-number")
    if "pages" in f and page and norm(page.split("-")[0]) != norm(f["pages"].split("-")[0]):
        probs.append(f"pages: crossref {page}")
    return probs


def check_arxiv(f, aid):
    raw = get("https://export.arxiv.org/api/query?id_list=" + aid)
    if raw is None:
        return ["arxiv unreachable"]
    t = re.search(r"<entry>.*?<title>(.*?)</title>", raw, re.S)
    if not t:
        return [f"arxiv id {aid} not found"]
    if SequenceMatcher(None, norm(t.group(1)), norm(f.get("title", ""))).ratio() < 0.85:
        return [f"title: arxiv '{' '.join(t.group(1).split())}'"]
    return []


def main():
    bad = 0
    for key, kind, f in parse(BIB.read_text()):
        aid = f.get("eprint") or (re.search(r"arXiv:(\d{4}\.\d{4,5})", f.get("note", "")) or [None, None])[1]
        if "doi" in f and not f["doi"].startswith("10.5281/zenodo"):
            probs, src = check_crossref(f), "crossref"
        elif aid:
            probs, src = check_arxiv(f, aid), "arxiv"
        else:
            probs, src = [], "not checked (book/software; check manually)"
        probs = [p for p in probs if not p.startswith(KNOWN.get(key, "\0"))]
        bad += bool(probs)
        print(f"{'FAIL' if probs else 'ok  '} {key:32s} {src}" + ("".join(f"\n       {p}" for p in probs)))
        time.sleep(0.2)
    print(f"\n{bad} entries with problems")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
