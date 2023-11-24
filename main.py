import sys
from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QInputDialog, QPushButton, QListWidget

from PyQt6.QtWebEngineWidgets import QWebEngineView

class WebPageViewer(QMainWindow): #создан коммит
    def init(self, interval_seconds=5):
        super().init()

        self.urls = []
        self.interval_seconds = interval_seconds
        self.current_index = 0

        self.web_view = QWebEngineView()
        self.setCentralWidget(self.web_view)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_next_page)
        self.timer.start(self.interval_seconds * 1000)  # Перевод в миллисекунды

        self.show_next_page()

    def show_next_page(self):
        if self.urls:
            url = QUrl.fromUserInput(self.urls[self.current_index]['url'])
            self.web_view.setUrl(url)
            self.current_index = (self.current_index + 1) % len(self.urls)

    def add_website(self, url, interval):
        new_website = {'url': url, 'interval': interval}
        self.urls.append(new_website)
        self.timer.start(self.interval_seconds * 1000)  # Запустить таймер, если он был остановлен

    def remove_website(self, index):
        if 0 <= index < len(self.urls):
            del self.urls[index]
            if not self.urls:
                self.timer.stop()  # Остановить таймер, если список пуст

class WebPageViewerApp(QApplication):
    def init(self, argv):
        super().init(argv)

        self.web_viewer = WebPageViewer()

        self.main_window = QMainWindow()
        self.add_website_button = QPushButton("Добавить веб-сайт", self.main_window)
        self.add_website_button.clicked.connect(self.show_add_website_dialog)

        self.remove_website_button = QPushButton("Удалить веб-сайт", self.main_window)
        self.remove_website_button.clicked.connect(self.show_remove_website_dialog)

        self.website_list = QListWidget(self.main_window)

        layout = QVBoxLayout(self.main_window)
        layout.addWidget(self.web_viewer)
        layout.addWidget(self.add_website_button)
        layout.addWidget(self.remove_website_button)
        layout.addWidget(self.website_list)

        central_widget = QWidget(self.main_window)
        central_widget.setLayout(layout)
        self.main_window.setCentralWidget(central_widget)

        self.main_window.show()

    def show_add_website_dialog(self):
        url, ok1 = QInputDialog.getText(self.main_window, 'Добавить веб-сайт', 'Введите URL:')
        interval, ok2 = QInputDialog.getInt(self.main_window, 'Добавить веб-сайт', 'Введите интервал (секунды):', value=5)

        if ok1 and ok2:
            self.web_viewer.add_website(url, interval)
            self.update_website_list()

    def show_remove_website_dialog(self):
        selected_item = self.website_list.currentRow()
        if selected_item != -1:
            self.web_viewer.remove_website(selected_item)
            self.update_website_list()

    def update_website_list(self):
        self.website_list.clear()
        for website in self.web_viewer.urls:
            self.website_list.addItem(f"{website['url']} - {website['interval']} сек")

if name == "main":
    app = WebPageViewerApp(sys.argv)
    sys.exit(app.exec())