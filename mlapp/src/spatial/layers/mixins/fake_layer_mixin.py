# -*- coding: utf-8 -*-

class FakeLayerMixin:
    _editing = False

    def isEditable(self):
        return self._editing
    
    def startEditing(self):
        self._editing = True
    
    def commitChanges(self):
        self._editing = False
    
    def rollBack(self):
        self._editing = False

