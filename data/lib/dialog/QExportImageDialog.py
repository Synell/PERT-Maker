#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QDialog, QGridLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QPainter
from data.lib.qtUtils import QColorButton, QFileButton, QFiles, QUtilsColor, QGridWidget, QIconWidget, QScrollableGridFrame
#----------------------------------------------------------------------

    # Class
class QExportImageDialog(QDialog):
    def __init__(self, parent = None, lang: dict = {}, bg_color: QUtilsColor = QUtilsColor('#000000'), fg_color = QUtilsColor('#ffffff'), data: QPixmap = None):
        super().__init__(parent = parent)

        self.lang = lang
        self.data = data

        layout = QGridLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(16, 16, 16, 16)

        self.setWindowTitle(lang['title'])
        self.setFixedWidth(700)
        self.setFixedHeight(500)

        right_buttons = QGridWidget()
        right_buttons.grid_layout.setSpacing(16)
        right_buttons.grid_layout.setContentsMargins(0, 0, 0, 0)

        button = QPushButton(lang['QPushButton']['cancel'])
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(self.reject)
        button.setProperty('color', 'white')
        button.setProperty('transparent', True)
        right_buttons.grid_layout.addWidget(button, 0, 0)

        button = QPushButton(lang['QPushButton']['export'])
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(self.accept)
        button.setProperty('color', 'main')
        right_buttons.grid_layout.addWidget(button, 0, 1)

        left_frame = QGridWidget()
        left_frame.grid_layout.setSpacing(16)
        left_frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.bg_color = QColorButton(None, lang['QColorDialog']['bgColor'], bg_color)
        self.bg_color.color_changed.connect(self.bg_color_changed)
        left_frame.grid_layout.addWidget(QLabel('Background Color'), 0, 0)
        left_frame.grid_layout.addWidget(self.bg_color, 0, 1)
        left_frame.grid_layout.setColumnStretch(2, 1)

        right_frame = QGridWidget()
        right_frame.grid_layout.setSpacing(16)
        right_frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.fg_color = QColorButton(None, lang['QColorDialog']['fgColor'], fg_color)
        self.fg_color.color_changed.connect(self.fg_color_changed)
        right_frame.grid_layout.addWidget(QLabel('Foreground Color'), 0, 0)
        right_frame.grid_layout.addWidget(self.fg_color, 0, 1)
        right_frame.grid_layout.setColumnStretch(2, 1)

        frame = QGridWidget()
        frame.grid_layout.setSpacing(16)
        frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        frame.grid_layout.addWidget(left_frame, 0, 0)
        frame.grid_layout.setAlignment(left_frame, Qt.AlignmentFlag.AlignCenter)
        frame.grid_layout.addWidget(right_frame, 0, 1)
        frame.grid_layout.setAlignment(right_frame, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(frame, 0, 0)

        preview_area = QScrollableGridFrame()
        self.preview = QIconWidget(None, self.data, QSize(self.data.width(), self.data.height()), False)
        preview_area.scroll_layout.addWidget(self.preview, 0, 0)
        layout.addWidget(preview_area, 1, 0)

        self.bg_color_changed(bg_color)
        self.fg_color_changed(fg_color)

        self.filename = QFileButton(
            None,
            lang['QFileButton'],
            './image.svg',
            None,
            QFiles.Dialog.SaveFileName,
            QFiles.Extension.combine(
                QFiles.Extension.Image.SVG,
                QFiles.Extension.Image.PNG,
                QFiles.Extension.Image.JPEG,
                QFiles.Extension.Image.TIFF,
                QFiles.Extension.Image.BMP
            )
        )

        frame = QGridWidget()
        frame.grid_layout.setSpacing(16)
        frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        frame.grid_layout.addWidget(self.filename, 0, 0)
        frame.grid_layout.addWidget(right_buttons, 0, 1)
        layout.addWidget(frame, 2, 0)

        # layout.addWidget(self.bg_color, 0, 0)
        # layout.addWidget(self.fg_color, 0, 1)
        # layout.addWidget(self.preview_area, 1, 0, 1, 2)
        # layout.addWidget(self.filename, 2, 0)
        # layout.addWidget(right_buttons, 2, 1)


    def bg_color_changed(self, color: QUtilsColor) -> None:
        self.color_changed(color, self.fg_color.color)

    def fg_color_changed(self, color: QUtilsColor) -> None:
        self.color_changed(self.bg_color.color, color)

    def color_changed(self, bg_color: QUtilsColor, fg_color: QUtilsColor) -> QPixmap:
        # self.preview.grid_layout.itemAt(0).widget().setStyleSheet(f'background-color: {color.ahex};')
        data = self.data.copy()

        qp = QPainter(data)
        qp.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
        qp.fillRect( data.rect(), fg_color.QColorAlpha )
        qp.end()

        new_data = QPixmap(data.width(), data.height())
        new_data.fill(bg_color.QColorAlpha)
        
        qp = QPainter(new_data)
        qp.drawPixmap(0, 0, data)
        qp.end()

        self.preview.icon = new_data

        return new_data


    def exec(self):
        accept = super().exec()
        if accept:
            format = 'svg' if sum(self.filename.path().endswith(f'.{ext}') for ext in ['svg', 'svgz']) else 'img'
            return {
                'path': self.filename.path(),
                'bg': self.bg_color.color,
                'fg': self.fg_color.color,
                'format': format,
                'data': self.color_changed(self.bg_color.color, self.fg_color.color) if format == 'img' else None
            }
#----------------------------------------------------------------------
