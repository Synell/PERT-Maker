#----------------------------------------------------------------------

    # Libraries
import sys, colorsys
from PyQt6.QtCore import QPoint, Qt, pyqtSignal, QSize, QRect, QMetaObject, QCoreApplication
from PyQt6.QtGui import QColor, QMouseEvent
from PyQt6.QtWidgets import QWidget, QSizePolicy, QFrame, QLabel, QFormLayout, QLineEdit, QHBoxLayout, QVBoxLayout, QSpinBox, QDoubleSpinBox, QComboBox
from .QGridFrame import QGridFrame
from .QNamedComboBox import QNamedComboBox
from .QUtilsColor import QUtilsColor
#----------------------------------------------------------------------

    # Class
class QColorPicker(QGridFrame):
    colorChanged = pyqtSignal(QUtilsColor)

    def __init__(self, parent = None, color: QUtilsColor = QUtilsColor(), has_alpha: bool = True) -> None:
        super().__init__(parent)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(10)
        self.__color__ = color
        self._hue_color__ = QUtilsColor.from_hsl(color.hue_hsl, 100.0, 50.0)
        self.__has_alpha__ = has_alpha
        self.__interaction_disabled__ = False

        self.setProperty('QColorPicker', True)
        self.__create_widgets__()
        self.color = color

    def __create_widgets__(self) -> None:
        self.__create_color_view__()
        self.__create_color_slider__()
        self.__create_alpha_slider__()
        self.__create_color_input__()

    def __create_color_view__(self) -> None:
        self.__color_view__ = QFrame()
        self.__color_view__.setMinimumSize(QSize(300, 300))
        self.__color_view__.setMaximumSize(QSize(5000, 5000))
        self.__color_view__.setStyleSheet('background-color: qlineargradient(x1:1, x2:0, stop:0 hsl(0%,100%,50%), stop:1 rgba(255, 255, 255, 255));')
        self.__color_view__.setFrameShape(QFrame.Shape.StyledPanel)
        self.__color_view__.setFrameShadow(QFrame.Shadow.Raised)
        self.__color_view__.setProperty('Rounded', True)

        self.__black_overlay__ = QFrame()
        self.__black_overlay__.setStyleSheet('background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(0, 0, 0, 0), stop:1 rgba(0, 0, 0, 255));')
        self.__black_overlay__.setFrameShape(QFrame.Shape.StyledPanel)
        self.__black_overlay__.setFrameShadow(QFrame.Shadow.Raised)
        self.__black_overlay__.setProperty('Rounded', True)

        self.__selector__ = QFrame(self.__black_overlay__)
        self.__selector__.setGeometry(QRect(-9, -9, 18, 18))
        self.__selector__.setMinimumSize(QSize(18, 18))
        self.__selector__.setMaximumSize(QSize(18, 18))
        self.__selector__.setStyleSheet('background-color:none; border: 3px solid #3F3844; border-radius: 9px;')
        self.__selector__.setFrameShape(QFrame.Shape.StyledPanel)
        self.__selector__.setFrameShadow(QFrame.Shadow.Raised)

        self.__white_ring__ = QLabel(self.__selector__)
        self.__white_ring__.setGeometry(QRect(3, 3, 15, 15))
        self.__white_ring__.setMinimumSize(QSize(12, 12))
        self.__white_ring__.setMaximumSize(QSize(12, 12))
        self.__white_ring__.setBaseSize(QSize(12, 12))
        self.__white_ring__.setStyleSheet('background-color: none; border: 3px solid white; border-radius: 6px;')

        self.grid_layout.addWidget(self.__color_view__, 0, 0)
        self.grid_layout.addWidget(self.__black_overlay__, 0, 0)
        self.grid_layout.addWidget(self.__color_view__, 0, 0)

        self.__black_overlay__.mouseMoveEvent = self.__move_sv_selector__
        self.__black_overlay__.mousePressEvent = self.__move_sv_selector__

    def __create_color_slider__(self) -> None:
        self.__hue_frame__ = QFrame()
        self.__hue_frame__.setProperty('Rounded', True)
        self.__hue_frame__.setMinimumSize(QSize(30, 0))
        self.__hue_frame__.setFrameShape(QFrame.Shape.StyledPanel)
        self.__hue_frame__.setFrameShadow(QFrame.Shadow.Raised)
        self.grid_layout.addWidget(self.__hue_frame__, 0, 1)

        self.__hue_bg__ = QFrame()
        self.__hue_bg__.setGeometry(QRect(0, 0, self.__hue_frame__.minimumWidth(), self.__color_view__.minimumHeight()))
        self.__hue_bg__.setFixedSize(QSize(self.__hue_frame__.minimumWidth(), self.__color_view__.minimumHeight()))
        self.__hue_bg__.setStyleSheet('background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.166 rgba(255, 255, 0, 255), stop:0.333 rgba(0, 255, 0, 255), stop:0.5 rgba(0, 255, 255, 255), stop:0.666 rgba(0, 0, 255, 255), stop:0.833 rgba(255, 0, 255, 255), stop:1 rgba(255, 0, 0, 255));')
        self.__hue_bg__.setProperty('Rounded', True)
        self.__hue_bg__.setProperty('Hue', True)
        self.__hue_bg__.setFrameShape(QFrame.Shape.StyledPanel)
        self.__hue_bg__.setFrameShadow(QFrame.Shadow.Raised)
        self.grid_layout.addWidget(self.__hue_bg__, 0, 1)
        self.grid_layout.setAlignment(self.__hue_bg__, Qt.AlignmentFlag.AlignCenter)

        self.__hue_selector__ = QFrame(self.__hue_bg__)
        self.__hue_selector__.setGeometry(QRect(-3, 0, 36, 9))
        self.__hue_selector__.setFixedSize(QSize(36, 9))
        self.__hue_selector__.setProperty('Rounded', True)
        self.__hue_selector__.setProperty('Hue', True)
        self.__hue_selector__.setStyleSheet('background-color: transparent; border: 3px solid #878787;')

        self.__hue_bg__.mouseMoveEvent = self.__move__hue__selector__
        self.__hue_bg__.mousePressEvent = self.__move__hue__selector__

    def __create_alpha_slider__(self) -> None:
        self.__alpha_frame__ = QFrame()
        self.__alpha_frame__.setProperty('Rounded', True)
        self.__alpha_frame__.setMinimumSize(QSize(30, 0))
        self.__alpha_frame__.setFrameShape(QFrame.Shape.StyledPanel)
        self.__alpha_frame__.setFrameShadow(QFrame.Shadow.Raised)
        self.grid_layout.addWidget(self.__alpha_frame__, 0, 2)

        self.__alpha_bg__ = QFrame()
        self.__alpha_bg__.setGeometry(QRect(0, 0, self.__alpha_frame__.minimumWidth(), self.__color_view__.minimumHeight()))
        self.__alpha_bg__.setFixedSize(QSize(self.__alpha_frame__.minimumWidth(), self.__color_view__.minimumHeight()))
        self.__alpha_bg__.setStyleSheet('background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));')
        self.__alpha_bg__.setProperty('Rounded', True)
        self.__alpha_bg__.setProperty('Hue', True)
        self.__alpha_bg__.setFrameShape(QFrame.Shape.StyledPanel)
        self.__alpha_bg__.setFrameShadow(QFrame.Shadow.Raised)
        self.grid_layout.addWidget(self.__alpha_bg__, 0, 2)
        self.grid_layout.setAlignment(self.__alpha_bg__, Qt.AlignmentFlag.AlignCenter)

        self.__alpha_selector__ = QFrame(self.__alpha_bg__)
        self.__alpha_selector__.setGeometry(QRect(-3, 0, 36, 9))
        self.__alpha_selector__.setFixedSize(QSize(36, 9))
        self.__alpha_selector__.setProperty('Rounded', True)
        self.__alpha_selector__.setProperty('Hue', True)
        self.__alpha_selector__.setStyleSheet('background-color: transparent; border: 3px solid #878787;')

        self.__alpha_bg__.mouseMoveEvent = self.__move_alpha_selector__
        self.__alpha_bg__.mousePressEvent = self.__move_alpha_selector__

    def __create_color_input__(self) -> None:
        frame = QGridFrame()
        frame.setFixedWidth(int(self.__color_view__.minimumWidth() / 2.5))
        frame.setFixedHeight(self.__color_view__.minimumWidth())
        frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        frame.grid_layout.setSpacing(0)
        frame.setProperty('Rounded', True)
        frame.setProperty('ColorInput', True)
        self.grid_layout.addWidget(frame, 0, 3)

        self.__color_vis__ = QFrame()
        self.__color_vis__.setMinimumWidth(self.__color_view__.minimumWidth() // 6)
        self.__color_vis__.setFixedHeight(self.__color_view__.minimumHeight() // 6)
        frame.grid_layout.addWidget(self.__color_vis__, 0, 0)
        self.__color_vis__.setStyleSheet('background-color: #fff;')

        input_frame = QGridFrame()
        input_frame.grid_layout.setContentsMargins(10, 10, 10, 10)
        input_frame.grid_layout.setSpacing(20)
        input_frame.setProperty('Bottom', True)
        frame.grid_layout.addWidget(input_frame, 1, 0)
        input_frame.grid_layout.setRowStretch(3, 1)


        self.__color_combobox__ = QComboBox()
        self.__color_combobox__.setCursor(Qt.CursorShape.PointingHandCursor)
        self.__color_combobox__.view().setCursor(Qt.CursorShape.PointingHandCursor)
        self.__color_combobox__.addItems([
            'RGB',
            'HSV',
            'HSL',
            'CMYK',
            'Hex'
        ])
        input_frame.grid_layout.addWidget(self.__color_combobox__, 0, 0)


        input_frame_top = QGridFrame()
        input_frame_top.grid_layout.setContentsMargins(0, 0, 0, 0)
        input_frame_top.grid_layout.setSpacing(10)
        input_frame.grid_layout.addWidget(input_frame_top, 1, 0)
        input_frame.grid_layout.setAlignment(input_frame_top, Qt.AlignmentFlag.AlignTop)

        input_frame_bottom = QGridFrame()
        input_frame_bottom.grid_layout.setContentsMargins(0, 0, 0, 0)
        input_frame_bottom.grid_layout.setSpacing(5)
        input_frame.grid_layout.addWidget(input_frame_bottom, 2, 0)
        input_frame.grid_layout.setAlignment(input_frame_bottom, Qt.AlignmentFlag.AlignTop)

        label = QLabel('A')
        label.setFixedWidth(20)
        input_frame_bottom.grid_layout.addWidget(label, 0, 0)
        self.__alpha_spinbox__ = QSpinBox()
        self.__alpha_spinbox__.setRange(0, 255)
        # self.__alpha_spinbox__.setValue(self.__color__.alpha)
        input_frame_bottom.grid_layout.addWidget(self.__alpha_spinbox__, 0, 1)


        self.__rgb_frame__ = QGridFrame()
        self.__rgb_frame__.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.__rgb_frame__.grid_layout.setSpacing(5)

        label = QLabel('R')
        label.setFixedWidth(20)
        self.__rgb_frame__.grid_layout.addWidget(label, 0, 0)
        self.__rgb_red_spinbox__ = QSpinBox()
        self.__rgb_red_spinbox__.setRange(0, 255)
        # self.__rgb_red_spinbox__.setValue(self.__color__.red)
        self.__rgb_frame__.grid_layout.addWidget(self.__rgb_red_spinbox__, 0, 1)

        label = QLabel('G')
        label.setFixedWidth(20)
        self.__rgb_frame__.grid_layout.addWidget(label, 1, 0)
        self.__rgb_green_spinbox__ = QSpinBox()
        self.__rgb_green_spinbox__.setRange(0, 255)
        # self.__rgb_green_spinbox__.setValue(self.__color__.green)
        self.__rgb_frame__.grid_layout.addWidget(self.__rgb_green_spinbox__, 1, 1)

        label = QLabel('B')
        label.setFixedWidth(20)
        self.__rgb_frame__.grid_layout.addWidget(label, 2, 0)
        self.__rgb_blue_spinbox__ = QSpinBox()
        self.__rgb_blue_spinbox__.setRange(0, 255)
        # self.__rgb_blue_spinbox__.setValue(self.__color__.blue)
        self.__rgb_frame__.grid_layout.addWidget(self.__rgb_blue_spinbox__, 2, 1)

        self.__rgb_frame__.grid_layout.setRowStretch(3, 1)
        input_frame_top.grid_layout.addWidget(self.__rgb_frame__, 0, 0)


        self.__hsv_frame__ = QGridFrame()
        self.__hsv_frame__.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.__hsv_frame__.grid_layout.setSpacing(5)

        label = QLabel('H')
        label.setFixedWidth(20)
        self.__hsv_frame__.grid_layout.addWidget(label, 0, 0)
        self.__hsv_hue_spinbox__ = QSpinBox()
        self.__hsv_hue_spinbox__.setRange(0, 360)
        # self.__hsv_hue_spinbox__.setValue(int(self.__color__.hue_hsv * 360))
        self.__hsv_frame__.grid_layout.addWidget(self.__hsv_hue_spinbox__, 0, 1)

        label = QLabel('S')
        label.setFixedWidth(20)
        self.__hsv_frame__.grid_layout.addWidget(label, 1, 0)
        self.__hsv_saturation_spinbox__ = QDoubleSpinBox()
        self.__hsv_saturation_spinbox__.setRange(0.0, 100.0)
        # self.__hsv_saturation_spinbox__.setValue(self.__color__.saturation_hsv)
        self.__hsv_frame__.grid_layout.addWidget(self.__hsv_saturation_spinbox__, 1, 1)

        label = QLabel('V')
        label.setFixedWidth(20)
        self.__hsv_frame__.grid_layout.addWidget(label, 2, 0)
        self.__hsv_value_spinbox__ = QDoubleSpinBox()
        self.__hsv_value_spinbox__.setRange(0.0, 100.0)
        # self.__hsv_value_spinbox__.setValue(self.__color__.value_hsv)
        self.__hsv_frame__.grid_layout.addWidget(self.__hsv_value_spinbox__, 2, 1)

        self.__hsv_frame__.grid_layout.setRowStretch(3, 1)
        input_frame_top.grid_layout.addWidget(self.__hsv_frame__, 0, 0)
        self.__hsv_frame__.setVisible(False)


        self.__hsl_frame__ = QGridFrame()
        self.__hsl_frame__.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.__hsl_frame__.grid_layout.setSpacing(5)

        label = QLabel('H')
        label.setFixedWidth(20)
        self.__hsl_frame__.grid_layout.addWidget(label, 0, 0)
        self.__hsl_hue_spinbox__ = QSpinBox()
        self.__hsl_hue_spinbox__.setRange(0, 360)
        # self.__hsl_hue_spinbox__.setValue(int(self.__color__.hue_hsl))
        self.__hsl_frame__.grid_layout.addWidget(self.__hsl_hue_spinbox__, 0, 1)

        label = QLabel('S')
        label.setFixedWidth(20)
        self.__hsl_frame__.grid_layout.addWidget(label, 1, 0)
        self.__hsl_saturation_spinbox__ = QDoubleSpinBox()
        self.__hsl_saturation_spinbox__.setRange(0.0, 100.0)
        # self.__hsl_saturation_spinbox__.setValue(self.__color__.saturation_hsl)
        self.__hsl_frame__.grid_layout.addWidget(self.__hsl_saturation_spinbox__, 1, 1)

        label = QLabel('L')
        label.setFixedWidth(20)
        self.__hsl_frame__.grid_layout.addWidget(label, 2, 0)
        self.__hsl_lightness_spinbox__ = QDoubleSpinBox()
        self.__hsl_lightness_spinbox__.setRange(0.0, 100.0)
        # self.__hsl_lightness_spinbox__.setValue(self.__color__.lightness_hsl)
        self.__hsl_frame__.grid_layout.addWidget(self.__hsl_lightness_spinbox__, 2, 1)

        self.__hsl_frame__.grid_layout.setRowStretch(3, 1)
        input_frame_top.grid_layout.addWidget(self.__hsl_frame__, 0, 0)
        self.__hsl_frame__.setVisible(False)


        self.__cmyk_frame__ = QGridFrame()
        self.__cmyk_frame__.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.__cmyk_frame__.grid_layout.setSpacing(5)

        label = QLabel('C')
        label.setFixedWidth(20)
        self.__cmyk_frame__.grid_layout.addWidget(label, 0, 0)
        self.__cmyk_cyan_spinbox__ = QDoubleSpinBox()
        self.__cmyk_cyan_spinbox__.setRange(0.0, 100.0)
        # self.__cmyk_cyan_spinbox__.setValue(self.__color__.cyan)
        self.__cmyk_frame__.grid_layout.addWidget(self.__cmyk_cyan_spinbox__, 0, 1)

        label = QLabel('M')
        label.setFixedWidth(20)
        self.__cmyk_frame__.grid_layout.addWidget(label, 1, 0)
        self.__cmyk_magenta_spinbox__ = QDoubleSpinBox()
        self.__cmyk_magenta_spinbox__.setRange(0.0, 100.0)
        # self.__cmyk_magenta_spinbox__.setValue(self.__color__.magenta)
        self.__cmyk_frame__.grid_layout.addWidget(self.__cmyk_magenta_spinbox__, 1, 1)

        label = QLabel('Y')
        label.setFixedWidth(20)
        self.__cmyk_frame__.grid_layout.addWidget(label, 2, 0)
        self.__cmyk_yellow_spinbox__ = QDoubleSpinBox()
        self.__cmyk_yellow_spinbox__.setRange(0.0, 100.0)
        # self.__cmyk_yellow_spinbox__.setValue(self.__color__.yellow)
        self.__cmyk_frame__.grid_layout.addWidget(self.__cmyk_yellow_spinbox__, 2, 1)

        label = QLabel('K')
        label.setFixedWidth(20)
        self.__cmyk_frame__.grid_layout.addWidget(label, 3, 0)
        self.__cmyk_key_spinbox__ = QDoubleSpinBox()
        self.__cmyk_key_spinbox__.setRange(0.0, 100.0)
        # self.__cmyk_key_spinbox__.setValue(self.__color__.black)
        self.__cmyk_frame__.grid_layout.addWidget(self.__cmyk_key_spinbox__, 3, 1)

        self.__cmyk_frame__.grid_layout.setRowStretch(4, 1)
        input_frame_top.grid_layout.addWidget(self.__cmyk_frame__, 0, 0)
        self.__cmyk_frame__.setVisible(False)


        self.__hex_frame__ = QGridFrame()
        self.__hex_frame__.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.__hex_frame__.grid_layout.setSpacing(5)

        label = QLabel('#')
        label.setFixedWidth(20)
        self.__hex_frame__.grid_layout.addWidget(label, 0, 0)
        self.__hex_line_edit__ = QLineEdit()
        # self.__hex_line_edit__.setText(self.__color__.hex.replace('#', ''))
        self.__hex_frame__.grid_layout.addWidget(self.__hex_line_edit__, 0, 1)

        self.__hex_frame__.grid_layout.setRowStretch(1, 1)
        input_frame_top.grid_layout.addWidget(self.__hex_frame__, 0, 0)
        self.__hex_frame__.setVisible(False)

        self.__color_combobox__.currentIndexChanged.connect(self.__color_combobox_changed__)

        self.__rgb_red_spinbox__.valueChanged.connect(lambda _: self.__rgb_changed__())
        self.__rgb_green_spinbox__.valueChanged.connect(lambda _: self.__rgb_changed__())
        self.__rgb_blue_spinbox__.valueChanged.connect(lambda _: self.__rgb_changed__())

        self.__hsv_hue_spinbox__.valueChanged.connect(lambda _: self.__hsv_changed__())
        self.__hsv_saturation_spinbox__.valueChanged.connect(lambda _: self.__hsv_changed__())
        self.__hsv_value_spinbox__.valueChanged.connect(lambda _: self.__hsv_changed__())

        self.__hsl_hue_spinbox__.valueChanged.connect(lambda _: self.__hsl_changed__())
        self.__hsl_saturation_spinbox__.valueChanged.connect(lambda _: self.__hsl_changed__())
        self.__hsl_lightness_spinbox__.valueChanged.connect(lambda _: self.__hsl_changed__())

        self.__cmyk_cyan_spinbox__.valueChanged.connect(lambda _: self.__cmyk_changed__())
        self.__cmyk_magenta_spinbox__.valueChanged.connect(lambda _: self.__cmyk_changed__())
        self.__cmyk_yellow_spinbox__.valueChanged.connect(lambda _: self.__cmyk_changed__())
        self.__cmyk_key_spinbox__.valueChanged.connect(lambda _: self.__cmyk_changed__())

        self.__hex_line_edit__.textChanged.connect(lambda _: self.__hex_changed__())

        self.__alpha_spinbox__.valueChanged.connect(lambda _: self.__alpha_changed__())


    def __color_combobox_changed__(self, index: int):
        self.__rgb_frame__.setVisible(index == 0)
        self.__hsv_frame__.setVisible(index == 1)
        self.__hsl_frame__.setVisible(index == 2)
        self.__cmyk_frame__.setVisible(index == 3)
        self.__hex_frame__.setVisible(index == 4)


    def __move_sv_selector__(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            pos = event.position()
            if pos.x() < 0: pos.setX(0)
            if pos.y() < 0: pos.setY(0)
            if pos.x() > self.__color_view__.minimumWidth(): pos.setX(self.__color_view__.minimumWidth())
            if pos.y() > self.__color_view__.minimumHeight(): pos.setY(self.__color_view__.minimumHeight())
            self.__selector__.move(int(pos.x() - 9), int(pos.y() - 9))
            self.__hsv_data_changed__()

    def __move__hue__selector__(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            pos = event.position().y() - 3
            if pos < 0: pos = 0
            if pos > self.__hue_bg__.minimumHeight() - 9: pos = self.__hue_bg__.minimumHeight() - 9
            self.__hue_selector__.move(QPoint(-3, int(pos)))
            self.__hsv_data_changed__()

    def __move_alpha_selector__(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            pos = event.position().y() - 3
            if pos < 0: pos = 0
            if pos > self.__alpha_bg__.minimumHeight() - 9: pos = self.__alpha_bg__.minimumHeight() - 9
            self.__alpha_selector__.move(QPoint(-3, int(pos)))
            self.__alpha_data_changed__()


    def update(self):
        self.__color_vis__.setStyleSheet(f'background-color: qlineargradient(x1:1, x2:0, stop:0 {self.__color__.ahex}, stop:0.35 {self.__color__.ahex}, stop:1 {self.__color__.hex});')
        self.__color_view__.setStyleSheet(f'border-radius: 5px; background-color: qlineargradient(x1:1, x2:0, stop:0 hsl({int(self._hue_color__.hue_hsl)}%,100%,50%), stop:1 #fff);')

    def __changed__(self):
        self.colorChanged.emit(self.__color__)
        self.update()

    def __hsv_data_changed__(self):
        if self.__interaction_disabled__: return
        self.__interaction_disabled__ = True

        h, s, v = 100 - (self.__hue_selector__.y() / (self.__hue_bg__.minimumHeight() - 9) * 100.0), (self.__selector__.x() + 9) / self.__color_view__.minimumWidth() * 100.0, ((self.__color_view__.minimumHeight() - 9) - self.__selector__.y()) / self.__color_view__.minimumHeight() * 100.0
        self.__color__.hsv = (h, s, v)
        self._hue_color__.hue_hsl = h
        self.__changed__()
        self.__set_rgb__()
        self.__set_hsv__()
        self.__set_hsl__()
        self.__set_cmyk__()
        self.__set_hex__()

        self.__interaction_disabled__ = False

    def __set_hsv_data__(self):
        h, s, v = self.__color__.hsv[0], self.__color__.hsv[1], self.__color__.hsv[2]
        self.__hue_selector__.move(QPoint(-3, int((100 - (h if h > 0 else 100)) / 100 * (self.__hue_bg__.minimumHeight() - 9))))
        self.__selector__.move(int((s / 100 * self.__color_view__.minimumWidth()) - 9), int(((100 - v) / 100 * self.__color_view__.minimumHeight()) - 9))
        self._hue_color__.hue_hsl = h


    def __alpha_data_changed__(self):
        if self.__interaction_disabled__: return
        self.__interaction_disabled__ = True

        a = 100 - (self.__alpha_selector__.y() / (self.__alpha_bg__.minimumHeight() - 9) * 100.0)
        self.__color__.alpha = round(a * 2.55)
        self.__changed__()
        self.__set_alpha__()

        self.__interaction_disabled__ = False

    def __set_alpha_data__(self):
        self.__alpha_selector__.move(QPoint(-3, int((self.__alpha_bg__.minimumHeight() - 9) - (self.__alpha_bg__.minimumHeight() - 9) * (self.__color__.alpha / 255.0))))

    def __rgb_changed__(self):
        if self.__interaction_disabled__: return
        self.__interaction_disabled__ = True

        r, g, b = self.__rgb_red_spinbox__.value(), self.__rgb_green_spinbox__.value(), self.__rgb_blue_spinbox__.value()
        self.__color__.rgb = (r, g, b)
        self.__changed__()
        self.__set_hsv_data__()
        self.__set_hsv__()
        self.__set_hsl__()
        self.__set_cmyk__()
        self.__set_hex__()

        self.__interaction_disabled__ = False

    def __set_rgb__(self):
        r, g, b = self.__color__.rgb
        self.__rgb_red_spinbox__.setValue(r)
        self.__rgb_green_spinbox__.setValue(g)
        self.__rgb_blue_spinbox__.setValue(b)

    def __hsv_changed__(self):
        if self.__interaction_disabled__: return
        self.__interaction_disabled__ = True

        h, s, v = self.__hsv_hue_spinbox__.value(), self.__hsv_saturation_spinbox__.value(), self.__hsv_value_spinbox__.value()
        self.__color__.hsv = (h, s, v)
        self.__changed__()
        self.__set_hsv_data__()
        self.__set_rgb__()
        self.__set_hsl__()
        self.__set_cmyk__()
        self.__set_hex__()

        self.__interaction_disabled__ = False

    def __set_hsv__(self):
        h, s, v = self.__color__.hsv
        self.__hsv_hue_spinbox__.setValue(int(h * 3.6))
        self.__hsv_saturation_spinbox__.setValue(s)
        self.__hsv_value_spinbox__.setValue(v)

    def __hsl_changed__(self):
        if self.__interaction_disabled__: return
        self.__interaction_disabled__ = True

        h, s, l = self.__hsl_hue_spinbox__.value(), self.__hsl_saturation_spinbox__.value(), self.__hsl_lightness_spinbox__.value()
        self.__color__.hsl = (h, s, l)
        self.__changed__()
        self.__set_hsv_data__()
        self.__set_rgb__()
        self.__set_hsv__()
        self.__set_cmyk__()
        self.__set_hex__()

        self.__interaction_disabled__ = False

    def __set_hsl__(self):
        h, s, l = self.__color__.hsl
        self.__hsl_hue_spinbox__.setValue(int(h))
        self.__hsl_saturation_spinbox__.setValue(s)
        self.__hsl_lightness_spinbox__.setValue(l)

    def __cmyk_changed__(self):
        if self.__interaction_disabled__: return
        self.__interaction_disabled__ = True

        c, m, y, k = self.__cmyk_cyan_spinbox__.value(), self.__cmyk_magenta_spinbox__.value(), self.__cmyk_yellow_spinbox__.value(), self.__cmyk_black_spinbox__.value()
        self.__color__.cmyk = (c, m, y, k)
        self.__changed__()
        self.__set_hsv_data__()
        self.__set_rgb__()
        self.__set_hsv__()
        self.__set_hsl__()
        self.__set_hex__()

        self.__interaction_disabled__ = False

    def __set_cmyk__(self):
        c, m, y, k = self.__color__.cmyk
        self.__cmyk_cyan_spinbox__.setValue(c)
        self.__cmyk_magenta_spinbox__.setValue(m)
        self.__cmyk_yellow_spinbox__.setValue(y)
        self.__cmyk_key_spinbox__.setValue(k)

    def __hex_changed__(self):
        s = self.__hex_line_edit__.text()
        pos = self.__hex_line_edit__.cursorPosition()
        hex = ''
        for ss in s:
            if ss in '0123456789abcdefABCDEF':
                hex += ss
        if len(hex) < 6: hex = hex + '0' * (6 - len(hex)) #hex.zfill(6)
        if len(hex) > 6: hex = hex[:6]
        s = self.__hex_line_edit__.setText(hex)
        self.__hex_line_edit__.setCursorPosition(pos)

        if self.__interaction_disabled__: return
        self.__interaction_disabled__ = True

        self.__color__.hex = f'#{hex}'
        self.__changed__()
        self.__set_hsv_data__()
        self.__set_rgb__()
        self.__set_hsv__()
        self.__set_hsl__()
        self.__set_cmyk__()

        self.__interaction_disabled__ = False

    def __set_hex__(self):
        hex = self.__color__.hex
        self.__hex_line_edit__.setText(hex.replace('#', ''))

    def __alpha_changed__(self):
        if self.__interaction_disabled__: return
        self.__interaction_disabled__ = True

        a = self.__alpha_spinbox__.value()
        self.__color__.alpha = a
        self.__changed__()
        self.__set_alpha_data__()

        self.__interaction_disabled__ = False

    def __set_alpha__(self):
        self.__alpha_spinbox__.setValue(self.__color__.alpha)

    @property
    def color(self):
        return QUtilsColor.from_rgba(self.__color__.rgba)

    @color.setter
    def color(self, color):
        self.__interaction_disabled__ = True
        self.__color__ = QUtilsColor.from_rgba(color.rgba)
        self.__set_hsv_data__()
        self.__set_rgb__()
        self.__set_hsv__()
        self.__set_hsl__()
        self.__set_cmyk__()
        self.__set_hex__()
        self.__set_alpha__()
        self.__set_alpha_data__()
        self.__changed__()
        self.__interaction_disabled__ = False
#----------------------------------------------------------------------
