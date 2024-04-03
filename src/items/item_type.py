from __future__ import annotations

from enum import IntEnum, auto

class ItemType(IntEnum):
    DUMMY = auto()
    ACTIVE = auto()
    EFFECT = auto()
    WEAPON = auto()
    DEBUFF = auto()
    MISCEL = auto()

    def typename(t: ItemType):
        return {
            ItemType.ACTIVE: "Active",
            ItemType.EFFECT: "Effect",
            ItemType.WEAPON: "Weapon (unimplemented)",
            ItemType.DEBUFF: "Debuff",
            ItemType.MISCEL: "Misc",
        }[t]
