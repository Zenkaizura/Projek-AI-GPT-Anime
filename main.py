"""Langkah 1: avatar desktop sederhana tanpa layanan AI."""

import sys

from PySide6.QtCore import QPoint, Qt, Signal
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMenu,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class AvatarWindow(QWidget):
    visibility_changed = Signal(bool)

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Avatar AI")
        self.setFixedSize(260, 330)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._drag_offset: QPoint | None = None

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        # Bayangan dan tubuh.
        painter.setBrush(QColor(35, 28, 75, 65))
        painter.drawEllipse(44, 299, 174, 22)
        painter.setBrush(QColor("#4d3a77"))
        painter.drawRoundedRect(60, 220, 140, 91, 38, 38)
        painter.setBrush(QColor("#f6e9ff"))
        painter.drawRoundedRect(88, 238, 84, 73, 26, 26)

        # Rambut belakang dan telinga kucing.
        painter.setBrush(QColor("#342650"))
        painter.drawEllipse(45, 51, 170, 211)
        left_ear = QPainterPath()
        left_ear.moveTo(65, 105)
        left_ear.lineTo(72, 24)
        left_ear.lineTo(119, 71)
        left_ear.closeSubpath()
        right_ear = QPainterPath()
        right_ear.moveTo(141, 71)
        right_ear.lineTo(188, 24)
        right_ear.lineTo(195, 105)
        right_ear.closeSubpath()
        painter.drawPath(left_ear)
        painter.drawPath(right_ear)
        painter.setBrush(QColor("#ef9cbb"))
        for points in (((76, 80), (79, 42), (102, 73)), ((158, 73), (181, 42), (184, 80))):
            inner = QPainterPath()
            inner.moveTo(*points[0])
            inner.lineTo(*points[1])
            inner.lineTo(*points[2])
            inner.closeSubpath()
            painter.drawPath(inner)

        # Wajah, poni, dan mata.
        painter.setBrush(QColor("#ffe4d7"))
        painter.drawEllipse(66, 78, 128, 149)
        painter.setBrush(QColor("#342650"))
        fringe = QPainterPath()
        fringe.moveTo(62, 133)
        fringe.cubicTo(55, 54, 191, 44, 197, 130)
        fringe.cubicTo(174, 106, 155, 91, 144, 102)
        fringe.cubicTo(124, 125, 96, 119, 62, 133)
        painter.drawPath(fringe)
        painter.setBrush(QColor("#554394"))
        painter.drawEllipse(92, 145, 17, 31)
        painter.drawEllipse(151, 145, 17, 31)
        painter.setBrush(QColor("#ffffff"))
        painter.drawEllipse(97, 150, 6, 9)
        painter.drawEllipse(156, 150, 6, 9)
        painter.setBrush(QColor(244, 123, 155, 90))
        painter.drawEllipse(76, 174, 29, 12)
        painter.drawEllipse(155, 174, 29, 12)
        mouth_pen = QPen(QColor("#9b5472"), 3)
        mouth_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(mouth_pen)
        painter.drawArc(123, 181, 16, 10, 190 * 16, 160 * 16)

        # Pita sederhana di kerah.
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#e47bab"))
        painter.drawEllipse(107, 232, 23, 16)
        painter.drawEllipse(130, 232, 23, 16)
        painter.setBrush(QColor("#a84782"))
        painter.drawEllipse(124, 233, 13, 13)

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_offset = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event) -> None:
        if self._drag_offset is not None and event.buttons() & Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_offset)
            event.accept()

    def mouseReleaseEvent(self, event) -> None:
        self._drag_offset = None
        event.accept()

    def contextMenuEvent(self, event) -> None:
        menu = QMenu(self)
        hide_action = menu.addAction("Sembunyikan avatar")
        quit_action = menu.addAction("Keluar")
        chosen = menu.exec(event.globalPos())
        if chosen == hide_action:
            self.hide()
        elif chosen == quit_action:
            QApplication.instance().quit()

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self.visibility_changed.emit(True)

    def hideEvent(self, event) -> None:
        super().hideEvent(event)
        self.visibility_changed.emit(False)


class ControlWindow(QWidget):
    def __init__(self, avatar: AvatarWindow) -> None:
        super().__init__()
        self.avatar = avatar
        self.setWindowTitle("Kontrol Avatar")
        self.setMinimumWidth(250)

        title = QLabel("Avatar desktop · Langkah 1")
        hint = QLabel("Seret avatar untuk memindahkannya.\nKlik kanan avatar untuk opsi lain.")
        self.toggle_button = QPushButton()
        self.toggle_button.clicked.connect(self.toggle_avatar)
        quit_button = QPushButton("Keluar")
        quit_button.clicked.connect(QApplication.instance().quit)

        buttons = QHBoxLayout()
        buttons.addWidget(self.toggle_button)
        buttons.addWidget(quit_button)
        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(hint)
        layout.addLayout(buttons)

        self.avatar.visibility_changed.connect(self.update_toggle_button)
        self.update_toggle_button(self.avatar.isVisible())

    def toggle_avatar(self) -> None:
        if self.avatar.isVisible():
            self.avatar.hide()
        else:
            self.avatar.show()

    def update_toggle_button(self, visible: bool) -> None:
        self.toggle_button.setText("Sembunyikan" if visible else "Tampilkan")

    def closeEvent(self, event) -> None:
        QApplication.instance().quit()
        event.accept()


def main() -> int:
    app = QApplication(sys.argv)
    avatar = AvatarWindow()
    controls = ControlWindow(avatar)
    controls.show()
    avatar.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
