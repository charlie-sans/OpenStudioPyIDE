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
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit
#setup varibalbes
config_file = 'config.ini'




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
        background = configparser['DEFAULT']['project']
        color = configparser['DEFAULT']['project']
        theme = configparser['DEFAULT']['project']
        font = configparser['DEFAULT']['project']
        font_size = configparser['DEFAULT']['project']
    else:
        background = 'white'
        color = 'black'
        theme = 'light'
        font = 'Arial'
        font_size = '12'

except Exception as e:
    logging.error('Error: {e}'.format(e))
    print('Error: {e}'.format(e))
    sys.exit(1)
# setup main window without using classes

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









window.show()
sys.exit(app.exec())
