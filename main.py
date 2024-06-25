import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from video_maker import make_video

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

        self.inputFileLabel = QLabel("Inputted Files:")
        layout.addWidget(self.inputFileLabel)

        makeVideoButton = QPushButton("make video")
        makeVideoButton.clicked.connect(self.button_clicked)
        layout.addWidget(makeVideoButton)

        self.files = []


    def dragEnterEvent(self, e):
        # Would use mimetypes but they are inconsistent with Linux file managers
        accepted = ["gif","jpg", "jpeg", "png", "mp3", "wav", "flac"]
        # Whitespace and whatnot are also inconsistent, hopefully this handles most file managers
        extension = ((e.mimeData().text()).split(".")[-1]).strip()
        print(extension, len(extension), extension == "jpg", extension == "png")
        if extension in accepted:
            e.accept()
        else:
            e.ignore()
            print(f"Invalid file path .{extension}, accepted are: {accepted}")

    def dropEvent(self, e):
        print("Dropped:", e.mimeData().text())
        #inputFileLabel.setText("")
        self.files += [e.mimeData().text()]
        self.inputFileLabel.setText("Inputted Files"+ "".join(self.files))
        

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
        make_video(self.files[0], self.files[1], "output.mp4")
        self.files = []
        #print(self.files)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()