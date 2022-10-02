#----------------------------------------------------------------------

    # Libraries
from PyQt6.QtWidgets import QStackedWidget, QWidget, QGraphicsOpacityEffect
from PyQt6.QtCore import pyqtSignal, QPauseAnimation, QPropertyAnimation, Qt, QEasingCurve, QPoint, QParallelAnimationGroup, QAbstractAnimation

from enum import Enum
from math import fmod
#----------------------------------------------------------------------

    # Class
class QSlidingStackedWidget(QStackedWidget):
    class Direction(Enum):
        Left2Right = 'left2right',
        Right2Left = 'right2left',
        Top2Bottom = 'top2bottom',
        Bottom2Top = 'bottom2top'
        Automatic = 'automatic'

    animation_finished = pyqtSignal()

    def __init__(self, parent = None) -> None:
        super().__init__(parent)

        self._orientation = Qt.Orientation.Horizontal
        self._speed = 300
        self._animation_type = QEasingCurve.Type.OutQuart
        self._now = 0
        self._next = 0
        self._wrap = False
        self._p_now = QPoint(0, 0)
        self._active = False

    def set_orientation(self, orientation: Qt.Orientation) -> None:
        self._orientation = orientation

    def set_speed(self, speed: int) -> None:
        self._speed = speed

    def set_animation(self, animation: QEasingCurve.Type) -> None:
        self._animation_type = animation

    def set_wrap(self, wrap: bool) -> None:
        self._wrap = wrap

    def slide_in_next(self) -> bool:
        now = self.currentIndex()
        if (self._wrap or (now < self.count() - 1)): self.slide_in_idx(now + 1)
        else: return False
        return True

    def slide_in_previous(self) -> bool:
        now = self.currentIndex()
        if (self._wrap or (now > 0)): self.slide_in_idx(now - 1)
        else: return False
        return True

    def slide_in_idx(self, idx: int, direction: Direction) -> None:
        if (idx > self.count() - 1):
            direction = QSlidingStackedWidget.Direction.Top2Bottom if (self._orientation == Qt.Orientation.Vertical) else QSlidingStackedWidget.Direction.Right2Left
            idx = int(fmod((idx), self.count()))
        elif (idx < 0):
            direction = QSlidingStackedWidget.Direction.Bottom2Top if (self._orientation == Qt.Orientation.Vertical) else QSlidingStackedWidget.Direction.Left2Right
            idx = fmod((idx + self.count()), self.count())
        self.slide_in_wgt(self.widget(idx), direction)

    def slide_in_wgt(self, newwidget: QWidget, direction: Direction) -> None:
        if (self._active): return
        else: self._active = True
        directionhint = None
        now = self.currentIndex()
        next = self.indexOf(newwidget)
        if (now == next):
            self._active = False
            return

        elif (now<next):
            directionhint = QSlidingStackedWidget.Direction.Top2Bottom if (self._orientation == Qt.Orientation.Vertical) else QSlidingStackedWidget.Direction.Right2Left

        else:
            directionhint = QSlidingStackedWidget.Direction.Bottom2Top if (self._orientation == Qt.Orientation.Vertical) else QSlidingStackedWidget.Direction.Left2Right

        if (direction == QSlidingStackedWidget.Direction.Automatic):
                direction = directionhint

        offset_x = self.frameRect().width()
        offset_y = self.frameRect().height()


        self.widget(next).setGeometry(0, 0, offset_x, offset_y)
        if (direction == QSlidingStackedWidget.Direction.Bottom2Top):
            offset_x = 0
            offset_y = -offset_y

        elif (direction == QSlidingStackedWidget.Direction.Top2Bottom):
                offset_x = 0

        elif (direction==QSlidingStackedWidget.Direction.Right2Left):
            offset_x = -offset_x
            offset_y = 0

        elif (direction==QSlidingStackedWidget.Direction.Left2Right):
            offset_y = 0

        p_next = self.widget(next).pos()
        p_now = self.widget(now).pos()
        self._p_now = p_now
        self.widget(next).move(p_next.x() - offset_x,p_next.y() - offset_y)

        self.widget(next).show()
        self.widget(next).raise_()

        anim_now = QPropertyAnimation(self.widget(now), 'pos')
        anim_now.setDuration(self._speed)
        anim_now.setEasingCurve(self._animation_type)
        anim_now.setStartValue(QPoint(p_now.x(), p_now.y()))
        anim_now.setEndValue(QPoint(offset_x + p_now.x(), offset_y + p_now.y()))

        anim_now_op_eff = QGraphicsOpacityEffect()
        self.widget(now).setGraphicsEffect(anim_now_op_eff)
        anim_now_op = QPropertyAnimation(anim_now_op_eff, 'opacity')
        anim_now_op.setDuration(self._speed // 2)
        anim_now_op.setStartValue(1)
        anim_now_op.setEndValue(0)

        def finished(effect: QGraphicsOpacityEffect):
            if(effect != None):
                effect.deleteLater()

        anim_now_op.finished.connect(lambda: finished(anim_now_op_eff))

        anim_next_op_eff = QGraphicsOpacityEffect()
        anim_next_op_eff.setOpacity(0)
        self.widget(next).setGraphicsEffect(anim_next_op_eff)
        anim_next_op = QPropertyAnimation(anim_next_op_eff, 'opacity')
        anim_next_op.setDuration(self._speed // 2)
        anim_next_op.setStartValue(0)
        anim_next_op.setEndValue(1)
        anim_next_op.finished.connect(lambda: finished(anim_next_op_eff))

        anim_next = QPropertyAnimation(self.widget(next), 'pos')
        anim_next.setDuration(self._speed)
        anim_next.setEasingCurve(self._animation_type)
        anim_next.setStartValue(QPoint(-offset_x + p_next.x(), offset_y + p_next.y()))
        anim_next.setEndValue(QPoint(p_next.x(), p_next.y()))

        animgroup = QParallelAnimationGroup
        animgroup.addAnimation(anim_now)
        animgroup.addAnimation(anim_next)
        animgroup.addAnimation(anim_now_op)
        animgroup.addAnimation(anim_next_op)

        animgroup.finished.connect(self.animation_done_slot)
        self._next = next
        self._now = now
        self._active = True
        animgroup.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)

    def animation_done_slot(self) -> None:
        self.setCurrentIndex(self._next)
        self.widget(self._now).hide()
        self.widget(self._now).move(self._p_now)
        self._active = False
        self.emit(self.animation_finished())
#----------------------------------------------------------------------
