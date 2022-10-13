from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QFrame, QScrollArea


class VerticalScrollArea(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWidgetResizable(True)
        self.setFrameStyle(QFrame.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)


@VerticalScrollArea::VerticalScrollArea(QWidget *parent)
: QScrollArea(parent)
{
setWidgetResizable(true);
setFrameStyle(QFrame::NoFrame);
setHorizontalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
setVerticalScrollBarPolicy(Qt::ScrollBarAsNeeded);
m_scrollAreaWidgetContents = new QWidget(this);
m_scrollAreaWidgetContents->setSizePolicy(QSizePolicy::Preferred, QSizePolicy::Preferred);
QVBoxLayout *baseLayout = new QVBoxLayout(m_scrollAreaWidgetContents);
setWidget(m_scrollAreaWidgetContents);
m_scrollAreaWidgetContents->installEventFilter(this);
}

bool VerticalScrollArea::eventFilter(QObject *o, QEvent *e)
{
if(o == m_scrollAreaWidgetContents && e->type() == QEvent::Resize)
setMinimumWidth(m_scrollAreaWidgetContents->minimumSizeHint().width() + verticalScrollBar()->width());

return false;
}@