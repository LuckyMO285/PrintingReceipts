import sys  # sys нужен для передачи argv в QApplication
import os  # Отсюда нам понадобятся методы для отображения содержимого директорий
import PyPDF2
from PIL import Image
import fitz
import os
import numpy as np
import shutil
import re
from natsort import natsorted, ns
import PIL.Image

from PyQt5 import QtCore, QtWidgets, QtGui, QtPrintSupport
from PIL import ImageQt
from PyQt5.QtCore import QRectF
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtCore import QFile, QIODevice

import design  # Это наш конвертированный файл дизайна

class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

        self.printer = QtPrintSupport.QPrinter()

        self.only_parsing_key = False

        self.delete_all_files_in_folder_key = False

        self.previous_path_for_pdf = '.'

        if os.path.exists('saveLabels/path.txt'):
            path_file = open('saveLabels/path.txt', 'r')
            self.previous_path_for_pdf = path_file.read()
            path_file.close()

        self.previous_path_for_png = '.'

        self.path_to_saveLabels_for_png = '.'
        
        self.btnBrowse.clicked.connect(self.start_func_open_pdf_file)  # Выполнить функцию open_pdf_file
                                                            # при нажатии кнопки
        self.parsingButton.clicked.connect(self.start_func_open_pdf_file_in_only_parsing_mode)

        self.chooseButton.clicked.connect(self.open_png_files)

    def start_func_open_pdf_file_in_only_parsing_mode(self):
        self.only_parsing_key = True
        self.open_pdf_file()

    def start_func_open_pdf_file(self):
        self.only_parsing_key = False
        self.delete_all_files_in_folder_key = True
        self.open_pdf_file()

    def open_png_files(self):
        if not os.path.exists(self.previous_path_for_png):
            self.previous_path_for_png = self.path_to_saveLabels_for_png
        if not os.path.exists(self.previous_path_for_png):
            self.previous_path_for_png = '.'
        dialog = QtWidgets.QFileDialog
        filenames, _filter = dialog.getOpenFileNames(self, "Open Files", self.previous_path_for_png, 'PNG (*.png)') #открытие файла с разрешение .png
        if len(filenames) > 0:
            self.delete_all_files_in_folder_key = False
            l = filenames[0].rsplit('/', 1)[:-1]
            l.append('/')
            folder_name= ''.join(l)
            self.previous_path_for_png = folder_name
            self.path_to_saveLabels_for_png = sys.argv[0].rsplit('\\', 1)[0] + '\\saveLabels\\'
            self.handlePrint(filenames, folder_name)

    def open_pdf_file(self):
        #if not os.path.exists(self.previous_path_for_pdf):
            #self.previous_path_for_pdf = '.'
        dialog = QtWidgets.QFileDialog
        filename, _filter = dialog.getOpenFileName(self, "Open File", self.previous_path_for_pdf, 'PDF (*.pdf)') #открытие файла с разрешение .pdf
        if len(filename) > 0:
            l = filename.rsplit('/', 1)[:-1]
            l.append('/')
            folder_name= ''.join(l)
            self.previous_path_for_pdf = folder_name
            
            self.make_png_files(filename) #запуск функции для парсинга картинок из файла .pdf с передачей пути до этого файла

    def make_png_files(self, filename):
        doc = fitz.open(filename)
        if not os.path.exists(sys.argv[0].rsplit('\\', 1)[0] + '\\saveLabels\\'): #создание папки save рядом с исполняемым файлом
            os.mkdir(sys.argv[0].rsplit('\\', 1)[0] + '\\saveLabels\\')
        if not os.path.exists(sys.argv[0].rsplit('\\', 1)[0] + '\\saveLabels\\' + (filename.rsplit('/', 1)[-1]).rsplit('.', 1)[0]): #создание папки с названием файла .pdf
            os.mkdir(sys.argv[0].rsplit('\\', 1)[0] + '\\saveLabels\\' + (filename.rsplit('/', 1)[-1]).rsplit('.', 1)[0])

        path_file = open('saveLabels/path.txt', 'w')    #сохранение пути в файл path.txt размещено здесь, так как после этого случая гарантировано создается файл saveLabels
        path_file.write(self.previous_path_for_pdf)
        path_file.close()
            
        filenames_list = [] #хранит путь до всех сгенерированных картинок
        folder_name = sys.argv[0].rsplit('\\', 1)[0] + '\\saveLabels\\' + (filename.rsplit('/', 1)[-1]).rsplit('.', 1)[0] + '\\'
        
        img_list = [] #лист, хранящие все изображения из pdf
        for i in range(len(doc)):
            temp_list = [] #лист, хранящий изображения с одной страницы из pdf
            list_of_image_names = [] #лист, хранящий названия изображений на странице
            for img in doc.getPageImageList(i):
                temp_list.append(img)
                list_of_image_names.append(img[7])
            list_of_image_names = natsorted(list_of_image_names) #естественная сортировка названий файлов
            for j in range(len(list_of_image_names)):
                for k in range(len(temp_list)):
                    if list_of_image_names[j] == temp_list[k][7]:
                        img_list.append(temp_list[k])

            
        for i in range(len(img_list)):
            xref = img_list[i][0]
            pix = fitz.Pixmap(doc, xref)
            rgb = "RGB" 
            img = Image.frombuffer(rgb, [pix.width, pix.height], pix.samples,
                       "raw", rgb, 0, 1)
                
            filenames_list.append(sys.argv[0].rsplit('\\', 1)[0] + '\\saveLabels\\' + (filename.rsplit('/', 1)[-1]).rsplit('.', 1)[0] + '\\' +
                                  (filename.rsplit('/', 1)[-1]).rsplit('.', 1)[0] + "p%s-%s.png" % (i, xref)) #узнаем расположение текущего файла, после берем путь до папки, в которой он
                                                                                                        #находится; создаем папку save; берем название файла pdf, обрезая его формат; делаем новое название для файла   
            pix.writePNG(filenames_list[-1])   
            pix = None
        if self.only_parsing_key == False:
            self.handlePrint(filenames_list, folder_name)

    def handlePrint(self, filenames_list, folder_name):
        dialog = QtPrintSupport.QPrintDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            painter = QtGui.QPainter()
            self.printer = dialog.printer()
            self.printer.setResolution(360)
            #self.printer.setOutputFileName("resultOfProgramm.pdf")
            painter.begin(self.printer)
            for i in range(len(filenames_list)):
                pixMap = QPixmap(filenames_list[i])
                pixMap = pixMap.scaled(self.printer.width(), self.printer.height(), aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode = QtCore.Qt.SmoothTransformation) 
                painter.drawPixmap(0, 0, pixMap)
                if i != len(filenames_list) - 1:
                    self.printer.newPage()
            painter.end()
            if self.delete_all_files_in_folder_key == True:
                self.deleteAllImages(folder_name)
            else:
                self.deleteFewImages(filenames_list)

    def deleteAllImages(self, folder_name):
        if self.checkBox.isChecked():
            shutil.rmtree(folder_name)

    def deleteFewImages(self, filenames_list):
        if self.checkBox.isChecked():
            for i in range(len(filenames_list)):
                os.remove(filenames_list[i])
        
def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
