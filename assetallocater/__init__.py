# __init__.py

from typing import Optional



from .core.assets import Assets

from .core.allocations import Allocations

from .core.allocation import Allocation



def load_assets(path: str, date: Optional[str] = None) -> Assets:

    """

    Read Assets from a CSV file.



    Wrapper for Assets.read_csv.

    """

    return Assets.read_csv(path, date=date)


def load_allocations(path: str) -> Allocations:
    """
    Read Allocations from a CSV file.

    Wrapper for Allocations.read_csv.
    """
    return Allocations.read_csv(path)


__all__ = [
    "Assets",
    "Allocations",
    "Allocation",
    "load_assets",
    "load_allocations",
]
