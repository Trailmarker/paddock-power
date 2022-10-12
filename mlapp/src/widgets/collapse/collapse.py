# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import pyqtSignal, pyqtSlot, QAbstractAnimation, QParallelAnimationGroup, QPropertyAnimation, QSize, Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QFrame, QHBoxLayout, QToolBar, QToolButton, QScrollArea, QSizePolicy, QVBoxLayout, QWidget

from ...utils import qgsDebug


class Collapse(QWidget):
    collapsed = pyqtSignal()
    expanded = pyqtSignal()

    def __init__(self, parent=None):
        super(Collapse, self).__init__(parent)

        self.toggleButton = QToolButton(
            text="", checkable=True, checked=False
        )
        self.toggleButton.setStyleSheet("QToolButton { border: none; }")
        self.toggleButton.setToolButtonStyle(
            Qt.ToolButtonTextBesideIcon
        )
        self.toggleButton.setArrowType(Qt.RightArrow)
        self.toggleButton.toggled.connect(self.toggle)

        self.toggleAnimation = QParallelAnimationGroup(self)

        self.toolBar = QToolBar()
        self.toolBar.setStyleSheet("QToolBar { padding: 0; }")
        self.toolBar.setFixedHeight(30)
        self.toolBar.setSizePolicy(QSizePolicy(
            QSizePolicy.Minimum, QSizePolicy.Fixed))

        self.content = QScrollArea(
            maximumHeight=0, minimumHeight=0
        )
        self.content.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed
        )
        self.content.setFrameShape(QFrame.NoFrame)

        self.headerLayout = QHBoxLayout()
        self.headerLayout.setSpacing(0)
        self.headerLayout.setContentsMargins(3, 3, 3, 3)
        self.headerLayout.addWidget(self.toggleButton)
        self.headerLayout.addStretch()
        self.headerLayout.addWidget(self.toolBar)

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

    def setTitle(self, title):
        self.toggleButton.setText(title)

    def addToolBarAction(self, action):
        """Add an action to the toolbar."""
        self.toolBar.addAction(action)

    def collapsedHeight(self):
        return self.headerLayout.sizeHint().height()

    def contentHeight(self):
        if self.content.layout() is None:
            return 0
        else:
            return self.content.layout().sizeHint().height()

    def sizeHint(self):
        """Return the size of the widget."""
        defaultSizeHint = super(Collapse, self).sizeHint()

        height = self.collapsedHeight()
        if self.toggleButton.isChecked():
            height += self.contentHeight()

        hint = QSize(defaultSizeHint.width(), height)
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
