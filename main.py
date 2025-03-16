import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit,
    QPushButton, QMessageBox, QDesktopWidget, QCheckBox
)
from PyQt5.QtCore import QTimer, Qt, pyqtSignal
from PyQt5.QtGui import QCursor

class CountdownApp(QMainWindow):
    def __init__(self):
        super().__init__()
        screen_geometry = QDesktopWidget().screenGeometry()
        self.setGeometry(screen_geometry)
        center_x = int(screen_geometry.width() // 2)
        center_y = int(screen_geometry.height() // 2)
        x_window = 600
        y_window = 400
        self.setWindowTitle("RestReminder")
        self.setGeometry(center_x - int(x_window // 2), int(center_y - y_window // 2), x_window, y_window)
        # Запрещаем изменение размера окна
        self.setFixedSize(x_window, y_window)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        # Основной виджет и layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setStyleSheet("background-color: rgb(20,20,20);border-radius: 20px;")
        self.central_widget.setFont(font)

        # Glow effect label
        self.label_restreminder_glow = QtWidgets.QLabel(self.central_widget)
        self.label_restreminder_glow.setGeometry(QtCore.QRect(40, 35, 300, 30))
        self.label_restreminder_glow.setText("⏰ RestReminder")
        self.label_restreminder_glow.setStyleSheet("background-color: rgba(0,0,0,0);color: rgba(255,255,255,50);font-size: 24px;")
        self.label_restreminder_glow.setFont(font)
        self.label_restreminder_glow_effect = QtWidgets.QGraphicsBlurEffect()
        self.label_restreminder_glow_effect.setBlurRadius(3)
        self.label_restreminder_glow.setGraphicsEffect(self.label_restreminder_glow_effect)

        # Main label
        self.label_restreminder = QtWidgets.QLabel(self.central_widget)
        self.label_restreminder.setGeometry(QtCore.QRect(40, 35, 300, 30))
        self.label_restreminder.setText("⏰ RestReminder")
        self.label_restreminder.setStyleSheet("background-color: rgba(0,0,0,0);color: white;font-size: 24px;")
        self.label_restreminder.setFont(font)

        # Exit button
        self.button_exit = QtWidgets.QPushButton(self.central_widget)
        self.button_exit.setGeometry(QtCore.QRect(530, 35, 30, 30))
        self.button_exit.setText("×")
        self.button_exit.setObjectName("button_exit")
        self.button_exit.clicked.connect(self.close)
        self.button_exit.setCursor(QtCore.Qt.PointingHandCursor)
        self.button_exit.setStyleSheet("QPushButton {"
                                       "    background-color: rgba(0,0,0,0);"
                                       "    color: rgb(153,154,156);"
                                       "    font-size: 28px;"
                                       "}"
                                       "QPushButton:hover {"
                                       "    background-color: rgba(0,0,0,0);"
                                       "    color: rgb(123,124,126);"
                                       "}")

        # Minimize button
        self.button_fullscreen = QtWidgets.QPushButton(self.central_widget)
        self.button_fullscreen.setGeometry(QtCore.QRect(490, 37.5, 30, 30))
        self.button_fullscreen.setText("-")
        self.button_fullscreen.setObjectName("button_fullscreen")
        self.button_fullscreen.clicked.connect(self.showMinimized)
        self.button_fullscreen.setCursor(QtCore.Qt.PointingHandCursor)
        self.button_fullscreen.setStyleSheet("QPushButton {"
                                             "    background-color: rgba(0,0,0,0);"
                                             "    color: rgb(153,154,156);"
                                             "    font-size: 28px;"
                                             "}"
                                             "QPushButton:hover {"
                                             "    background-color: rgba(0,0,0,0);"
                                             "    color: rgb(123,124,126);"
                                             "}")

        # Timer input field
        self.label_timer = QtWidgets.QLabel(self.central_widget)
        self.label_timer.setGeometry(QtCore.QRect(40, 85, 300, 20))
        self.label_timer.setText("Введите время таймера (час. мин. сек.):")
        self.label_timer.setStyleSheet("background-color: rgba(0,0,0,0);color: rgb(200,200,200);font-size: 16px;")
        self.label_timer.setFont(font)

        self.time_input = QtWidgets.QLineEdit(self.central_widget)
        self.time_input.setGeometry(QtCore.QRect(40, 120, 300, 30))
        self.time_input.setPlaceholderText("Пример: 1 30 0 (1 час 30 минут 0 секунд)")
        self.time_input.setStyleSheet("background-color: rgb(15,15,15);color: rgb(100,100,100);font-size: 14px;border-radius: 15px;padding-left: 14px;padding-right: 14px;")
        self.time_input.setFont(font)
        self.time_input.textChanged.connect(self.on_changes)

        # Close time input field
        self.label_close_time = QtWidgets.QLabel(self.central_widget)
        self.label_close_time.setGeometry(QtCore.QRect(40, 165, 475, 20))
        self.label_close_time.setText("Введите время закрытия окна 'Время вышло' (час. мин. сек.):")
        self.label_close_time.setStyleSheet("background-color: rgba(0,0,0,0);color: rgb(200,200,200);font-size: 16px;")
        self.label_close_time.setFont(font)

        self.close_time_input = QtWidgets.QLineEdit(self.central_widget)
        self.close_time_input.setGeometry(QtCore.QRect(40, 200, 300, 30))
        self.close_time_input.setPlaceholderText("Пример: 0 5 0 (5 минут 0 секунд)")
        self.close_time_input.setStyleSheet("background-color: rgb(15,15,15);color: rgb(100,100,100);font-size: 14px;border-radius: 15px;padding-left: 14px;padding-right: 14px;")
        self.close_time_input.setFont(font)
        self.close_time_input.textChanged.connect(self.on_changes)

        # Remaining time label
        self.timer_label = QtWidgets.QLabel(self.central_widget)
        self.timer_label.setGeometry(QtCore.QRect(40, 240, 300, 20))
        self.timer_label.setText("Осталось времени: --:--:--")
        self.timer_label.setStyleSheet("background-color: rgba(0,0,0,0);color: white;font-size: 16px;")
        self.timer_label.setFont(font)

        # Loop checkbox
        self.loop_checkbox = QtWidgets.QCheckBox(self.central_widget)
        self.loop_checkbox.setText("Зациклить процесс")
        self.loop_checkbox.setGeometry(40, 270, 210, 25)
        self.loop_checkbox.setFont(font)
        self.loop_checkbox.stateChanged.connect(self.on_changes)
        self.loop_checkbox.setStyleSheet("""
            QCheckBox {
                spacing: 10px;
                color: rgb(200,200,200);
                font-size: 16px;
            }
            QCheckBox::indicator {
                width: 10px;
                height: 10px;
                border: 2px solid white;
                border-radius: 5px;  /* Закругленные углы */
            }
            QCheckBox::indicator:checked {
                background-color: rgb(255,255,255);  /* Цвет при выборе */
                spacing: 5px;
            }
        """)

        # Start button
        self.start_button_glow = QtWidgets.QPushButton(self.central_widget)
        self.start_button_glow.setGeometry(QtCore.QRect(40, 320, 300, 50))
        self.start_button_glow.setStyleSheet("background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgba(17,100,180,100), stop:1 rgba(12,85,165,100));border-radius: 25px;color: white;font-size: 18px;")
        self.start_button_glow_effect = QtWidgets.QGraphicsBlurEffect()
        self.start_button_glow_effect.setBlurRadius(15)
        self.start_button_glow.setGraphicsEffect(self.start_button_glow_effect)

        self.start_button = QtWidgets.QPushButton(self.central_widget)
        self.start_button.setGeometry(QtCore.QRect(40, 320, 300, 50))
        self.start_button.setText("Начать отсчёт")
        self.start_button.clicked.connect(self.start_countdown)
        self.start_button.setStyleSheet("QPushButton {background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgb(17,100,180), stop:1 rgb(12,85,165));border-radius: 25px;color: white;font-size: 18px;} QPushButton:hover {background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgb(10,90,170), stop:1 rgb(10,80,155));border-radius: 25px;color: white;font-size: 18px;}")
        self.start_button.setIconSize(QtCore.QSize(24, 24))
        self.start_button.setCursor(QtCore.Qt.PointingHandCursor)
        self.start_button.setFont(font)

        # Pause/Resume button
        self.pause_resume_button_glow = QtWidgets.QPushButton(self.central_widget)
        self.pause_resume_button_glow.setGeometry(QtCore.QRect(360, 320, 200, 50))
        self.pause_resume_button_glow.setStyleSheet("background-color: rgba(45,45,45,100);border-radius: 25px;color: white;font-size: 18px;")
        self.pause_resume_button_glow_effect = QtWidgets.QGraphicsBlurEffect()
        self.pause_resume_button_glow_effect.setBlurRadius(15)
        self.pause_resume_button_glow.setGraphicsEffect(self.pause_resume_button_glow_effect)

        self.pause_resume_button = QtWidgets.QPushButton(self.central_widget)
        self.pause_resume_button.setGeometry(QtCore.QRect(360, 320, 200, 50))
        self.pause_resume_button.setText("Приостановить")
        self.pause_resume_button.clicked.connect(self.toggle_pause_resume)
        self.pause_resume_button.setStyleSheet("QPushButton {background-color: rgb(45,45,45);border-radius: 25px;color: white;font-size: 18px;} QPushButton:hover {background-color: rgb(71,74,81);border-radius: 25px;color: white;font-size: 18px;}")
        self.pause_resume_button.setIconSize(QtCore.QSize(24, 24))
        self.pause_resume_button.setCursor(QtCore.Qt.PointingHandCursor)
        self.pause_resume_button.setFont(font)
        self.pause_resume_button.setEnabled(False)

        # Timers
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.close_timer = QTimer()
        self.remaining_time = 0
        self.is_looping = False
        self.is_paused = False

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.central_widget.mousePressEvent = self.mousePressEvent
        self.central_widget.mouseMoveEvent = self.mouseMoveEvent
        self.central_widget.mouseReleaseEvent = self.mouseReleaseEvent

    def on_changes(self):
        self.start_button_glow.setStyleSheet("background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgba(17,100,180,100), stop:1 rgba(12,85,165,100));border-radius: 25px;color: white;font-size: 18px;")
        self.start_button.setText("Начать отсчёт")
        self.start_button.setStyleSheet("QPushButton {background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgb(17,100,180), stop:1 rgb(12,85,165));border-radius: 25px;color: white;font-size: 18px;} QPushButton:hover {background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgb(10,90,170), stop:1 rgb(10,80,155));border-radius: 25px;color: white;font-size: 18px;}")
        self.pause_resume_button_glow.setStyleSheet("background-color: rgba(45,45,45,100);border-radius: 25px;color: white;font-size: 18px;")
        self.pause_resume_button.setText("Приостановить")
        self.pause_resume_button.setStyleSheet("QPushButton {background-color: rgb(45,45,45);border-radius: 25px;color: white;font-size: 18px;} QPushButton:hover {background-color: rgb(71,74,81);border-radius: 25px;color: white;font-size: 18px;}")
        self.pause_resume_button.setEnabled(False)

    def parse_time_input(self, input_text):
        try:
            parts = input_text.split()
            if len(parts) != 3:
                raise ValueError("Введите три числа через пробел: часы минуты секунды.")
            hours, minutes, seconds = map(int, parts)
            if not (0 <= hours <= 24 and 0 <= minutes <= 59 and 0 <= seconds <= 59):
                raise ValueError("Неверный формат времени. Введите значения в диапазоне: часы (0-24), минуты (0-59), секунды (5-59).")
            if (hours == 0 and minutes == 0 and seconds == 0) or (hours == 0 and minutes == 0 and seconds == 1) or (hours == 0 and minutes == 0 and seconds == 2) or (hours == 0 and minutes == 0 and seconds == 3) or (hours == 0 and minutes == 0 and seconds == 4):
                raise ValueError(f"Время не может быть равно 00:00:0{seconds}\nОграничение: минимум 5 секунд")
            return hours, minutes, seconds
        except ValueError as e:
            raise ValueError(str(e))

    def validate_time_input(self, input_text):
        if not input_text.strip():
            raise ValueError("Необходимо ввести все значения: часы, минуты и секунды.")

    def start_countdown(self):
        try:
            # Validate close time input
            time_input_text = self.close_time_input.text().strip()
            self.validate_time_input(time_input_text)
            hours, minutes, seconds = self.parse_time_input(time_input_text)
            total_seconds = hours * 3600 + minutes * 60 + seconds
            if total_seconds <= 0:
                raise ValueError("Время должно быть положительным числом.")

            # Validate main timer input
            time_input_text = self.time_input.text().strip()
            self.validate_time_input(time_input_text)
            hours, minutes, seconds = self.parse_time_input(time_input_text)
            total_seconds = hours * 3600 + minutes * 60 + seconds
            if total_seconds <= 0:
                raise ValueError("Время должно быть положительным числом.")

            self.time_input.setEnabled(False)
            self.close_time_input.setEnabled(False)
            self.remaining_time = total_seconds
            self.is_looping = self.loop_checkbox.isChecked()
            self.update_timer_label()
            self.timer.start(1000)
            self.start_button.setStyleSheet("QPushButton {background-color: rgb(45,45,45);border-radius: 25px;color: white;font-size: 18px;} QPushButton:hover {background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgb(10,90,170), stop:1 rgb(10,80,155));border-radius: 25px;color: white;font-size: 18px;}")
            self.start_button_glow.setStyleSheet("background-color: rgba(45,45,45,100);border-radius: 25px;color: white;font-size: 18px;")
            self.start_button.setEnabled(False)
            self.loop_checkbox.setEnabled(False)
            self.pause_resume_button.setEnabled(True)
            self.pause_resume_button.setText("Приостановить")
            self.pause_resume_button.setStyleSheet("QPushButton {background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgb(17,100,180), stop:1 rgb(12,85,165));border-radius: 25px;color: white;font-size: 18px;} QPushButton:hover {background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgb(10,90,170), stop:1 rgb(10,80,155));border-radius: 25px;color: white;font-size: 18px;}")
            self.pause_resume_button_glow.setStyleSheet("background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgba(17,100,180,100), stop:1 rgba(12,85,165,100));border-radius: 25px;color: white;font-size: 18px;")
            self.is_paused = False
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", str(e))

    def update_timer(self):
        if self.remaining_time > 0 and not self.is_paused:
            self.remaining_time -= 1
            self.update_timer_label()
        elif self.remaining_time == 0:
            self.timer.stop()
            self.show_fullscreen_message()
            close_time_text = self.close_time_input.text().strip()
            if close_time_text:
                try:
                    self.validate_time_input(close_time_text)
                    close_hours, close_minutes, close_seconds = self.parse_time_input(close_time_text)
                    close_total_seconds = close_hours * 3600 + close_minutes * 60 + close_seconds
                    if close_total_seconds <= 0:
                        raise ValueError("Время закрытия должно быть положительным числом.")
                    self.fullscreen_window.set_close_timer(close_total_seconds)
                    self.close_timer.timeout.connect(self.close_and_restart)
                    self.close_timer.start(close_total_seconds * 1000)
                except ValueError as e:
                    QMessageBox.warning(self, "Ошибка", str(e))
            else:
                self.close_and_restart()

    def update_timer_label(self):
        hours = self.remaining_time // 3600
        minutes = (self.remaining_time % 3600) // 60
        seconds = self.remaining_time % 60
        self.timer_label.setText(f"Осталось времени: {hours:02}:{minutes:02}:{seconds:02}")

    def toggle_pause_resume(self):
        if self.is_paused:
            self.timer.start(1000)
            self.is_paused = False
            QApplication.processEvents()
            self.pause_resume_button.setStyleSheet("QPushButton {background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgb(17,100,180), stop:1 rgb(12,85,165));border-radius: 25px;color: white;font-size: 18px;} QPushButton:hover {background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgb(10,90,170), stop:1 rgb(10,80,155));border-radius: 25px;color: white;font-size: 18px;}")
            self.pause_resume_button_glow.setStyleSheet("background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgba(17,100,180,100), stop:1 rgba(12,85,165,100));border-radius: 25px;color: white;font-size: 18px;")
            self.pause_resume_button.setText("Приостановить")
            self.start_button_glow.setStyleSheet("background-color: rgba(45,45,45,100);border-radius: 25px;color: white;font-size: 18px;")
            self.start_button.setStyleSheet("QPushButton {background-color: rgb(45,45,45);border-radius: 25px;color: white;font-size: 18px;} QPushButton:hover {background-color: rgb(71,74,81);border-radius: 25px;color: white;font-size: 18px;}")
            self.time_input.setEnabled(False)
            self.close_time_input.setEnabled(False)
            self.start_button.setEnabled(False)
            self.loop_checkbox.setEnabled(False)
            QApplication.processEvents()
        else:
            self.timer.stop()
            self.is_paused = True
            QApplication.processEvents()
            self.pause_resume_button.setStyleSheet("QPushButton {background-color: rgb(255,164,32);border-radius: 25px;color: white;font-size: 18px;} QPushButton:hover {background-color: rgb(235,144,22);border-radius: 25px;color: white;font-size: 18px;}")
            self.pause_resume_button_glow.setStyleSheet("background-color: rgba(255,164,32,50);border-radius: 25px;color: white;font-size: 18px;")
            self.pause_resume_button.setText("Возобновить")
            self.start_button.setStyleSheet("QPushButton {background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgb(17,100,180), stop:1 rgb(12,85,165));border-radius: 25px;color: white;font-size: 18px;} QPushButton:hover {background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgb(10,90,170), stop:1 rgb(10,80,155));border-radius: 25px;color: white;font-size: 18px;}")
            self.start_button_glow.setStyleSheet("background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgba(17,100,180,100), stop:1 rgba(12,85,165,100));border-radius: 25px;color: white;font-size: 18px;")
            self.time_input.setEnabled(True)
            self.close_time_input.setEnabled(True)
            self.start_button.setEnabled(True)
            self.loop_checkbox.setEnabled(True)
            QApplication.processEvents()

    def show_fullscreen_message(self):
        self.fullscreen_window = FullscreenMessageWindow()
        self.fullscreen_window.close_signal.connect(self.close_and_restart)
        self.fullscreen_window.show()
        screen_geometry = QDesktopWidget().screenGeometry()
        center_x = screen_geometry.width() // 2
        center_y = screen_geometry.height() // 2
        QCursor.setPos(center_x, center_y)

    def close_and_restart(self):
        self.timer.stop()
        self.close_timer.stop()
        if hasattr(self, "fullscreen_window"):
            self.fullscreen_window.close()
        if self.is_looping:
            self.start_countdown()
        elif not self.is_looping:
            self.start_button_glow.setStyleSheet("background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgba(17,100,180,100), stop:1 rgba(12,85,165,100));border-radius: 25px;color: white;font-size: 18px;")
            self.start_button.setText("Начать отсчёт")
            self.start_button.setStyleSheet("QPushButton {background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgb(17,100,180), stop:1 rgb(12,85,165));border-radius: 25px;color: white;font-size: 18px;} QPushButton:hover {background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgb(10,90,170), stop:1 rgb(10,80,155));border-radius: 25px;color: white;font-size: 18px;}")
            self.pause_resume_button_glow.setStyleSheet("background-color: rgba(45,45,45,100);border-radius: 25px;color: white;font-size: 18px;")
            self.pause_resume_button.setText("Приостановить")
            self.pause_resume_button.setStyleSheet("QPushButton {background-color: rgb(45,45,45);border-radius: 25px;color: white;font-size: 18px;} QPushButton:hover {background-color: rgb(71,74,81);border-radius: 25px;color: white;font-size: 18px;}")
            self.pause_resume_button.setEnabled(False)
            self.time_input.setEnabled(True)
            self.close_time_input.setEnabled(True)
            self.start_button.setEnabled(True)
            self.loop_checkbox.setEnabled(True)

    def mousePressEvent(self, event):
        try:
            if event.button() == QtCore.Qt.LeftButton:
                self.startPos = event.globalPos() - self.frameGeometry().topLeft()
                self.isDragging = True
                event.accept()
        except:
            pass
    def mouseMoveEvent(self, event):
        try:
            if self.isDragging:
                self.move(event.globalPos() - self.startPos)
                event.accept()
        except:
            pass
    def mouseReleaseEvent(self, event):
        try:
            if event.button() == QtCore.Qt.LeftButton and self.isDragging:
                self.isDragging = False
                event.accept()
        except:
            pass


class FullscreenMessageWindow(QWidget):
    close_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        screen_geometry = QDesktopWidget().screenGeometry()
        self.setGeometry(screen_geometry)
        self.setStyleSheet("background-color: black;")
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label = QLabel("Пора отдыхать! Время вышло.")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("""
            font-size: 48px;
            color: white;
            font-family: 'Segoe UI Semibold';
        """)
        layout.addWidget(self.label)

        self.timer_label = QLabel("Осталось времени до возвращения доступа: --:--")
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("""
            font-size: 24px;
            color: white;
            font-family: 'Segoe UI Semibold';
        """)
        layout.addWidget(self.timer_label)

        close_button = QPushButton("Нажмите сюда, чтобы экстренно закрыть")
        close_button.setStyleSheet("""
            font-size: 24px;
            font-family: 'Segoe UI Semibold';
            background-color: transparent;
            border: none;
            color: white;
        """)
        close_button.clicked.connect(self.close_window)
        close_button.setCursor(QtCore.Qt.PointingHandCursor)
        layout.addWidget(close_button)

        self.close_timer = QTimer()
        self.remaining_time = 0

    def set_close_timer(self, seconds):
        self.remaining_time = seconds
        self.update_timer_label()
        self.close_timer.timeout.connect(self.update_close_timer)
        self.close_timer.start(1000)

    def update_close_timer(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.update_timer_label()
        else:
            self.close_timer.stop()
            self.close_signal.emit()
            self.close()

    def update_timer_label(self):
        minutes = self.remaining_time // 60
        seconds = self.remaining_time % 60
        self.timer_label.setText(f"Осталось времени: {minutes:02}:{seconds:02}")

    def close_window(self):
        self.close_timer.stop()
        self.close_signal.emit()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CountdownApp()
    window.show()
    sys.exit(app.exec_())
