# core/assets.py

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Optional, List
import csv


@dataclass
class Assets:
    """
    Represents a collection of asset values.
    Each asset has a name and its current value (and optionally a principal).

    Example:
        assets = Assets({"オルカン": 100, "S&P500": 50})
    """
    values: Dict[str, float] = field(default_factory=dict)
    principals: Optional[Dict[str, float]] = None
    date: Optional[str] = None

    # --- Initialization and Basic Operations ---

    def __getitem__(self, name: str) -> float:
        return self.values.get(name, 0.0)

    def __setitem__(self, name: str, value: float) -> None:
        self.values[name] = value

    def names(self) -> List[str]:
        return list(self.values.keys())

    def total_value(self) -> float:
        """Returns the total value of all assets."""
        return sum(self.values.values())

    # --- CSV Input/Output ---

    def to_csv(self, path: str) -> None:
        """Export Assets to CSV"""
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["name", "principal", "value"])
            for name, value in self.values.items():
                principal = (
                    self.principals.get(name, "") if self.principals is not None else ""
                )
                writer.writerow([name, principal, value])

    @classmethod
    def read_csv(cls, path: str, date: Optional[str] = None) -> Assets:
        """Read Assets from a CSV file"""
        values: Dict[str, float] = {}
        principals: Dict[str, float] = {}

        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row["name"].strip()
                value = float(row.get("value") or 0)
                principal_raw = row.get("principal")
                if principal_raw not in (None, "", "None"):
                    principals[name] = float(principal_raw)
                values[name] = value

        return cls(values=values, principals=principals or None, date=date)

    # --- Calculation Helpers ---

    def merge(self, other: Assets) -> Assets:
        """Combine two Assets objects"""
        merged: Dict[str, float] = self.values.copy()
        for k, v in other.values.items():
            merged[k] = merged.get(k, 0.0) + v
        return Assets(values=merged)

    # --- String Representation ---

    def __repr__(self) -> str:
        total = self.total_value()
        return f"Assets({len(self.values)} items, total={total:.2f})"
