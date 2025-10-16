# core/allocation.py

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Allocation:
    """
    Represents allocation ratios for a single asset.

    Example:
        Allocation(
            name="オルカン",
            ratios={"米国株式": 0.7, "新興国株式": 0.3}
        )
    """
    name: str
    ratios: Dict[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self._validate_and_normalize()

    # --- validation and normalization ---

    def _validate_and_normalize(self) -> None:
        total = sum(self.ratios.values())
        if abs(total - 1.0) < 1e-6:
            return  # 正常
        elif total < 1.0:
            missing = 1.0 - total
            self.ratios["undefined"] = missing
            print(f"[Warning] {self.name}: ratios sum to {total:.2f}, 'undefined' class added with {missing:.2f}")
        else:
            raise ValueError(f"Allocation sum for {self.name} exceeds 1.0 (sum={total:.2f})")

    # --- public API ---

    def to_dict(self) -> Dict[str, float]:
        """Return a shallow copy of the ratios dictionary."""
        return dict(self.ratios)

    def normalize(self) -> Allocation:
        """Return a normalized copy of this allocation."""
        total = sum(self.ratios.values())
        if total == 0:
            raise ValueError(f"Cannot normalize allocation {self.name} with zero total.")
        normalized_ratios = {k: v / total for k, v in self.ratios.items()}
        return Allocation(name=self.name, ratios=normalized_ratios)

    # --- representation ---

    def __repr__(self) -> str:
        ratios_str = ", ".join(f"{k}: {v:.2f}" for k, v in self.ratios.items())
        return f"Allocation(name='{self.name}', ratios={{ {ratios_str} }})"
