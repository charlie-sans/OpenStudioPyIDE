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

import requests
import subprocess
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QFileDialog,QAbstractButton,QAbstractGraphicsShapeItem,QAbstractItemDelegate, QMessageBox
#setup varibalbes
config_file = 'config.ini'
current_file = ''




def print_version():
    print('OpenStudioPyIDE v0.1.0')
    print('Created by: OpenStudioPyIDE Team')

def print_status(func):
    def wrapper(*args, **kwargs):
        print('Running {func}...'.format(func=func.__name__))
        func(*args, **kwargs)
        print('Finished {func}...'.format(func=func.__name__))
    return wrapper
parser = argparse.ArgumentParser(description='help for OpenStudioPyIDE')
parser.add_argument('-p', '--project', help='project name, use only if running from external script')
parser.add_argument('-s', '--script', help='script name to run, use only if running from external script')
parser.add_argument('-d', '--debug', help='debug mode, use only if something went woops', action='store_true')
parser.add_argument('-v', '--version', help='prints the version', action='store_true')
parser.add_argument('-l', '--log', help='log file name, use only if you want to change the log file name')


args = parser.parse_args()

# setup logging
if args.log:
    logging.basicConfig(filename="OpenIDE.crsh", level=logging.DEBUG)
else:
    print('No log file specified, using default log file name')

# setup config file
try:
    if os.path.exists('config.ini'):
        config_file = 'config.ini'
        configparser = configparser.ConfigParser()
        configparser.read(config_file)
        background = configparser['IDE']['background']
        color = configparser['IDE']['color']
        theme = configparser['IDE']['theme']
    else:
        print('No config file found, using default settings')
        background = 'white'
        color = 'black'
        theme = 'light'
        font = 'Arial'
        font_size = '12'

except Exception as e:
    logging.error('Error: {e}'.format(e))
    print('Error: {e}'.format(e))
    sys.exit(1)

if theme == 'light':
        background = 'white'
        color = 'black'
        font = 'Arial'
        font_size = '12'
elif theme == 'dark':
        background = 'black'
        color = 'white'
        font = 'Arial'
        font_size = '12'
elif theme == 'water':
        background = 'blue'
        color = 'white'
        font = 'Arial'
        font_size = '12'
elif theme == 'fire':
      background = 'red'
      color = 'orange'
      font = 'Arial'
      font_size = '12'
      

# setup main window


app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle('OpenStudioPyIDE')
window.setGeometry(100, 100, 800, 600)

# setup menu bar with submenus
menu = window.menuBar()
file_menu = menu.addMenu('File')
edit_menu = menu.addMenu('Edit')
view_menu = menu.addMenu('View')
run_menu = menu.addMenu('Run')
help_menu = menu.addMenu('Help')

# setup file menu
new_action = file_menu.addAction('New')
open_action = file_menu.addAction('Open')
save_action = file_menu.addAction('Save')
save_as_action = file_menu.addAction('Save As')
exit_action = file_menu.addAction('Exit')

# setup edit menu
undo_action = edit_menu.addAction('Undo')
redo_action = edit_menu.addAction('Redo')
cut_action = edit_menu.addAction('Cut')
copy_action = edit_menu.addAction('Copy')
paste_action = edit_menu.addAction('Paste')
find_action = edit_menu.addAction('Find')
replace_action = edit_menu.addAction('Replace')
select_all_action = edit_menu.addAction('Select All')

# setup view menu
zoom_in_action = view_menu.addAction('Zoom In')
zoom_out_action = view_menu.addAction('Zoom Out')
toggle_fullscreen_action = view_menu.addAction('Toggle Fullscreen')
toggle_line_numbers_action = view_menu.addAction('Toggle Line Numbers')
toggle_status_bar_action = view_menu.addAction('Toggle Status Bar')
toggle_tool_bar_action = view_menu.addAction('Toggle Tool Bar')
toggle_word_wrap_action = view_menu.addAction('Toggle Word Wrap')

# setup run menu
run_action = run_menu.addAction('Run')
run_selection_action = run_menu.addAction('Run Selection')
run_file_action = run_menu.addAction('Run File')
run_configuration_action = run_menu.addAction('Run Configuration')
update_action = run_menu.addAction('Update')

# setup help menu
about_action = help_menu.addAction('About')
help_action = help_menu.addAction('Help')

# setup toolbar
toolbar = window.addToolBar('Toolbar')
toolbar.addAction(new_action)
toolbar.addAction(open_action)
toolbar.addAction(save_action)
toolbar.addAction(save_as_action)
toolbar.addAction(exit_action)
toolbar.addAction(undo_action)
toolbar.addAction(redo_action)


# setup text editor
text_editor = QTextEdit()
text_editor.setStyleSheet('background-color: {background}; color: {color}; font-family: {font}; font-size: {font_size};'.format(background=background, color=color, font=font, font_size=font_size))
window.setCentralWidget(text_editor)


# setup status bar
status_bar = window.statusBar()
status_bar.showMessage('Ready')

# setup signals and slots
def new_file():
    status_bar.showMessage('New File')
    text_editor.clear()
    logging.info('New File')

    # open the default dialog to create a file then open it
    dialog = QFileDialog()
    options = dialog.options()
    
    file_name, _ = dialog.getSaveFileName(window, "Create New File", "", "All Files (*);;Text Files (*.txt)", options=options)
    if file_name:
        with open(file_name, 'w') as f:
            f.write('')
    

def open_file(file_name=None):
    status_bar.showMessage('Open File')
    logging.info('Open File')
    global current_file
    
    if file_name:
        
        with open(file_name, 'r') as f:
            text_editor.setPlainText(f.read())
    else:
        # open the default dialog to open a file
        dialog = QFileDialog()
        options = dialog.options()

        file_name, _ = dialog.getOpenFileName(window, "Open File", "", "All Files (*);;Text Files (*.txt)", options=options)
        if file_name:
            with open(file_name, 'r') as f:
                text_editor.setPlainText(f.read())
        

global file_name

def save_file():
    global current_file

    if current_file:
        with open(current_file, 'w') as f:
            f.write(text_editor.toPlainText())
        status_bar.showMessage('File saved')
        logging.info('File saved')
    else:
        dialog = QFileDialog()
        options = dialog.options()

        file_name, _ = QFileDialog.getSaveFileName(window, "Save File", "", "All Files (*);;Text Files (*.txt)", options=options)
        if file_name:
            with open(file_name, 'w') as f:
                f.write(text_editor.toPlainText())
            current_file = file_name
            status_bar.showMessage('File saved')
            logging.info('File saved')

def save_as_file():
    status_bar.showMessage('Save As File')
    logging.info('Save As File')

    # open the default dialog to save a file
    dialog = QFileDialog()
    options = dialog.options()

    file_name, _ = dialog.getSaveFileName(window, "Save File", "", "All Files (*);;Text Files (*.txt)", options=options)
    if file_name:
        with open(file_name, 'w') as f:
            f.write(text_editor.toPlainText())

def exit_file():
    status_bar.showMessage('Exit File')
    logging.info('Exit File')
    sys.exit(0)

def undo_file():
        status_bar.showMessage('Undo File')
        logging.info('Undo File')
    
def redo_file():
        status_bar.showMessage('Redo File')
        logging.info('Redo File')

def cut_file():
        status_bar.showMessage('Cut File')
        logging.info('Cut File')

def copy_file():
        status_bar.showMessage('Copy File')
        logging.info('Copy File')

def paste_file():   
        status_bar.showMessage('Paste File')
        logging.info('Paste File')

def find_file():
        status_bar.showMessage('Find File')
        logging.info('Find File')

def replace_file():
        status_bar.showMessage('Replace File')
        logging.info('Replace File')

def select_all_file():
        status_bar.showMessage('Select All File')
        logging.info('Select All File')

def zoom_in_file():
        status_bar.showMessage('Zoom In File')
        logging.info('Zoom In File')

def zoom_out_file():
        status_bar.showMessage('Zoom Out File')
        logging.info('Zoom Out File')
        
def toggle_fullscreen_file():
        status_bar.showMessage('Toggle Fullscreen File')
        logging.info('Toggle Fullscreen File')

def toggle_line_numbers_file():
        status_bar.showMessage('Toggle Line Numbers File')
        logging.info('Toggle Line Numbers File')

def toggle_status_bar_file():
        status_bar.showMessage('Toggle Status Bar File')
        logging.info('Toggle Status Bar File')

def toggle_tool_bar_file():
        status_bar.showMessage('Toggle Tool Bar File')
        logging.info('Toggle Tool Bar File')

def toggle_word_wrap_file():
        status_bar.showMessage('Toggle Word Wrap File')
        logging.info('Toggle Word Wrap File')

def run_file():
        status_bar.showMessage('Run File')
        logging.info('Run File')

def run_selection_file():
        status_bar.showMessage('Run Selection File')
        logging.info('Run Selection File')

def run_configuration_file():
        open_file("config.ini")
        status_bar.showMessage('Run Configuration File')
        logging.info('Run Configuration File')

def about_file():
        status_bar.showMessage('About File')
        logging.info('About File')

def help_file():
        app = QApplication(sys.argv)
        window = QMainWindow()
        window.setWindowTitle('OpenStudioPyIDE')
        window.setGeometry(100, 100, 800, 600)
        text_box = QTextEdit()
        text_box.setReadOnly(True)
        window.setCentralWidget(text_box)
        try:
                with open('help.txt', 'r') as f:
                        text_box.setPlainText(f.read())
        except FileNotFoundError:
                print('Help file not found')
        except Exception as e:
                logging.error('Error: {e}'.format(e))
        status_bar.showMessage('Help File')
        logging.info('Help File')

# setup run file sections for detecting if the file has an extention then run it


def run_file():
        global current_file

        if current_file:
                ext = os.path.splitext(current_file)[1]

                try:
                        if ext == '.py':
                                # run a Python file
                                exec(open(current_file).read())
                        elif ext == '.cs':
                                subprocess.Popen(['dotnet run', current_file])
                                pass
                        elif ext == '.js':
                                subprocess.Popen(['node', current_file])
                                pass
                        else:
                                # unsupported file type
                                raise Exception('Unsupported file type, please make a feature request on GitHub')
                except Exception as e:
                        logging.error('Error: {}'.format(e))
        else:
                status_bar.showMessage('No file selected')
                logging.warning('No file selected')


# setup an updater to check if the github repo has a new version in the versions list
def update():
        global current_version
        # get the latest version from the server
        r = requests.get('https://raw.githubusercontent.com/charlie-sans/OpenStudioPyIDE/main/versions.json')
        if r.status_code == 200:
                # parse the JSON data
                try:
                        data = json.loads(r.content)
                        with open('version.txt', 'r') as f:
                                current_version = f.read().strip()
                       # get the OpenStudioPYIDE section
                        # get the Versions array
                        versions_array = data[0]['Versions']

                                # get a list of all the version numbers
                        versions = [v['version'] for v in versions_array]
                except json.JSONDecodeError as e:
                        print('Error decoding JSON data:', e)
                        return
                # check if the latest version is newer than the current version
                if current_version in versions:
                        print('You have the latest version')
                else:
                        latest_version = max(versions)
                        #show a message box to tell the user to update
                        msg = QMessageBox()
                        msg.setWindowTitle('Update')
                        msg.setText('There is a new version available, please update')
                        msg.setInformativeText('Your version: {current_version}\nLatest version: {latest_version}\nPlease update at github.com/Charlie-sans/OpenStudioPyIDE'.format(current_version=current_version, latest_version=latest_version))
                        msg.setIcon(QMessageBox.Icon.Information)
                        msg.exec()
                        




                        #print('There is a new version available, please update')
                        #print('Your version: {current_version}'.format(current_version=current_version))
                        #print('Latest version: {latest_version}'.format(latest_version=latest_version))
                        #print('Please update at github.com/Charlie-sans/OpenStudioPyIDE')
                        
        else:
                print('Error getting version information:', r.status_code)


# connect signals and slots

new_action.triggered.connect(new_file)
open_action.triggered.connect(open_file)
save_action.triggered.connect(save_file)
save_as_action.triggered.connect(save_as_file)
exit_action.triggered.connect(exit_file)
undo_action.triggered.connect(undo_file)
redo_action.triggered.connect(redo_file)
cut_action.triggered.connect(cut_file)
copy_action.triggered.connect(copy_file)
paste_action.triggered.connect(paste_file)
find_action.triggered.connect(find_file)
replace_action.triggered.connect(replace_file)
select_all_action.triggered.connect(select_all_file)
zoom_in_action.triggered.connect(zoom_in_file)
zoom_out_action.triggered.connect(zoom_out_file)
toggle_fullscreen_action.triggered.connect(toggle_fullscreen_file)
toggle_line_numbers_action.triggered.connect(toggle_line_numbers_file)
toggle_status_bar_action.triggered.connect(toggle_status_bar_file)  
toggle_tool_bar_action.triggered.connect(toggle_tool_bar_file)  
toggle_word_wrap_action.triggered.connect(toggle_word_wrap_file)
run_action.triggered.connect(run_file)  
run_selection_action.triggered.connect(run_selection_file)
run_configuration_action.triggered.connect(run_configuration_file)
about_action.triggered.connect(about_file)
help_action.triggered.connect(help_file)
update_action.triggered.connect(update)

# hotkeys
new_action.setShortcut('Ctrl+N')
open_action.setShortcut('Ctrl+O')
save_action.setShortcut('Ctrl+S')
save_as_action.setShortcut('Ctrl+Shift+S')
exit_action.setShortcut('Ctrl+Q')
undo_action.setShortcut('Ctrl+Z')
redo_action.setShortcut('Ctrl+Shift+Z')
cut_action.setShortcut('Ctrl+X')
copy_action.setShortcut('Ctrl+C')
paste_action.setShortcut('Ctrl+V')
find_action.setShortcut('Ctrl+F')
replace_action.setShortcut('Ctrl+H')
select_all_action.setShortcut('Ctrl+A')
zoom_in_action.setShortcut('Ctrl+Shift+=')
zoom_out_action.setShortcut('Ctrl+-')
toggle_fullscreen_action.setShortcut('F11')
toggle_line_numbers_action.setShortcut('Ctrl+Shift+L')
toggle_status_bar_action.setShortcut('Ctrl+Shift+S')
toggle_tool_bar_action.setShortcut('Ctrl+Shift+T')
toggle_word_wrap_action.setShortcut('Ctrl+Shift+W')





window.show()
sys.exit(app.exec())
