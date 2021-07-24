# MultiPixelBox version 1.0 (22.07.2021)
import sys
import time
# ------------------------------------------
import Image_builder
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
from PyQt5.QtCore import *  # QThread, pyqtSignal,
from PyQt5 import uic

folder_from = ''
folder_to = ''
scale = 1


class App(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.start()
        self.set()
        self.progress = ProgressBar()
        self.build = BuilderCall()

    def start(self):
        self.ui = uic.loadUi('MultiPixelBox.ui')
        self.ui.show()

    def set(self):
        self.ui.btn_from.clicked.connect(lambda: self.click(command='btn_from'))
        self.ui.btn_to.clicked.connect(lambda: self.click(command='btn_to'))
        self.ui.btn_resize.clicked.connect(lambda: self.click(command='btn_resize'))

    def click(self, command):
        global folder_from, folder_to, scale
        if command == 'btn_from':
            folder = QFileDialog.getExistingDirectory()
            self.ui.line_path_from.setText(folder)
        elif command == 'btn_to':
            folder = QFileDialog.getExistingDirectory()
            self.ui.line_path_to.setText(folder)
        elif command == 'btn_resize':
            scale = self.ui.spinBox_scale.value()
            folder_from = self.ui.line_path_from.text()
            folder_to = self.ui.line_path_to.text()

            Image_builder.done = True
            self.build.start()

            self.progress.start()
            self.progress.update_progress.connect(self.progress_bar_update)
            self.progress.update_label.connect(self.label_progress)

    def progress_bar_update(self, val):
        self.ui.progressBar.setValue(val)

    def label_progress(self, val):
        self.ui.label_progress.setText(val)


class BuilderCall(QThread):
    global folder_from, folder_to, scale

    def run(self):
        Image_builder.multiplier(folder_from, folder_to, scale)


class ProgressBar(QThread):
    update_progress = pyqtSignal(int)
    update_label = pyqtSignal(str)

    def run(self):
        self.update_progress.emit(0)
        while Image_builder.done:
            time.sleep(0.2)
            self.update_label.emit(f'Processing... {Image_builder.file_name}')
            try:
                if Image_builder.progress == Image_builder.image_count:
                    percent = 100
                else:
                    percent = round(Image_builder.progress / Image_builder.image_count * 100)
                self.update_progress.emit(percent)
            except ZeroDivisionError:
                print('Zero division')
        self.update_label.emit('Complete')


# ------------------------------------------------------ Main ----------------------------------------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    app.exec_()
