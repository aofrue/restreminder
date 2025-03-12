import sys
from PySide2 import QtCore
from PySide2.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit,
    QPushButton, QMessageBox, QDesktopWidget, QCheckBox
)
from PySide2.QtCore import QTimer, Qt, Signal
from PySide2.QtGui import QCursor


class CountdownApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("RestReminder")
        self.setGeometry(100, 100, 400, 200)

        # Запрещаем изменение размера окна
        self.setFixedSize(400, 200)

        # Основной виджет и layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Поле для ввода времени таймера
        self.label_timer = QLabel("Введите время таймера (час. мин. сек.):")
        self.layout.addWidget(self.label_timer)

        self.time_input = QLineEdit()
        self.time_input.setPlaceholderText("Пример: 1 30 0 (1 час 30 минут 0 секунд)")
        self.layout.addWidget(self.time_input)

        # Поле для ввода времени автоматического закрытия окна "Время вышло"
        self.label_close_time = QLabel("Введите время закрытия окна 'Время вышло' (час. мин. сек.):")
        self.layout.addWidget(self.label_close_time)

        self.close_time_input = QLineEdit()
        self.close_time_input.setPlaceholderText("Пример: 0 5 0 (5 минут 0 секунд)")
        self.layout.addWidget(self.close_time_input)

        # Метка для отображения оставшегося времени
        self.timer_label = QLabel("Осталось времени: --:--:--")
        self.layout.addWidget(self.timer_label)

        # Чекбокс для зацикливания процесса
        self.loop_checkbox = QCheckBox("Зациклить процесс")
        self.layout.addWidget(self.loop_checkbox)

        # Кнопка "Начать отсчёт"
        self.start_button = QPushButton("Начать отсчёт")
        self.start_button.clicked.connect(self.start_countdown)
        self.layout.addWidget(self.start_button)

        # Кнопка приостановки/возобновления
        self.pause_resume_button = QPushButton("Приостановить")
        self.pause_resume_button.clicked.connect(self.toggle_pause_resume)
        self.pause_resume_button.setEnabled(False)  # Кнопка неактивна до старта таймера
        self.layout.addWidget(self.pause_resume_button)

        # Таймеры
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)  # Подключаем сигнал один раз
        self.close_timer = QTimer()
        self.remaining_time = 0
        self.is_looping = False
        self.is_paused = False  # Флаг приостановки таймера

    def parse_time_input(self, input_text):
        """Парсит ввод времени в формате 'часы минуты секунды'."""
        try:
            parts = input_text.split()
            if len(parts) != 3:
                raise ValueError("Необходимо ввести ровно три числа через пробел: часы, минуты и секунды.")
            hours, minutes, seconds = map(int, parts)
            if not (0 <= hours <= 24 and 0 <= minutes <= 59 and 0 <= seconds <= 59):
                raise ValueError("Неверный формат времени. Введите значения в диапазоне: часы (0-24), минуты (0-59), секунды (0-59).")
            if hours == 0 and minutes == 0 and seconds == 0:
                raise ValueError("Время не может быть 0 0 0.")
            return hours, minutes, seconds
        except ValueError as e:
            raise ValueError(str(e))

    def validate_time_input(self, input_text):
        """Проверяет, что все поля ввода заполнены."""
        if not input_text.strip():
            raise ValueError("Необходимо ввести все значения: часы, минуты и секунды.")

    def start_countdown(self):
        try:
            # Проверяем, что все поля заполнены
            time_input_text = self.time_input.text().strip()
            self.validate_time_input(time_input_text)

            # Парсим время из поля ввода
            hours, minutes, seconds = self.parse_time_input(time_input_text)
            total_seconds = hours * 3600 + minutes * 60 + seconds
            if total_seconds <= 0:
                raise ValueError("Время должно быть положительным числом.")

            self.remaining_time = total_seconds
            self.is_looping = self.loop_checkbox.isChecked()  # Проверяем чекбокс

            # Обновляем метку таймера
            self.update_timer_label()

            # Запускаем таймер
            self.timer.start(1000)  # Обновление каждую секунду
            self.pause_resume_button.setEnabled(True)  # Активируем кнопку приостановки/возобновления
            self.pause_resume_button.setText("Приостановить")  # Устанавливаем текст кнопки
            self.is_paused = False  # Сбрасываем флаг приостановки
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", str(e))

    def update_timer(self):
        if self.remaining_time > 0 and not self.is_paused:
            self.remaining_time -= 1
            self.update_timer_label()
        elif self.remaining_time == 0:
            self.timer.stop()
            self.show_fullscreen_message()

            # Если указано время закрытия окна "Время вышло"
            close_time_text = self.close_time_input.text().strip()
            if close_time_text:
                try:
                    self.validate_time_input(close_time_text)
                    close_hours, close_minutes, close_seconds = self.parse_time_input(close_time_text)
                    close_total_seconds = close_hours * 3600 + close_minutes * 60 + close_seconds
                    if close_total_seconds <= 0:
                        raise ValueError("Время закрытия должно быть положительным числом.")

                    # Закрываем окно "Время вышло" через заданное время
                    self.fullscreen_window.set_close_timer(close_total_seconds)
                    self.close_timer.timeout.connect(self.close_and_restart)
                    self.close_timer.start(close_total_seconds * 1000)
                except ValueError as e:
                    QMessageBox.warning(self, "Ошибка", str(e))
            else:
                # Если время закрытия не указано, сразу перезапускаем таймер
                self.close_and_restart()

    def update_timer_label(self):
        # Форматируем оставшееся время в формат HH:MM:SS
        hours = self.remaining_time // 3600
        minutes = (self.remaining_time % 3600) // 60
        seconds = self.remaining_time % 60
        self.timer_label.setText(f"Осталось времени: {hours:02}:{minutes:02}:{seconds:02}")

    def toggle_pause_resume(self):
        """Переключает состояние таймера между приостановкой и возобновлением."""
        if self.is_paused:
            self.timer.start(1000)  # Возобновляем таймер
            self.pause_resume_button.setText("Приостановить")
            self.is_paused = False
        else:
            self.timer.stop()  # Приостанавливаем таймер
            self.pause_resume_button.setText("Возобновить")
            self.is_paused = True

    def show_fullscreen_message(self):
        # Создаём полноэкранное окно
        self.fullscreen_window = FullscreenMessageWindow()
        self.fullscreen_window.close_signal.connect(self.close_and_restart)  # Подключаем сигнал закрытия
        self.fullscreen_window.show()

        # Перемещаем курсор в центр экрана
        screen_geometry = QDesktopWidget().screenGeometry()
        center_x = screen_geometry.width() // 2
        center_y = screen_geometry.height() // 2
        QCursor.setPos(center_x, center_y)  # Перемещаем курсор в центр

    def close_and_restart(self):
        # Останавливаем все таймеры
        self.timer.stop()
        self.close_timer.stop()

        # Закрываем окно "Время вышло", если оно существует
        if hasattr(self, "fullscreen_window"):
            self.fullscreen_window.close()

        # Если зацикливание включено, перезапускаем таймер
        if self.is_looping:
            self.start_countdown()

class FullscreenMessageWindow(QWidget):
    close_signal = Signal()  # Сигнал для закрытия окна

    def __init__(self):
        super().__init__()

        # Устанавливаем флаги для безрамочного окна поверх всех остальных
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        # Получаем разрешение экрана
        screen_geometry = QDesktopWidget().screenGeometry()
        self.setGeometry(screen_geometry)

        # Устанавливаем чёрный фон для всего окна
        self.setStyleSheet("background-color: black;")

        # Создаём layout и добавляем текстовое сообщение
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Текст "Время истекло!"
        self.label = QLabel("Пора отдыхать! Время вышло.")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("""
            font-size: 48px;
            color: white;
            font-family: 'Segoe UI Semibold';
        """)
        layout.addWidget(self.label)

        # Таймер до закрытия окна
        self.timer_label = QLabel("Осталось времени до возвращения доступа: --:--")
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("""
            font-size: 24px;
            color: white;
            font-family: 'Segoe UI Semibold';
        """)
        layout.addWidget(self.timer_label)

        # Кнопка экстренного закрытия с прозрачным фоном
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

        # Таймер для отсчёта времени до закрытия окна
        self.close_timer = QTimer()
        self.remaining_time = 0

    def set_close_timer(self, seconds):
        # Устанавливаем таймер для закрытия окна
        self.remaining_time = seconds
        self.update_timer_label()
        self.close_timer.timeout.connect(self.update_close_timer)
        self.close_timer.start(1000)  # Обновление каждую секунду

    def update_close_timer(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.update_timer_label()
        else:
            self.close_timer.stop()
            self.close_signal.emit()
            self.close()

    def update_timer_label(self):
        # Форматируем оставшееся время в формат MM:SS
        minutes = self.remaining_time // 60
        seconds = self.remaining_time % 60
        self.timer_label.setText(f"Осталось времени: {minutes:02}:{seconds:02}")

    def close_window(self):
        # Останавливаем таймер закрытия
        self.close_timer.stop()
        self.close_signal.emit()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CountdownApp()
    window.show()
    sys.exit(app.exec_())