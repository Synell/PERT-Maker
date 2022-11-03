#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QFrame, QSizePolicy, QLayout
from PySide6.QtCore import Qt, QRect, QSize, QPoint
from .QSmoothScrollArea import QSmoothScrollArea
#----------------------------------------------------------------------

    # Class
class QFlowWidget(QSmoothScrollArea):
    def __init__(self, parent = None, orientation = Qt.Orientation.Horizontal, margin = 0, spacing = -1):
        super(QFlowWidget, self).__init__(parent)
        self.scroll_frame = QFrame()
        self.scroll_frame.setContentsMargins(margin, margin, margin, margin)
        self.scroll_layout = QFlowLayout(self.scroll_frame, orientation, spacing)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setWidget(self.scroll_frame)
        self.setWidgetResizable(True)


class QFlowLayout(QLayout):
    def __init__(self, parent = None, orientation = Qt.Orientation.Horizontal, spacing = -1):
        super().__init__(parent)
        self.orientation = orientation

        self.setContentsMargins(0, 0, 0, 0)

        self.setSpacing(spacing)

        self.item_list = []

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item):
        self.item_list.append(item)

    def count(self):
        return len(self.item_list)

    def itemAt(self, index):
        if index >= 0 and index < len(self.item_list):
            return self.item_list[index]

        return None

    def takeAt(self, index):
        if index >= 0 and index < len(self.item_list):
            return self.item_list.pop(index)

        return None

    def expandingDirections(self):
        return Qt.Orientation(0)

    def hasHeightForWidth(self):
        return self.orientation == Qt.Orientation.Horizontal

    def heightForWidth(self, width):
        return self.doLayout(QRect(0, 0, width, 0), True)

    def hasWidthForHeight(self):
        return self.orientation == Qt.Orientation.Vertical

    def widthForHeight(self, height):
        return self.doLayout(QRect(0, 0, 0, height), True)

    def setGeometry(self, rect):
        super().setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()

        for item in self.item_list:
            size = size.expandedTo(item.minimumSize())

        margin, _, _, _ = self.getContentsMargins()

        size += QSize(2 * margin, 2 * margin)
        return size

    def doLayout(self, rect, testOnly):
        x = rect.x()
        y = rect.y()
        lineHeight = columnWidth = heightForWidth = 0

        for item in self.item_list:
            wid = item.widget()
            spaceX = self.spacing() + wid.style().layoutSpacing(QSizePolicy.ControlType.PushButton, QSizePolicy.ControlType.PushButton, Qt.Orientation.Horizontal)
            spaceY = self.spacing() + wid.style().layoutSpacing(QSizePolicy.ControlType.PushButton, QSizePolicy.ControlType.PushButton, Qt.Orientation.Vertical)
            if self.orientation == Qt.Orientation.Horizontal:
                nextX = x + item.sizeHint().width() + spaceX
                if nextX - spaceX > rect.right() and lineHeight > 0:
                    x = rect.x()
                    y = y + lineHeight + spaceY
                    nextX = x + item.sizeHint().width() + spaceX
                    lineHeight = 0

                if not testOnly:
                    item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

                x = nextX
                lineHeight = max(lineHeight, item.sizeHint().height())
            else:
                nextY = y + item.sizeHint().height() + spaceY
                if nextY - spaceY > rect.bottom() and columnWidth > 0:
                    x = x + columnWidth + spaceX
                    y = rect.y()
                    nextY = y + item.sizeHint().height() + spaceY
                    columnWidth = 0

                heightForWidth += item.sizeHint().height() + spaceY
                if not testOnly:
                    item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

                y = nextY
                columnWidth = max(columnWidth, item.sizeHint().width())

        if self.orientation == Qt.Orientation.Horizontal:
            return y + lineHeight - rect.y()
        else:
            return heightForWidth - rect.y()
#----------------------------------------------------------------------
