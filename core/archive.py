"""Elite archive of the best distinct feasible designs (objective minimised)."""
from __future__ import annotations

import heapq
import itertools
from typing import Any, Hashable

from .problem import EvalResult


class EliteArchive:
    def __init__(self, size: int):
        self.size = size
        self._heap: list[tuple[float, int, Hashable, Any, EvalResult]] = []  # max-heap via -obj
        self._keys: set[Hashable] = set()
        self._counter = itertools.count()

    @staticmethod
    def key(design: Any) -> Hashable:
        return tuple(design) if not isinstance(design, Hashable) else design

    def add(self, design: Any, result: EvalResult) -> bool:
        """Insert if feasible, new, and better than the current worst. Returns True if inserted."""
        if not result.feasible:
            return False
        k = self.key(design)
        if k in self._keys:
            return False
        entry = (-result.objective, next(self._counter), k, design, result)
        if len(self._heap) < self.size:
            heapq.heappush(self._heap, entry)
        elif result.objective < -self._heap[0][0]:
            _, _, old_k, _, _ = heapq.heapreplace(self._heap, entry)
            self._keys.discard(old_k)
        else:
            return False
        self._keys.add(k)
        return True

    def best(self, n: int | None = None) -> list[tuple[Any, EvalResult]]:
        ranked = sorted(self._heap, key=lambda e: (-e[0], e[1]))
        return [(e[3], e[4]) for e in ranked[:n]]

    def __len__(self) -> int:
        return len(self._heap)
