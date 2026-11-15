"""

ID filtering for logging.

"""


__all__ = [
    "Filter",
]


class Filter(object):

    def __init__(self) -> None:
        self.allowed_ids: set[int] = set()
        self.denied_ids: set[int] = set()

    def allow_ids(self, ids: set[int]) -> None:
        self.allowed_ids.update(ids)

    def deny_ids(self, ids: set[int]) -> None:
        self.denied_ids.update(ids)

    def filter(self, target_id: int | None) -> bool:
        if target_id is not None:
            if self.allowed_ids and target_id not in self.allowed_ids:
                return True
            if self.denied_ids and target_id in self.denied_ids:
                return True
        return False
