#----------------------------------------------------------------------

    # Libraries
from sys import argv
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtCore import QPauseAnimation, QRect, QEvent, QSequentialAnimationGroup, QPauseAnimation, QPropertyAnimation, Qt, QEasingCurve
from PyQt6.QtGui import QIcon, QPixmap
#----------------------------------------------------------------------

    # Class
class QBaseApplication(QApplication):
    def __init__(self) -> None:
        super().__init__(argv)
        self.window = QMainWindow()
        self.window.setWindowTitle('Base Qt Window')

        self._alerts = []
        self._has_installed_event_filter = False

    def show_alert(self, message: str, icon: QIcon|QPixmap = None, raise_duration: int = 350, pause_duration: int = 1300, fade_duration: int = 350, color: str = 'main') -> None:
        if not self._has_installed_event_filter:
            self.window.centralWidget().installEventFilter(self)
            self._has_installed_event_filter = True

        alert = QLabel(message, self.window.centralWidget(), alignment = Qt.AlignmentFlag.AlignCenter)
        if icon: alert.setPixmap(icon.pixmap(16, 16) if isinstance(icon, QIcon) else icon)
        alert.setProperty('QAlert', True)
        alert.setProperty('color', color)
        alert.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        alert.animation = QSequentialAnimationGroup(alert)
        alert.animation.addAnimation(QPropertyAnimation(alert, b'geometry', duration = raise_duration, easingCurve = QEasingCurve.Type.OutCubic))
        alert.animation.addAnimation(QPauseAnimation(pause_duration))
        alert.animation.addAnimation(QPropertyAnimation(alert, b'geometry', duration = fade_duration, easingCurve = QEasingCurve.Type.InCubic))
        self._alerts.append(alert)

        def deleteLater() -> None:
            self._alerts.remove(alert)
            alert.deleteLater()
        alert.animation.finished.connect(deleteLater)

        self._update_alert_animations()

        alert.setGeometry(alert.animation.animationAt(0).startValue())
        alert.show()
        alert.raise_()
        alert.animation.start()

    def _update_alert_animations(self) -> None:
        width = self.window.centralWidget().width() - 20
        y = self.window.centralWidget().height() - 10
        margin = self.window.fontMetrics().height()
        for alert in self._alerts:
            height = alert.heightForWidth(width) + margin
            startRect = QRect(10, y, width, height)
            endRect = startRect.translated(0, -height)
            alert.animation.animationAt(0).setStartValue(startRect)
            alert.animation.animationAt(0).setEndValue(endRect)
            alert.animation.animationAt(2).setStartValue(endRect)
            alert.animation.animationAt(2).setEndValue(startRect)

    def eventFilter(self, obj: QLabel, event: QEvent) -> bool:
        try:
            if obj == self.window.centralWidget() and event.type() == event.Type.Resize and self._alerts:
                self._update_alert_animations()
                for alert in self._alerts:
                    anim = alert.animation
                    if isinstance(anim.currentAnimation(), QPauseAnimation):
                        alert.setGeometry(anim.animationAt(0).endValue())

        except: pass

        return super().eventFilter(obj, event)
#----------------------------------------------------------------------
