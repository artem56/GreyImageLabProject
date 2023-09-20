from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog
from PyQt6 import uic, QtGui
from PyQt6.QtGui import QPixmap
from PIL import Image





class MyGui (QMainWindow):

    def __init__(self):
        super(MyGui, self).__init__()
        uic.loadUi("./GreyImageLab.ui",self)
        self.show()
        self.label.setMinimumSize(1,1)
        self.setCentralWidget(self.centralwidget)
        self.current_file = ""
        self.actionOpen_File.triggered.connect(self.open_file)
        self.radioButton_0.toggled.connect(self.toggleRadioButton)
        self.radioButton_1.toggled.connect(self.toggleRadioButton)
        self.radioButton_2.toggled.connect(self.toggleRadioButton)
        self.scrollAreaWidgetContents.setMouseTracking(True)

        #self.BeginTranslation.clicked.connect(self.Translate_Button)

    def mouseMoveEvent(self, e):
        x = int(e.position().x())
        y = int(e.position().y())
        X_coord = f'{x}'
        Y_coord = f'{y}'
        self.lineEdit_x_coordinate.setText(X_coord)
        self.lineEdit_y_coordinate.setText(Y_coord)

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", "", "File (*.mbv)")
        if filename != "":
            self.current_file = filename
            self.plainTextEdit_FileName.setPlainText(filename)
            #for b in self.readBytes(filename, 6):
            #    i = int.from_bytes(b, byteorder='little')
            #    print(f"raw({b}) - int({i}) - binary({bin(i)})")
            # Может меняться порядок байтов, но не битов в байтах!

            # Определяем сдвиг по radio_button
            if   (self.radioButton_0.isChecked()):
                shift = 0
            elif (self.radioButton_1.isChecked()):
                shift = 1
            elif (self.radioButton_2.isChecked()):
                shift = 2
            else:
                shift = 0

            with open(self.current_file, 'rb') as file:
                width = int.from_bytes(file.read(2),byteorder='little')
                heigth = int.from_bytes(file.read(2),byteorder='little')
                im = Image.new(mode="RGB", size=(width, heigth))
                #Color1 = int.from_bytes(file.read(2), byteorder='little') >> shift & 255
                #Color2 = int.from_bytes(file.read(2), byteorder='little') >> shift & 255
                #print(f"width = {width} heigth = {heigth}")
                #print(f"color1 = {Color1} color2 = {Color2}")
                for h in range(3000):
                    for w in range(500):
                        Color = int.from_bytes(file.read(2), byteorder='little') >> shift & 255
                        im.putpixel((w,h),(Color,Color,Color))
                im = im.convert("RGB")
                data = im.tobytes("raw", "RGB")
                qi = QtGui.QImage(data, im.size[0], im.size[1], im.size[0] * 3, QtGui.QImage.Format.Format_RGB888)
                pixmap = QPixmap.fromImage(qi)
                self.image_lable.setPixmap(pixmap)
                #im.show()
                file.close()

    def toggleRadioButton(self):


        if self.current_file != "":
            if (self.radioButton_0.isChecked()):
                shift = 0
            elif (self.radioButton_1.isChecked()):
                shift = 1
            elif (self.radioButton_2.isChecked()):
                shift = 2
            else:
                shift = 0

            with open(self.current_file, 'rb') as file:
                width = int.from_bytes(file.read(2), byteorder='little')
                heigth = int.from_bytes(file.read(2), byteorder='little')
                im = Image.new(mode="RGB", size=(width, heigth))
                for h in range(3000):
                    for w in range(500):
                        Color = int.from_bytes(file.read(2), byteorder='little') >> shift & 255
                        im.putpixel((w, h), (Color, Color, Color))
                im = im.convert("RGB")
                data = im.tobytes("raw", "RGB")
                qi = QtGui.QImage(data, im.size[0], im.size[1], im.size[0] * 3, QtGui.QImage.Format.Format_RGB888)
                pixmap = QPixmap.fromImage(qi)
                self.image_lable.setPixmap(pixmap)
                #im.show()
                file.close()





    # def readBytes(self,filename, nBytes):
    #     # rb - read in binary mode
    #     with open(filename, 'rb') as file:
    #         while True:
    #             byte = file.read(1)
    #             if byte:
    #                 yield byte
    #             else:
    #                 break
    #             if nBytes > 0:
    #                 nBytes -=1
    #                 if nBytes == 0:
                        # break


def main():
    app = QApplication([])
    window = MyGui()
    app.exec()


if __name__ == "__main__":
    main()
