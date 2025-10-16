from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, DefaultDict
import csv
from collections import defaultdict

from .allocation import Allocation
from .assets import Assets


@dataclass
class Allocations:
    """
    Represents a collection of Allocation objects.

    Example:
        allocations = Allocations([
            Allocation(name="オルカン", ratios={"米国株式": 0.7, "新興国株式": 0.3}),
            Allocation(name="S&P500", ratios={"米国株式": 1.0}),
        ])
    """
    items: List[Allocation] = field(default_factory=list)

    # --- CSV Input/Output ---
    @classmethod
    def read_csv(cls, path: str) -> Allocations:
        """Read Allocations from a CSV file"""
        ratios_by_name: DefaultDict[str, Dict[str, float]] = defaultdict(dict)
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row["name"].strip()
                asset_class = row["class"].strip()
                ratio = float(row["ratio"])
                ratios_by_name[name][asset_class] = ratio

        allocations = [
            Allocation(name=name, ratios=ratios) for name, ratios in ratios_by_name.items()
        ]
        return cls(items=allocations)

    # --- Basic Operations ---

    def add(self, allocation: Allocation) -> None:
        """Adds an Allocation object to the collection."""
        self.items.append(allocation)

    def names(self) -> List[str]:
        """Returns a list of all Allocation names in the collection."""
        return [a.name for a in self.items]

    def to_dict(self) -> Dict[str, Dict[str, float]]:
        """Returns a dictionary mapping Allocation names to their ratios."""
        return {a.name: a.ratios for a in self.items}

    # --- Multiplication (Allocations x Assets) ---

    def __mul__(self, assets: Assets) -> Assets:
        """
        Combine allocations with asset values to compute the weighted class composition.

        Returns:
            Assets: A new Assets object with aggregated principal and value by class.
        """
        values_by_class: Dict[str, float] = {}
        principals_by_class: Dict[str, float] = {}
        principals = assets.principals
        has_principals = principals is not None

        for allocation in self.items:
            if allocation.name not in assets.values:
                print(f"[Warning] Asset '{allocation.name}' not found in assets; skipped.")
                continue

            asset_value = assets.values[allocation.name]

            asset_principal = 0.0
            if has_principals:
                asset_principal = principals.get(allocation.name, 0.0)

            for cls, ratio in allocation.ratios.items():
                values_by_class[cls] = values_by_class.get(cls, 0.0) + asset_value * ratio
                if has_principals:
                    principals_by_class[cls] = principals_by_class.get(cls, 0.0) + asset_principal * ratio

        return Assets(
            values=values_by_class,
            principals=principals_by_class if has_principals else None,
        )

    # --- String Representation ---

    def __repr__(self) -> str:
        return f"Allocations({len(self.items)} items)"


