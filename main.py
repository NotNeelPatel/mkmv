import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt, QSize, QTimer
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

        #self.logoLabel = QLabel("mkmv")
        #layout.addWidget(self.logoLabel)
        toolbar = QToolBar("My main toolbar")
        self.addToolBar(toolbar)

        button_action = QAction("Your button", self)
        button_action.setStatusTip("This is your button")
        #button_action.triggered.connect(self.onMyToolBarButtonClick)
        toolbar.addAction(button_action)

        self.errorLabel = QLabel("Error")
        self.errorLabel.setProperty("class","error-label")
        self.errorLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.errorLabel.setVisible(False)
        self.errorLabel.setFixedHeight(40);
        layout.addWidget(self.errorLabel)

        self.inputFileLabel = QLabel("Drag and drop files here:")
        self.inputFileLabel.setProperty("class","drop-label")
        self.inputFileLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.inputFileLabel)

        makeVideoButton = QPushButton("make video")
        makeVideoButton.setProperty("class", "make-video-button")
        makeVideoButton.clicked.connect(self.button_clicked)
        layout.addWidget(makeVideoButton)

        layout.setSpacing(20)

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
            self.show_error("Error: File not Found:" + formatted)
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

            self.inputFileLabel.setText("Inputted Files:\n"+ "\n".join(self.files))
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
            self.inputFileLabel.setText("Drag and drop files here:")
            make_video(self.files, "output.mp4", "h264_nvenc")
            self.files = ["", ""]
        else:
            self.show_error("Error: Add one valid image/gif and one valid audio file")
            
        #print(self.files)

    def show_error(self, message):
        self.errorLabel.setText(message)
        self.errorLabel.setVisible(True)
        QTimer.singleShot(5000, self.hide_error)

    def hide_error(self):
        self.errorLabel.setVisible(False)

app = QApplication(sys.argv)
app.setStyleSheet("""
    QWidget {
        background-color: #242424;
        color: white;
    }

    .error-label{
        border-radius: 5px;
        background-color: #f23e30;
        color: white;
        margin: 0 20px 0 20px;
    }

    .drop-label{
        border: 2px dashed white; 
        border-radius: 15px;
        padding: 0px;
        margin: 10px 200px 0 200px;
        text-align: center;
    }

    .make-video-button{
        border: 2px solid white; 
        border-radius: 15px;
        padding: 20px 0 20px 0;
        margin: 0 200px 20px 200px;
    }

""")

window = MainWindow()
window.show()

app.exec()