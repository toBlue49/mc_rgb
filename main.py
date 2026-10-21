import sys;
import blocks;
import image_creator;
import video_splitter;
import os;
from PySide6 import QtCore, QtWidgets, QtGui;
from PIL import Image;
from colorama import Fore, Style;

rgb_blocks = blocks.generate_rgb_blocks(blocks.solid_blocks)

class VideoWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.FPS1 = 0
        self.FPS2 = 1
        self.FPS4 = 2
        self.FPS5 = 3
        self.FPS10 = 4
        self.FPS20 = 5
        
        self.video_path: str
        self.image_creator = image_creator.ImageCreator(rgb_blocks)
        self.vid_splitter = video_splitter.VideoSplitter("./out/temp")

        self.load_button = QtWidgets.QPushButton("Load Video File: (none)", self)
        self.load_button.clicked.connect(self.load_button_clicked)
        self.load_button.setToolTip("Select an Video File to convert")

        self.create_button = QtWidgets.QPushButton("Create Functions", self)
        self.create_button.clicked.connect(self.create_button_clicked)
        self.create_button.setToolTip("Creates the function files in ./out/mcfunction")

        self.namespace_text = QtWidgets.QLineEdit(parent=self)
        self.namespace_text.setText("my_namespace:the_folder/")
        self.namespace_text.setPlaceholderText("[Namespace]:[OPTIONAL: Folder]")
        self.namespace_text.setToolTip("[Namespace]:[OPTIONAL: Folder]. Basically the text before the function name")

        self.size_x_spinbox = QtWidgets.QSpinBox(self)
        self.size_x_spinbox.setMaximum(1280)
        self.size_x_spinbox.setValue(128)
        self.size_x_spinbox.setToolTip("[X] Video Width of the Video in blocks")

        self.size_y_spinbox = QtWidgets.QSpinBox(self)
        self.size_y_spinbox.setMaximum(720)
        self.size_y_spinbox.setValue(72)
        self.size_y_spinbox.setToolTip("[Y] Video Height of the Video in blocks")
        
        self.fps_label = QtWidgets.QLabel("Framerate:", self)

        self.fps_dropdown: QtWidgets.QComboBox = QtWidgets.QComboBox(self)
        self.fps_dropdown.addItem("1 FPS")
        self.fps_dropdown.addItem("2 FPS")
        self.fps_dropdown.addItem("4 FPS")
        self.fps_dropdown.addItem("5 FPS")
        self.fps_dropdown.addItem("10 FPS")
        self.fps_dropdown.addItem("20 FPS (not recommended)")
        self.fps_dropdown.setCurrentIndex(self.FPS5)
        self.fps_dropdown.setToolTip("Framerate of the video in game")

        self.radio_fill : QtWidgets.QRadioButton = QtWidgets.QRadioButton("/fill Method", self)
        self.radio_fill.setChecked(True)
        self.radio_fill.setToolTip("Uses /fill commands instead of only /setblock commands.")
        
        self.radio_skip : QtWidgets.QRadioButton = QtWidgets.QRadioButton("Skip Pixel Method", self)
        self.radio_skip.setToolTip("Uses the previous frame, to skip pixels which did not change.")

        self.radio_group = QtWidgets.QButtonGroup(self)
        self.radio_group.addButton(self.radio_fill)
        self.radio_group.addButton(self.radio_skip)

        self.help_button: QtWidgets.QPushButton = QtWidgets.QPushButton("?", self)
        self.help_button.setGeometry(10, 10, 25, 25)
        self.help_button.clicked.connect(self.help_button_clicked)

        self.setWindowTitle("Video Creator")

    def resizeEvent(self, event):
        self.load_button.setGeometry(50, 20, self.width()-50*2, 30)
        self.create_button.setGeometry(30, self.height()-30-20, self.width()-30*2, 30)
        self.namespace_text.setGeometry(50, 70, self.width()-50*2, 30)
        self.size_x_spinbox.setGeometry(50, 110, 0.5*self.width()-30*2, 30)
        self.size_y_spinbox.setGeometry(50 + 0.5*self.width()-20*2, 110, 0.5*self.width()-25*2, 30)
        self.fps_label.setGeometry(50, 150, 90, 30)
        self.fps_dropdown.setGeometry(50+100, 150, self.width()-95*2, 30)
        self.radio_fill.setGeometry(50, 180, 200, 30)
        self.radio_skip.setGeometry(50 + 0.5*self.width()-20*2, 180, 200, 30)

        return super().resizeEvent(event)

    @QtCore.Slot()
    def help_button_clicked(self):
        help_dialog = QtWidgets.QDialog()
        layout = QtWidgets.QVBoxLayout()

        message = QtWidgets.QLabel(
            "Video Creator Help\n\n" + 
            "Hover over the inputs to get more info.\n" +
            "The Output can be found in ./out/mcfunction. Copy the functions inside your functions folder you\n"
            "put in the Namespace/Folder Textfield. Run the tick function generated every tick at the position you want\n" +
            "the video to play. Use /scoreboard players set [videoname] video.frame 0 to start the video."
            )
        layout.addWidget(message)
        
        dlg_button = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok)
        dlg_button.accepted.connect(lambda: help_dialog.close())
        layout.addWidget(dlg_button)
        
        
        help_dialog.setWindowTitle("Help")
        help_dialog.setLayout(layout)
        help_dialog.exec()
    
    @QtCore.Slot()
    def load_button_clicked(self):
        filedialog = QtWidgets.QFileDialog
        dialog = filedialog(self)
        dialog.setFileMode(filedialog.FileMode.ExistingFile)
        dialog.setNameFilter("Video (*.mp4 *.webm *.mkv)")
        dialog.setViewMode(filedialog.Detail)
        filepath = ""
        if dialog.exec_():
            filepath = dialog.selectedFiles()[0]

        print(filepath)
        self.load_button.setText("Load Video File: " + os.path.basename(filepath))
        self.video_path = filepath

    def convert_to_fps(self, input: int) -> int:
        if input == self.FPS1:
            return 1
        if input == self.FPS2:
            return 2
        if input == self.FPS4:
            return 4
        if input == self.FPS5:
            return 5
        if input == self.FPS10:
            return 10
        if input == self.FPS20:
            return 20

    def clear_folder(self, path: str):
        files = os.listdir(path)
        for file in files:
            this_path = os.path.join(path, file)
            os.remove(this_path)
            print(Fore.YELLOW + "Deleted file " + file + Fore.RESET)
    
    @QtCore.Slot()
    def create_button_clicked(self):
        fps = self.convert_to_fps(self.fps_dropdown.currentIndex())
        video_name_no_ext = os.path.splitext(os.path.basename(self.video_path))[0]
        play_string = ""
        counter_multiplier = 20//fps
        namespace = self.namespace_text.text()
        method_convert = "" #Will contain the code

        self.clear_folder("./out/temp")
        self.clear_folder("./out/mcfunction")
        self.vid_splitter.split(self.video_path, (self.size_x_spinbox.value(), self.size_y_spinbox.value()), fps)

        #Image Method
        if self.radio_fill.isChecked(): #/fill Method
            method_convert = "self.image_creator.convert_image_smart(img, (self.size_x_spinbox.value(), self.size_y_spinbox.value()))"
            print(Fore.CYAN + "Image Method: /fill" + Fore.RESET)
        else: #Skip Pixels Method
            method_convert = "self.image_creator.convert_image_skip_pixels(img, (self.size_x_spinbox.value(), self.size_y_spinbox.value()), last_frame_img)"
            print(Fore.CYAN + "Image Method: Skip Pixels" + Fore.RESET)
        
        image_list = os.listdir("./out/temp")
        counter = 0
        last_frame_img: Image
        for image_file in image_list:
            img = Image.open(os.path.join("./out/temp", image_file))
            string = ""
            
            if (counter == 0):
                string = self.image_creator.convert_image(img, (self.size_x_spinbox.value(), self.size_y_spinbox.value()))
            else:
                string = eval(method_convert)
        
            file = open("./out/mcfunction/f" + str(counter) + ".mcfunction", "w")
            file.write(string)
            file.close()
        
            print(counter)
            play_string += f"execute if score {video_name_no_ext} video.frame matches {counter*counter_multiplier} run function {namespace}f{counter}\n"
            
            counter += 1
            last_frame_img = img

        play_string += f"scoreboard objectives add video.frame dummy\n"
        play_string += f"execute if score {video_name_no_ext} video.frame matches 0..{counter*counter_multiplier} run scoreboard players add {video_name_no_ext} video.frame 1\n"
        play_string += f"execute if score {video_name_no_ext} video.frame matches {counter*counter_multiplier+1}.. run scoreboard players set {video_name_no_ext} video.frame -1\n"
        
        final_file = open("./out/mcfunction/tick.mcfunction", "w")
        final_file.write(play_string)
        final_file.close()

        print(Fore.GREEN + "Done! Output in out/mcfunction" + Fore.RESET)

    def closeEvent(self, event):
        self.close()

class ImageWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.img: Image
        self.image_creator = image_creator.ImageCreator(rgb_blocks)
        
        self.load_button = QtWidgets.QPushButton("Load Image: (none)", self)
        self.load_button.clicked.connect(self.load_button_clicked)
        self.load_button.setToolTip("Select an Image File to convert")

        self.create_button = QtWidgets.QPushButton("Create Function", self)
        self.create_button.clicked.connect(self.create_button_clicked)
        self.create_button.setToolTip("Creates the function in ./out with the given name.")
        
        self.out_filename_text = QtWidgets.QLineEdit(parent=self)
        self.out_filename_text.setPlaceholderText("Filename here! (.mcfunction)")
        self.out_filename_text.setToolTip("The name of the output file without the file extension")

        self.size_x_spinbox = QtWidgets.QSpinBox(self)
        self.size_x_spinbox.setMaximum(1280)
        self.size_x_spinbox.setValue(256)
        self.size_x_spinbox.setToolTip("[X] Video Width of the Video in blocks")
        
        self.size_y_spinbox = QtWidgets.QSpinBox(self)
        self.size_y_spinbox.setMaximum(720)
        self.size_y_spinbox.setValue(144)
        self.size_y_spinbox.setToolTip("[Y] Video Height of the Video in blocks")

        self.help_button: QtWidgets.QPushButton = QtWidgets.QPushButton("?", self)
        self.help_button.setGeometry(10, 10, 25, 25)
        self.help_button.clicked.connect(self.help_button_clicked)

        self.setWindowTitle("Image Creator")

    @QtCore.Slot()
    def help_button_clicked(self):
        print(123)
        help_dialog = QtWidgets.QDialog()
        layout = QtWidgets.QVBoxLayout()

        message = QtWidgets.QLabel(
            "Image Creator Help\n\n" +
            "Hover over the inputs to get more info.\n" +
            "The Output can be found in ./out/. Put the function file into your datapack\n" +
            "and run it at the position the image should be spawned."
            )
        layout.addWidget(message)
        
        dlg_button = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok)
        dlg_button.accepted.connect(lambda: help_dialog.close())
        layout.addWidget(dlg_button)
        
        
        help_dialog.setWindowTitle("Help")
        help_dialog.setLayout(layout)
        help_dialog.exec()
    
    @QtCore.Slot()
    def load_button_clicked(self):
        filedialog = QtWidgets.QFileDialog
        dialog = filedialog(self)
        dialog.setFileMode(filedialog.FileMode.ExistingFile)
        dialog.setNameFilter("Images (*.png *.jpg *.webm)")
        dialog.setViewMode(filedialog.Detail)
        filepath = ""
        if dialog.exec_():
            filepath = dialog.selectedFiles()[0]

        print(filepath)
        self.load_button.setText("Load Image: " + os.path.basename(filepath))

        self.img = Image.open(filepath)

    @QtCore.Slot()
    def create_button_clicked(self):
        print("Started Image Creation")
        
        function = self.image_creator.convert_image(self.img, (self.size_x_spinbox.value(), self.size_y_spinbox.value()))

        file = open("./out/%s.mcfunction" % self.out_filename_text.text(), "w")
        file.write(function)
        file.close()

        print("Done!")

    def resizeEvent(self, event):
        self.load_button.setGeometry(50, 20, self.width()-50*2, 30)
        self.create_button.setGeometry(30, self.height()-30-20, self.width()-30*2, 30)
        self.out_filename_text.setGeometry(50, 70, self.width()-50*2, 20)
        self.size_x_spinbox.setGeometry(50, 100, 0.5*self.width()-30*2, 30)
        self.size_y_spinbox.setGeometry(50 + 0.5*self.width()-20*2, 100, 0.5*self.width()-25*2, 30)
        
        return super().resizeEvent(event)

    def closeEvent(self, event):
        self.close()

class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout: QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout()

        self.image_button = QtWidgets.QPushButton("Image to MC")
        self.layout.addWidget(self.image_button)
        self.image_button.clicked.connect(self.image_clicked)

        self.video_button = QtWidgets.QPushButton("Video to MC")
        self.layout.addWidget(self.video_button)
        self.video_button.clicked.connect(self.video_clicked)

        self.setLayout(self.layout)
        self.setWindowTitle("IMAGE/VIDEO to Minecraft")

    @QtCore.Slot()
    def image_clicked(self):
        print("Image Widget")
        self.img_widget = ImageWidget()
        self.img_widget.resize(400, 300)
        self.img_widget.show()

    @QtCore.Slot()
    def video_clicked(self):
        print("Video Widget")
        self.vid_widget = VideoWidget()
        self.vid_widget.resize(400, 300)
        self.vid_widget.show()
    

if __name__ == "__main__":
    
    app = QtWidgets.QApplication([])

    widget = MainWidget()
    widget.resize(350, 150)
    widget.show()

    sys.exit(app.exec())