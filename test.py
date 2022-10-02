from logging import exception
from operator import le
import sys
from PyQt5.QtGui import QDoubleValidator, QIntValidator, QValidator
from PyQt5.QtCore import QDate
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QCompleter, QComboBox
from PyQt5.QtWidgets import QMainWindow
from matplotlib.backend_bases import cursors
from matplotlib.style import use
from database import mysqlDB
from main_UI import Ui_main_view

cursor = mysqlDB()

l = [1,2,3,4]

print(1 not in l)