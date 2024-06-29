import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from video_maker import make_video
import os

ACCEPTED_IMG = ["gif","jpg", "jpeg", "png"]
ACCEPTED_AUDIO = ["mp3", "wav", "flac"]


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.setAcceptDrops(True)
        self.setWindowTitle("mkmv")
        layout = QVBoxLayout()

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.logoLabel = QLabel("mkmv")
        layout.addWidget(self.logoLabel)

        self.inputFileLabel = QLabel("Drag and drop files here:")
        layout.addWidget(self.inputFileLabel)

        makeVideoButton = QPushButton("make video")
        makeVideoButton.clicked.connect(self.button_clicked)
        layout.addWidget(makeVideoButton)

        self.files = ["", ""]


    def validate_file(self, unformatted_file):
        # Sometimes the input file is "", this filters it out
        if len(unformatted_file) <= 2:
            return None
        
        input_file = unformatted_file.split("\r")[0]

        extension = (input_file.split(".")[-1]).strip()
        if not(extension in ACCEPTED_IMG or extension in ACCEPTED_AUDIO):
            return None

        formatted = input_file.split("file:///")[-1].strip()

        if sys.platform.startswith('linux'):
            formatted = "/" + formatted
        
        if not os.path.exists(formatted):
            print("Error: File not Found:", formatted)
            return None
        print(formatted)
        return formatted
    
    def update_file_list(self, input_file, locked_in):
        extension = (input_file.split(".")[-1]).strip()
        if extension in ACCEPTED_IMG and not locked_in[0]:
            self.files[0] = input_file
            locked_in[0] = True
        elif extension in ACCEPTED_AUDIO and not locked_in[1]:
            self.files[1] = input_file
            locked_in[1] = True
        else:
            print("FAIL LOCKED IN")

        return locked_in

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        input_files = e.mimeData().text().split("\n")
        print(input_files)
        count = 0
        locked_in = [False, False]
        while(count < len(input_files)):
            print(count)

            input_file = self.validate_file(input_files[count])

            if(input_file != None):
                locked_in = self.update_file_list(input_file, locked_in)
                print(input_file, locked_in)
            else:
                "FAIL input file none"

            self.inputFileLabel.setText("Inputted Files"+ "".join(self.files))
            count += 1

    def button_clicked(self):
        self.mk_video()
        """
        dlg = QDialog(self)
        dlg.setWindowTitle("Make Video")
        dlg.resize(300, 500)

        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.mk_video)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("There will be options here")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

        dlg.exec()
        """

    def mk_video(self):
        if(self.files[0] != "" and self.files[1] != ""):
            # TODO: Change the h264 codec later for prod
            make_video(self.files, "output.mp4", "h264_nvenc")
            self.files = ["", ""]
        else:
            print("need to input an image and an audio")
        #print(self.files)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()