#!/usr/bin/python3
import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.Qt import Qt
from PyQt5 import QtCore
from PyQt5.QtCore import *
from qtwidgets import AnimatedToggle
import subprocess
import shutil
import time
sys.stdout = open(os.devnull, 'w')
LightSkyBlue = "rgb(80, 150, 201)"
DarkSkyBlue = "rgb(83, 111, 135)"


class CutomizeWidget:
    def change_font(self, name, font, size, bold, italic):
        font = QFont(font, size)
        font.setBold(bold)
        font.setItalic(italic)
        name.setFont(font)

    def customize_button(self, name, fg, bg, corners, height, width):
        name.setFixedSize(width, height)
        name.setStyleSheet(f"""
            background-color: {bg};
            color: {fg};
            border-radius: {corners}px;
        """)

    def customize_label(self, name, fg, bg, corners, height, width):
        name.setFixedSize(width, height)
        name.setStyleSheet(f"""
            background-color: {bg};
            color: {fg};
            border-radius: {corners}px;
        """)

    def customize_lineEdit(self, name, fg, bg, corners, height, width):
        name.setFixedSize(width, height)
        name.setStyleSheet(f"""
            background-color: {bg};
            color: {fg};
            border-radius: {corners}px;
        """)


cw = CutomizeWidget()


class LoadingScreen(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Creating Application")
        self.setFixedSize(800, 200)

        self.layout = QVBoxLayout()

        self.lbl = QLabel(self, text="")
        self.lbl.setAlignment(QtCore.Qt.AlignBottom)
        cw.customize_label(self.lbl, "black", None, 10, 30, 800)
        cw.change_font(self.lbl, "Futura", 24, True, False)
        self.layout.addWidget(self.lbl)

        self.bar = QProgressBar(self)
        self.bar.setMaximum(100)
        self.bar.setStyle(QCommonStyle())
        self.bar.setFixedSize(600, 20)
        self.layout.addWidget(self.bar)
        self.setLayout(self.layout)
        self.show()

        if self.bar.value() > 99:
            self.destroy()

    def increase(self, value):
        v = self.bar.value()
        while v < value:
            v = v + 1
            time.sleep(0.01)
            self.bar.setValue(v)
            QApplication.processEvents()

    def change_lbl(self, text):
        self.lbl.setText(text)

class MainWindowGUI(QWidget):

    python_file = None
    application_name = None
    application_dir = None
    icon_file = None
    readme = None
    error = False

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PY TO APP")
        self.setFixedSize(1200, 600)
        self.logo = QPixmap(
            "/Users/adityaprakash/Documents/Python Projects/PyQt/Py to App/logo.png")
        self.logo = self.logo.scaled(400, 200)
        self.icon = QLabel(self)
        self.icon.setStyleSheet("border-radius: 20;")
        self.icon.setPixmap(self.logo)
        self.icon.move(10, 10)

        self.frm = QFrame(parent=self)
        self.frm.move(10, 300)
        self.layout = QGridLayout()
        for lbltext in ["Python File:", "Application Name:", "Application Directory:", "Icon Image (.icns):"]:
            lbl = QLabel(parent=self, text=lbltext)
            self.layout.addWidget(
                lbl, ["Python File:", "Application Name:", "Application Directory:", "Icon Image (.icns):"].index(lbltext), 0)
            cw.customize_label(lbl, "black", None, 20, 40, 300)
            cw.change_font(lbl, "Futura", 24, True, False)

        self.frm.setLayout(self.layout)

        self.python_file_btn = QPushButton(text="Select File")
        cw.customize_button(self.python_file_btn, "white",
                            LightSkyBlue, 20, 40, 200)
        cw.change_font(self.python_file_btn, "Futura", 20, True, False)
        self.layout.addWidget(self.python_file_btn, 0, 1)
        self.python_file_btn.clicked.connect(self.select_python_file)

        self.python_file_label = QLabel(self.frm, text="None")
        cw.change_font(self.python_file_label, "Futura", 12, False, False)
        cw.customize_label(self.python_file_label, "black", None, 10, 40, 600)
        self.layout.addWidget(self.python_file_label, 0, 2)

        self.application_name_lineEdit = QLineEdit(self.frm)
        self.application_name_lineEdit.setAttribute(Qt.WA_MacShowFocusRect, 0)
        cw.customize_lineEdit(self.application_name_lineEdit,
                              "black", "white", 10, 40, 200)
        cw.change_font(self.application_name_lineEdit,
                       "Futura", 14, False, False)
        self.layout.addWidget(self.application_name_lineEdit, 1, 1)
        self.application_name_lineEdit.textChanged.connect(self.update_name)

        self.application_name_label = QLabel(self.frm, text=".app")
        cw.change_font(self.application_name_label, "Futura", 16, False, False)
        self.layout.addWidget(self.application_name_label, 1, 2)

        self.application_dir_btn = QPushButton(
            self.frm, text="Select Directory")
        cw.customize_button(self.application_dir_btn,
                            "white", LightSkyBlue, 20, 40, 200)
        cw.change_font(self.application_dir_btn, "Futura", 18, True, False)
        self.application_dir_btn.clicked.connect(self.select_dir)
        self.layout.addWidget(self.application_dir_btn, 2, 1)

        self.dir_label = QLabel(self.frm, text="None")
        cw.change_font(self.dir_label, "Futura", 12, False, False)
        cw.customize_label(self.dir_label, "black", None, 10, 40, 600)
        self.layout.addWidget(self.dir_label, 2, 2)

        self.create_application_button = QPushButton(
            self, text="CREATE STANDALONE APPLICATION")
        cw.customize_button(self.create_application_button,
                            "white", LightSkyBlue, 10, 40, 500)
        cw.change_font(self.create_application_button,
                       "Futura", 20, True, False)
        self.create_application_button.move(20, 550)
        self.create_application_button.clicked.connect(self.create_application)

        self.select_icon_file = QPushButton(text="Select Icon File")
        cw.customize_button(self.select_icon_file,
                            "white", LightSkyBlue, 20, 40, 200)
        cw.change_font(self.select_icon_file, "Futura", 20, True, False)
        self.layout.addWidget(self.select_icon_file, 3, 1)
        self.select_icon_file.clicked.connect(self.select_icon)

        self.icon_file_label = QLabel(self.frm, text="None")
        cw.change_font(self.icon_file_label, "Futura", 12, False, False)
        self.layout.addWidget(self.icon_file_label, 3, 2)

        self.cFrame = QFrame(self)
        self.cFrame.setFixedSize(600, 200)
        self.cFrame.move(500, 10)
        self.cFrame.setStyleSheet("""
            border-radius: 10;
            background-color: white;
        """)
        self.toggle = AnimatedToggle(self)
        self.toggle.move(520, 30)
        self.toggle.setChecked(True)
        self.lbl = QLabel(self, text="Include 'setup.py'")
        cw.change_font(self.lbl, "Futura", 16, True, False)
        self.lbl.move(575, 41)

        self.upload_readme = QPushButton(
            self, text="Upload File 📁")
        cw.change_font(self.upload_readme, "Futura", 14, True, False)
        cw.customize_button(self.upload_readme, "white",
                            LightSkyBlue, 10, 40, 200)
        self.upload_readme.move(800, 30)
        self.upload_readme.clicked.connect(self.upload_readme_file)
        self.readmelbl = QLabel(self, text="None")
        cw.customize_label(self.readmelbl, "black", None, 10, 40, 200)
        cw.change_font(self.readmelbl, "Futura", 14, False, False)
        self.readmelbl.move(800, 80)

        self.python2radiobutton = QRadioButton(self, text="Python 2")
        self.python2radiobutton.move(550, 80)
        cw.change_font(self.python2radiobutton, "Futura", 16, True, False)

        self.python3radiobutton = QRadioButton(self, text="Python3")
        self.python3radiobutton.move(550, 120)
        cw.change_font(self.python3radiobutton, "Futura", 16, True, False)
        self.python3radiobutton.setChecked(True)

    def select_python_file(self):
        self.file_dialog = QFileDialog(self, "Select Python File")
        self.file_dialog.setNameFilters(
            ["Python Files (*.py)", "Python Window Files (*.pyw)"])
        self.file_dialog.selectNameFilter("Python Files (*.py)")

        if self.file_dialog.exec():
            if os.path.isfile(self.file_dialog.selectedFiles()[0]) == False or os.path.isdir(self.file_dialog.selectedFiles()[0]) == True:
                self.python_file_label.setText("ERROR: NOT A FILE")
                cw.customize_label(self.python_file_label,
                                   "red", None, 10, 40, 600)
                return None
            MainWindowGUI.python_file = self.file_dialog.selectedFiles()
            MainWindowGUI.python_file = MainWindowGUI.python_file[0]
            self.python_file_label.setText(MainWindowGUI.python_file)
            cw.customize_label(self.python_file_label,
                               "black", None, 10, 40, 600)
            self.file_dialog.destroy()

    def select_dir(self):
        self.file_dialog = QFileDialog()
        MainWindowGUI.application_dir = self.file_dialog.getExistingDirectory()
        self.dir_label.setText(MainWindowGUI.application_dir)
        cw.customize_label(self.dir_label,
                           "black", None, 10, 40, 600)
        self.file_dialog.destroy()

    def select_icon(self):
        self.file_dialog = QFileDialog(self, "Select Icon File")
        self.file_dialog.setNameFilters(
            ["Apple Icon Files (*.icns)"])
        self.file_dialog.selectNameFilter("Apple Icon Files (*.icns)")

        if self.file_dialog.exec():
            MainWindowGUI.icon_file = self.file_dialog.selectedFiles()
            MainWindowGUI.icon_file = MainWindowGUI.icon_file[0]
            self.icon_file_label.setText(MainWindowGUI.icon_file)
            cw.customize_label(self.icon_file_label,
                               "black", None, 10, 40, 600)
            self.file_dialog.destroy()

    def update_name(self):
        self.application_name_label.setText(
            f"{self.application_name_lineEdit.text()}.app")

    def upload_readme_file(self):
        self.file_dialog = QFileDialog(self, "Upload REAME")
        self.file_dialog.setNameFilters(
            ["Text Files (*.txt)", "Markdown Files (*.md)"])
        if self.file_dialog.exec():
            MainWindowGUI.readme = self.file_dialog.selectedFiles()[0]
            self.readmelbl.setText(str(MainWindowGUI.readme.split(
                "/")[len(MainWindowGUI.readme.split("/")) - 1]))
            print(str(MainWindowGUI.readme.split("/")
                      [len(MainWindowGUI.readme.split("/")) - 1]))

    def create_application(self):
        try:
            os.remove("setup.py")
        except:
            pass
        if MainWindowGUI.python_file != None and MainWindowGUI.application_dir != None:
            MainWindowGUI.application_name = self.application_name_lineEdit.text()
            loading = LoadingScreen()
            loading.show()

            loading.increase(7)
            loading.change_lbl("Creating Directories...")

            def execute_command(command):
                command = command.split(" ")
                execute = subprocess.run(
                    command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, text=True)
                if execute.returncode != 0:
                    MainWindowGUI.error = True

            try:
                os.mkdir(
                    f"{MainWindowGUI.application_dir}/{MainWindowGUI.application_name}")
            except:
                pass

            os.chdir(
                f"{MainWindowGUI.application_dir}/{MainWindowGUI.application_name}")

            loading.increase(20)
            loading.change_lbl("Installing py2app...")

            if self.python3radiobutton.isChecked():
                execute_command("pip3 install py2app")
            else:
                execute_command("pip install py2app")

            loading.increase(40)
            loading.change_lbl("Creating setup file...")

            subprocess.run(
                ["py2applet", "--make-setup", MainWindowGUI.python_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, text=True)

            if MainWindowGUI.icon_file != None:
                with open("setup.py", "r") as file:
                    lines = file.readlines()
                    print(str(lines))
                    lines[(lines.index("OPTIONS = {}\n"))
                          ] = f"OPTIONS = {{'iconfile': '{MainWindowGUI.icon_file}'}}\n"
                with open("setup.py", "w") as file:
                    file.writelines(lines)
                    print(str(lines))

            loading.increase(80)
            loading.change_lbl("Creating Standalone Application...")

            if self.python3radiobutton.isChecked():
                subprocess.run(["python3", "setup.py", "py2app"],
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL,
                               text=True)
            else:
                subprocess.run(["python2", "setup.py", "py2app"],
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL,
                               text=True)

            loading.increase(80)
            loading.change_lbl("Executing setup.py...")

            python_file_ = str(MainWindowGUI.python_file.split(
                "/")[len(MainWindowGUI.python_file.split("/")) - 1][: -3])

            loading.increase(100)
            loading.change_lbl("Finishing Touches...")

            os.chdir(
                f"{MainWindowGUI.application_dir}/{MainWindowGUI.application_name}/dist/")
            os.rename(f"{python_file_}.app",
                      f"{MainWindowGUI.application_name}.app")
            shutil.move(f"{MainWindowGUI.application_dir}/{MainWindowGUI.application_name}/dist/{MainWindowGUI.application_name}.app",
                        f"{MainWindowGUI.application_dir}/{MainWindowGUI.application_name}/{MainWindowGUI.application_name}.app")
            os.chdir(
                f"{MainWindowGUI.application_dir}/{MainWindowGUI.application_name}")

            if MainWindowGUI.readme != None:
                shutil.copy(MainWindowGUI.readme, "README.md")
            if not self.toggle.isChecked():
                os.remove("setup.py")
            shutil.rmtree("dist")
            shutil.rmtree("build")

        else:
            if self.python_file_label.text() == "None" or self.python_file_label == "ERROR: NOT A FILE":
                self.python_file_label.setText("ERROR: FILE NOT SELECTED")
                cw.customize_label(self.python_file_label,
                                   "red", None, 10, 40, 600)

            if self.application_name_label.text() == ".app":
                self.application_name_label.setText("ERROR: NAME UNDEFINED")
                cw.customize_label(self.application_name_label,
                                   "red", None, 10, 40, 600)

            if self.dir_label.text() == "None":
                self.dir_label.setText("ERROR: DIRECTORY NOT SELECTED")
                cw.customize_label(self.dir_label, "red", None, 10, 40, 600)

            if self.icon_file_label.text() == "None" or self.icon_file_label == "ERROR: NOT A FILE":
                self.icon_file_label.setText("ERROR: ICON FILE NOT SELECTED")
                cw.customize_label(self.icon_file_label,
                                   "red", None, 10, 40, 600)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindowGUI()
    window.show()
    sys.exit(app.exec())
