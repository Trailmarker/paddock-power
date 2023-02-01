# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

class Feature(ABC):

    @abstractmethod
    def delete(self):
        """Delete the Persisted item."""
        pass

    @abstractmethod
    def recalculate(self):
        """Recalculate everything that can be recalculated about this item."""
        pass

    @abstractmethod
    def upsert(self):
        """Add or update this Persisted item."""
        pass

  