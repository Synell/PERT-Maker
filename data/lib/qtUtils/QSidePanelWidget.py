#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QWidget, QGridLayout
from PySide6.QtCore import Qt, Signal
from .QSidePanel import QSidePanel, QSidePanelItem
from .QSlidingStackedWidget import QSlidingStackedWidget
from .QGridWidget import QGridWidget
#----------------------------------------------------------------------

    # Class
class QSidePanelWidget(QWidget):
    current_index_changed = Signal(int)

    def __init__(self, parent = None, width: int = 120) -> None:
        super().__init__(parent)
        self._layout = QGridLayout(self)

        self.sidepanel = QSidePanel(self, width = width)
        self.sidepanel.setProperty('border-right', True)

        w = QGridWidget()
        w.grid_layout.setSpacing(0)
        w.grid_layout.setContentsMargins(16, 16, 16, 16)

        self._widget = QSlidingStackedWidget()
        self._widget.set_orientation(Qt.Orientation.Vertical)
        w.grid_layout.addWidget(self._widget, 0, 0)

        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._layout.addWidget(self.sidepanel, 0, 0)
        self._layout.addWidget(w, 0, 1)

    def add_widget(self, widget: QWidget, title: str, icon: str = None) -> None:
        self._widget.addWidget(widget)
        i = self._widget.count() - 1
        self.sidepanel.add_item(QSidePanelItem(title, icon, lambda: self.set_current_index(i)))

    def current_index(self) -> int:
        return self._widget.currentIndex()

    def set_current_index(self, index: int) -> None:
        self._widget.slide_in_idx(index)
        self.sidepanel.set_current_index(index)
#----------------------------------------------------------------------
