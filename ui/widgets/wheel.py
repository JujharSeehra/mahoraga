import math

from PySide6.QtCore import (QTimer, Qt,)
from PySide6.QtGui import (QPainter, QPen, QBrush,)
from PySide6.QtWidgets import QWidget
from core.state import MahoragaState


class MahoragaWheel(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.angle = 0
        self.rotation_speed = 2

        self.setMinimumSize(260, 260)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate)
        self.timer.start(30)

    def rotate(self):
        self.angle = (self.angle + self.rotation_speed) % 360
        self.update()

    def set_speed(self, speed):
        self.rotation_speed = speed

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        center = self.rect().center()
        radius = min(self.width(), self.height()) // 2 - 45
        painter.translate(center)
        painter.save()
        painter.rotate(self.angle)

        gold = Qt.darkYellow
        bright_gold = Qt.yellow
        dark_gold = Qt.darkYellow

        outer_pen = QPen(gold)
        outer_pen.setWidth(7)

        painter.setPen(outer_pen)
        painter.setBrush(Qt.NoBrush)

        painter.drawEllipse(-radius,-radius,radius * 2,radius * 2)
        inner_radius = radius - 10

        inner_pen = QPen(dark_gold)
        inner_pen.setWidth(3)
        painter.setPen(inner_pen)
        painter.drawEllipse(-inner_radius,-inner_radius,inner_radius * 2,inner_radius * 2)

        handle_count = 8

        for i in range(handle_count):

            angle = i * 360 / handle_count

            painter.save()

            painter.rotate(angle)
            spoke_pen = QPen(gold)
            spoke_pen.setWidth(6)

            painter.setPen(spoke_pen)

            painter.drawLine(0,0,0,-inner_radius + 2)
            neck_pen = QPen(gold)
            neck_pen.setWidth(7)

            painter.setPen(neck_pen)

            painter.drawLine(0,-radius + 2,0,-radius - 17)
            handle_radius = 13

            painter.setBrush(QBrush(gold))
            painter.setPen( QPen(dark_gold, 3))

            painter.drawEllipse(-handle_radius,-radius - 30,handle_radius * 2,handle_radius * 2)

            highlight_radius = 4

            painter.setBrush(QBrush(bright_gold))

            painter.setPen(Qt.NoPen)

            painter.drawEllipse(-highlight_radius + 4,-radius - 30 + 4,highlight_radius * 2,highlight_radius * 2)

            painter.restore()

        hub_radius = 18
        painter.setBrush(QBrush(gold))

        painter.setPen(QPen(dark_gold, 4))

        painter.drawEllipse(-hub_radius,-hub_radius,hub_radius * 2,hub_radius * 2)

        highlight_radius = 6

        painter.setBrush(QBrush(bright_gold))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(-highlight_radius,-highlight_radius,highlight_radius * 2,highlight_radius * 2)
        inner_hub_radius = 8
        painter.setBrush(QBrush(dark_gold))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(-inner_hub_radius,-inner_hub_radius,inner_hub_radius * 2,inner_hub_radius * 2)
        painter.restore()
        painter.end()
    def set_state(self, state):
        if state == MahoragaState.IDLE:
            self.set_speed(1)
        elif state == MahoragaState.THINKING:
            self.set_speed(5)
        elif state == MahoragaState.USING_TOOL:
            self.set_speed(8)
        elif state == MahoragaState.LEARNING:
            self.set_speed(3)
        elif state == MahoragaState.ERROR:
            self.set_speed(0)
        elif state == MahoragaState.OFFLINE:
            self.set_speed(0)