# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal, pyqtSlot, QAbstractAnimation, QParallelAnimationGroup, QPropertyAnimation, QSize, Qt
from qgis.PyQt.QtWidgets import QFrame, QHBoxLayout, QToolButton, QScrollArea, QSizePolicy, QVBoxLayout, QWidget


class Collapse(QWidget):
    collapsed = pyqtSignal()
    expanded = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.toggleButton = QToolButton(
            text="", checkable=True, checked=False
        )
        self.toggleButton.setStyleSheet("QToolButton { border: none; }")
        self.toggleButton.setToolButtonStyle(
            Qt.ToolButtonTextBesideIcon
        )
        self.toggleButton.setArrowType(Qt.RightArrow)
        self.toggleButton.toggled.connect(self.toggle)
        self.toggleButton.setSizePolicy(
            QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.toggleAnimation = QParallelAnimationGroup(self)

        self.content = QScrollArea(
            maximumHeight=0, minimumHeight=0
        )
        self.content.setSizePolicy(
            QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding
        )
        self.content.setFrameShape(QFrame.NoFrame)

        self.headerLayout = QHBoxLayout()
        self.headerLayout.setSpacing(0)
        self.headerLayout.setContentsMargins(3, 0, 3, 3)
        self.headerLayout.addWidget(self.toggleButton)
        self.headerLayout.addStretch()

        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(self.headerLayout)
        layout.addWidget(self.content)

        self.toggleAnimation.addAnimation(
            QPropertyAnimation(self, b"minimumHeight")
        )
        self.toggleAnimation.addAnimation(
            QPropertyAnimation(self, b"maximumHeight")
        )
        self.toggleAnimation.addAnimation(
            QPropertyAnimation(self.content, b"maximumHeight")
        )

    def addHeaderWidget(self, widget):
        """Add a toolbar to this Collapse."""
        self.headerLayout.addWidget(widget)

    @pyqtSlot()
    def toggle(self):

        checked = self.toggleButton.isChecked()
        self.toggleButton.setArrowType(
            Qt.DownArrow if checked else Qt.RightArrow
        )
        self.toggleAnimation.setDirection(
            QAbstractAnimation.Forward
            if checked
            else QAbstractAnimation.Backward
        )

        self.toggleAnimation.start()
        if checked:
            self.expanded.emit()
        else:
            self.collapsed.emit()

    @pyqtSlot()
    def setExpanded(self, expanded=True):
        checked = self.toggleButton.isChecked()
        if checked != expanded:
            self.toggleButton.toggle()

    def setTitle(self, title):
        self.toggleButton.setText(title)

    def collapsedHeight(self):
        return self.headerLayout.sizeHint().height()

    def contentHeight(self):
        if self.content.layout() is None:
            return 0
        else:
            return self.content.layout().sizeHint().height()

    def sizeHint(self):
        """Return the size of the widget."""
        #defaultSizeHint = super().sizeHint()

        headerWidth = self.headerLayout.sizeHint().width()
        contentWidth = self.content.sizeHint().width()

        width = max(headerWidth, contentWidth)

        height = self.collapsedHeight()
        if self.toggleButton.isChecked():
            height += self.contentHeight()

        hint = QSize(width, height)
        return hint

    def setContentLayout(self, layout):
        currentLayout = self.content.layout()
        del currentLayout
        self.content.setLayout(layout)

        collapsedHeight = self.collapsedHeight()
        contentHeight = self.contentHeight()

        for i in range(self.toggleAnimation.animationCount()):
            animation = self.toggleAnimation.animationAt(i)
            animation.setDuration(50)
            animation.setStartValue(collapsedHeight)
            animation.setEndValue(collapsedHeight + contentHeight)

        contentAnimation = self.toggleAnimation.animationAt(
            self.toggleAnimation.animationCount() - 1
        )
        contentAnimation.setDuration(50)
        contentAnimation.setStartValue(0)
        contentAnimation.setEndValue(contentHeight)
