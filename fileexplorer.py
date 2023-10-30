###########
# Imports #
###########
import os
import sys
import time
import json
import random
import logging
import argparse
import datetime
import gzip
import configparser
from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont, QColor
from PyQt6.QtCore import QRegularExpression, Qt
import requests
import asyncio
import subprocess
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QFileDialog,QAbstractButton,QAbstractGraphicsShapeItem,QAbstractItemDelegate, QMessageBox, QTextBrowser,QListWidget
#setup varibalbes

current_file = ''


# file explorer class
class FileExplorer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'File Explorer'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
     # setup list widget
        self.listWidget = QListWidget(self)
        self.listWidget.setGeometry(0, 0, 640, 480)
        self.listWidget.itemDoubleClicked.connect(self.on_click)
        self.listWidget.itemClicked.connect(self.on_click)
        self.listWidget.itemEntered.connect(self.on_click)
        self.listWidget.itemPressed.connect(self.on_click)
        self.listWidget.itemSelectionChanged.connect(self.on_click)
        self.listWidget.itemActivated.connect(self.on_click)
        self.listWidget.itemChanged.connect(self.on_click)
        self.listWidget.itemEntered.connect(self.on_click)
        self.listWidget.itemPressed.connect(self.on_click)
        self.listWidget.clear()
        # if the user has opened a folder then show the contents of that folder
        if os.path.isdir(current_file):
            for file in os.listdir(current_file):
                self.listWidget.addItem(file)
        # if the user has opened a file then show the contents of that file in the main window
        elif os.path.isfile(current_file):
            with open(current_file, 'r') as file:
                self.textEdit.setText(file.read())
        
       

    def on_click(self):
        global selected
        selected = self.listWidget.currentItem().text()
        print(selected)
       
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        # create

    def context_menu(self, pos):
        menu = self.textEdit.createStandardContextMenu()
        menu.addSeparator()
        menu.addAction("Custom Action")
        menu.exec_(self.textEdit.mapToGlobal(pos))

    def text_changed(self):
        print("Text Changed")

    def cursor_position_changed(self):
        print("Cursor Position Changed")

    def selection_changed(self):
        print("Selection Changed")

    def copy_available(self, b):
        print("Copy Available")

if __name__ == "main":
    app = QApplication(sys.argv)
    ex = FileExplorer()
    ex.show()
    sys.exit(app.exec_())