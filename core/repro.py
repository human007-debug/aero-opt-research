"""Reproducibility helpers: seeding and environment capture."""
from __future__ import annotations

import platform
import random
import subprocess
import sys
from importlib import metadata

import numpy as np

TRACKED_PACKAGES = ["numpy", "scipy", "pyyaml", "pymoo", "torch", "botorch", "anthropic"]


def seed_everything(seed: int) -> np.random.Generator:
    random.seed(seed)
    np.random.seed(seed)
    try:
        import torch

        torch.manual_seed(seed)
    except ImportError:
        pass
    return np.random.default_rng(seed)


def git_commit() -> str | None:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True
        )
        dirty = subprocess.run(
            ["git", "status", "--porcelain"], capture_output=True, text=True, check=True
        ).stdout.strip()
        return out.stdout.strip() + ("-dirty" if dirty else "")
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def environment_info() -> dict:
    versions = {}
    for pkg in TRACKED_PACKAGES:
        try:
            versions[pkg] = metadata.version(pkg)
        except metadata.PackageNotFoundError:
            pass
    return {
        "python": sys.version,
        "platform": platform.platform(),
        "packages": versions,
        "git_commit": git_commit(),
    }
