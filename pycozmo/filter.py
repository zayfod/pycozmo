"""

ID filtering for logging.

"""

from typing import Set


__all__ = [
    "Filter",
]


class Filter(object):

    def __init__(self):
        self.allowed_ids = set()
        self.denied_ids = set()

    def allow_ids(self, ids: Set[int]) -> None:
        self.allowed_ids.update(ids)

    def deny_ids(self, ids: Set[int]) -> None:
        self.denied_ids.update(ids)

    def filter(self, target_id: int) -> bool:
        if target_id is not None:
            if self.allowed_ids and target_id not in self.allowed_ids:
                return True
            if self.denied_ids and target_id in self.denied_ids:
                return True
        return False
