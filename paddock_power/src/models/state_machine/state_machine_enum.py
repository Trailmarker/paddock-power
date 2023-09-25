# -*- coding: utf-8 -*-
from enum import Enum


class StateMachineEnum(Enum):
    def match(self, *statuses):
        """Return True if a provided StateMachineStatus or string matches this status.
            Note Enum values are tested by identity, so this became necessary."""
        return self.value in [s.value if isinstance(s, StateMachineEnum) else str(s) for s in statuses]

    def __format__(self, _):
        return self.value

    def __str__(self):
        return self.value
