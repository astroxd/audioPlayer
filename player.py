from sputofy import Ui_MainWindow
import sys, os, random

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QStyle
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QUrl




class Window(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        #create media player object
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
 
 
       
 
       

        #open button
        self.actionOpen_File.triggered.connect(self.open_file)
        self.actionOpen_Folder.triggered.connect(self.open_folder)
 
 
        #create button for playing
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)

        #playlist button
        self.nextBtn.clicked.connect(self.next)
        # self.nextBtn.setIcon(self.style().standardIcon(QStyle.SP_))
        
        self.prevBtn.clicked.connect(self.previous)
        # self.prevBtn.setIcon(self.style().standardIcon(QStyle.SP_))
        self.shuffleBtn.clicked.connect(self.shuffle)
 
 
 
        #create slider
        self.durationSlider.sliderMoved.connect(self.set_position)
 
 
 
        
        # volumeSlider
        self.volumeSlider.setProperty("value", 100)

        # volumeBtn
        self.volumeBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
        self.volumeBtn.clicked.connect(self.volumeToggle)
        self.i_volume = 0
        

        #media player signals
 
        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)
        # self.volumeSlider.valueChanged.connect(self.mediaPlayer.setVolume)
        self.volumeSlider.valueChanged.connect(self.setVolume)   

        self.mediaPlayer.durationChanged.connect(self.update_duration)
        self.mediaPlayer.positionChanged.connect(self.update_time_remaining)
        self.durationSlider.valueChanged.connect(self.mediaPlayer.setPosition) 

    
        
        
        
        
        
        # create the playlist (mettila dentro la funzione open folder )
        self.playlist =  QMediaPlaylist()
        self.playlist.setPlaybackMode(2)
        self.mediaPlayer.setPlaylist(self.playlist)

        self.loopBtn.clicked.connect(self.loop)
        
        

    def next(self):
        self.playlist.next()

    def previous(self):
        self.playlist.previous()

    
    # TODO
    def shuffle(self):
        self.playlist.setPlaybackMode(4)
    
    def loop(self):
        self.playlist.setPlaybackMode(3)
        

            








    def open_folder(self):
        foldername = QFileDialog.getExistingDirectory(self, "open folder", "c:\\")
        self.max_songs = 0 #TODO
        
        for song in os.listdir(foldername):
            self.playlist.addMedia(QMediaContent(QUrl(f"{foldername}/{song}")))
            self.textBrowser.append(song.replace(".mp3", ""))
            self.max_songs+1
        self.playlist.setCurrentIndex(0)
        # self.playlist.setPlaybackMode(2)
        self.playBtn.setEnabled(True)
        

        

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")
 
        if filename != '':
            self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn.setEnabled(True)
            
            
 
    
    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
 
        else:
            self.mediaPlayer.play()
 
 
    def mediastate_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
 
        else:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
 
    def position_changed(self, position):
        self.durationSlider.setValue(position)
 
 
    def duration_changed(self, duration):
        self.durationSlider.setRange(0, duration)
 
 
    def set_position(self, position):
        self.mediaPlayer.setPosition(position)
 
    
    def hhmmss(self, ms):
        # s = 1000
        # m = 60000
        # h = 360000
        # h, r = divmod(ms, 36000)
        # m, r = divmod(r, 60000)
        # s, _ = divmod(r, 1000)

        s = (ms/1000) % 60
        m = (ms/60000) % 60
        h = (ms/3600000) % 24
        if ms >= 3600000:
            return("%d:%02d:%02d" % (h,m,s))
        else:
            return("%d:%02d" % (m,s))

    def update_duration(self, duration):
        print(duration)
        if duration >= 0:
            self.total_timeLabel.setText(self.hhmmss(duration))

    def update_time_remaining(self, position):
        if position >= 0:
            self.time_remainingLabel.setText(self.hhmmss(position))

        # Disable the events to prevent updating triggering a setPosition event (can cause stuttering).
        self.durationSlider.blockSignals(True)
        self.durationSlider.setValue(position)
        self.durationSlider.blockSignals(False)
    
    
    def volumeToggle(self):
        if self.i_volume == 0:
            self.mediaPlayer.setVolume(0)
            self.volumeBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaVolumeMuted))
            self.i_volume = 1
        elif self.i_volume == 1:
            if self.volumeSlider.value() == 0:
                self.volumeSlider.setValue(10)
                self.volumeBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
            else:
                self.mediaPlayer.setVolume(self.volumeSlider.value())
                self.volumeBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
            self.i_volume = 0
    

    def setVolume(self):
        self.mediaPlayer.setVolume(self.volumeSlider.value())
        if self.volumeSlider.value() == 0:
            self.i_volume = 0
            self.volumeToggle()
        else:
            self.i_volume = 0
            self.volumeBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))

 
        
 
        



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")

    window = Window()
    window.show()

    sys.exit(app.exec_())
