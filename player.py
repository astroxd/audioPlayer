
from __future__ import unicode_literals

import datetime  # in teoria l'ho rimosso creando la funzione time_format()#TODO
import os
import random
import sys

from functools import partial


import yaml
import youtube_dl
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QAbstractListModel, Qt, QTimer, QUrl
from PyQt5.QtGui import QIcon, QPixmap, QKeySequence, QPalette, QColor
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimedia import (QMediaContent, QMediaPlayer,
                                QMediaPlayerControl, QMediaPlaylist)
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtWidgets import (QFileDialog, QHBoxLayout, QLineEdit, QMainWindow,
                             QPushButton, QStyle, QVBoxLayout, QShortcut, QInputDialog)


from playlistNameWindow import Ui_playlistNameWindow
from SecondWindow import Ui_Dialog
from sputofy import Ui_MainWindow

base_path = os.path.split(os.path.abspath(__file__))[0]
res_path = f"{base_path}\\res"



def time_format(seconds): # format seconds into hh:mm:ss
    mm, ss = divmod(seconds, 60)
    hh, mm = divmod(mm, 60)
    if seconds >= 3600:
        s = "%d:%02d:%02d" % (hh, mm, ss)
    else:
        s = "%d:%02d" % (mm, ss)
    
    return s

def yaml_loader(): # load config
    with open(os.path.join(base_path, "config.yaml"), "r") as config:
        data = yaml.load(config, Loader=yaml.FullLoader)
        return data

def yaml_dump(data): # rewrite config
    with open(os.path.join(base_path, "config.yaml"), "w") as config:
        yaml.dump(data, config)

class config():
    def __init__(self, height, width):
        
        self.height = height
        self.width = width
        self.data = yaml_loader()
        self.default_folder()
        self.last_window_size()

    def default_folder(self):
        user = os.getlogin()
        default_folderConfig = {
            "default_folder": "C:\\Users\\"+user+"\\Desktop\\sputofy_songs"}
        yaml_dump(default_folderConfig)

    def last_window_size(self):
        self.data['last_window_size']['width'] = self.width
        self.data['last_window_size']['heigth'] = self.height
        yaml_dump(self.data)  # TODO è gia nella main window

class PlaylistModel(QAbstractListModel):
    def __init__(self, playlist, *args, **kwargs):
        super(PlaylistModel, self).__init__(*args, **kwargs)
        self.playlist = playlist

    def data(self, index, role):
        if role == Qt.DisplayRole:
            media = self.playlist.media(index.row())
            song = media.canonicalUrl().fileName().replace(".mp3","")
            songPosition = f"#{index.row()+1}    {song}"
            # return media.canonicalUrl().fileName().replace(".mp3", "")
            return songPosition

    def rowCount(self, index):
        return self.playlist.mediaCount()



class SecondWindow(QtWidgets.QWidget, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.startBtn.clicked.connect(self.startDownload)
        self.download_folderBtn.clicked.connect(self.openDownloadFolder)

    def mostra(self):
        self.show()
        

    def openDownloadFolder(self):
        downloadFolderName = QFileDialog.getExistingDirectory(
            self, "open folder", "c:\\")
        self.download_folder.setText(downloadFolderName)

    def startDownload(self):  
        YTlink = self.youtube_link.text()

        if self.download_folder.text() != "":
            download_folder = self.download_folder.text()
        else:
            try:
                download_folder = yaml_loader()['default_folder']
                os.makedirs(download_folder)
            except:
                download_folder = yaml_loader()['default_folder']
                print(f"\x1b[1;34;40mfolder already existing : {download_folder}\x1b[0;37;40m")
        
        # array with conversion options
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': download_folder+'/%(title)s.%(ext)s',

        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([YTlink])
                
            except:
                print("insert a valid url")

            Window().statusbar.showMessage("ciao")#TODO 
            self.youtube_link.setText("")#TODO 
            self.close()
            # gettin id and title of song(don't need)
            # info_dict = ydl.extract_info(YTlink)
            # video_id = info_dict.get("id", None)
            # video_title = info_dict.get('title', None)

class Window(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        # load config
        self.data = yaml_loader()

        # load ui
        self.setupUi(self)
        
        self.setWindowTitle("Sputofy")
        self.setWindowIcon(QIcon(os.path.join(res_path, "logo.svg")))

        # "libary"
        self.xCor = self.data['last_position']['xPos']
        self.yCor = self.data['last_position']['yPos']
        self.widthSize = self.data['last_window_size']['width']
        self.heightSize = self.data['last_window_size']['heigth']

        self.setGeometry(self.xCor, self.yCor, self.widthSize,self.heightSize)
        
        # load secondWindow
        self.secondWindow = SecondWindow()
        

        self.statusbar.showMessage("ciao")#TODO
    
        
        
        # open secondWindow using button
        self.actionOpenSecondWindow.triggered.connect(self.secondWindow.mostra)

        #===========================  mediaplayer  ==============================
        
        # create media player object
        # self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer = QMediaPlayer(None)


        
        # open button
        self.actionOpen_File.triggered.connect(self.open_file)
        self.actionOpen_Folder.triggered.connect(self.open_folder)

        

        # play button
        self.playBtn.setEnabled(False)
        self.playBtn.clicked.connect(self.play_video)# when btn is pressed: if it is playing it pause and change icon, if it is paused it play and change icon
        QShortcut('Space', self, lambda:self.play_video())
        # QShortcut(QKeySequence("Space"), self).activated.connect(self.play_video)metodo da ricordare in caso di problemi #TODO

        
        
        

        
        
        # duration slider
        self.durationSlider.setEnabled(False)
        self.durationSliderMaxValue = 0
        self.durationSlider.valueChanged.connect(self.mediaPlayer.setPosition)# set mediaPlayer position using the value took from the slider
        QShortcut('Right', self, lambda:self.durationSlider.setValue(self.durationSlider.value()+10000))# 1s = 1000ms
        QShortcut('Left', self, lambda:self.durationSlider.setValue(self.durationSlider.value()-10000))# 1s = 1000ms


        QShortcut('Shift+Right', self, lambda:self.durationSlider.setValue(self.durationSliderMaxValue-1000))
        QShortcut('Shift+Left', self, lambda:self.durationSlider.setValue(0))

        
        # volumeSlider
        self.volumeSlider.setProperty("value", 100)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setValue(self.data['volume'] if self.data['volume']!=0 else self.data['volume']+1)
        self.volumeLabel.setText(f"{self.data['volume']}%" if self.data['volume']!=0 else f"{self.data['volume']+1}%")
        self.volumeSlider.valueChanged.connect(self.mediaPlayer.setVolume)# set mediaPlayer volume using the value took from the slider
        
        QShortcut('Up', self, lambda:self.volumeSlider.setValue(self.volumeSlider.value()+1))
        QShortcut('Down', self, lambda:self.volumeSlider.setValue(self.volumeSlider.value()-1))

        QShortcut('Shift+Up', self, lambda:self.volumeSlider.setValue(100))
        QShortcut('Shift+Down', self, lambda:self.volumeSlider.setValue(0))


        

        # volumeBtn
        
        self.volumeBtn.clicked.connect(self.volumeToggle)
        self.isMuted = False
        self.previousVolume = self.data['volume']

        QShortcut('M', self, lambda:self.volumeToggle())



        # media player signals
        self.mediaPlayer.durationChanged.connect(self.duration_changed)  # set range of duration slider
        self.mediaPlayer.positionChanged.connect(self.position_changed)  # duration slider progress
        self.mediaPlayer.stateChanged.connect(self.player_state)# see when it's playing or in pause 
        self.mediaPlayer.volumeChanged.connect(self.volumeIcon)# change volumebtn icon
        
        #===========================  playlist  ==============================
        
        # create the playlist
        self.playlist = QMediaPlaylist()
        self.playlist.setPlaybackMode(2)
        self.mediaPlayer.setPlaylist(self.playlist)

        # clear the playlist
        self.playlistIsEmpty = True

        # non so perché ma va model
        self.model = PlaylistModel(self.playlist)
        self.playlistView.setModel(self.model)
        self.playlist.currentIndexChanged.connect(self.playlist_position_changed)
        selection_model = self.playlistView.selectionModel()
        selection_model.selectionChanged.connect(self.playlist_selection_changed)
        
        
        #===========================  playlist function  ==============================
        
        self.mediaList = []# array of loaded songs
        self.currentPlaylist = ""# current loaded playlist name
        self.isCustomPlaylist = False

        # add song name on title
        self.playlist.mediaChanged.connect(partial(self.setTitle, 0))
        
        
        # playlist button
        self.nextBtn.clicked.connect(self.playlist.next)# seek track forward
        QShortcut('D', self, lambda:self.playlist.next())

        self.prevBtn.clicked.connect(self.playlist.previous)# seek track backward
        QShortcut('A', self, lambda:self.playlist.previous())        

        
        self.mediaPlayer.mediaStatusChanged.connect(self.autoNextTrack)# once song is ended seek track forward and play it
                                                                         

        self.actionLoopIt.triggered.connect(self.loopSong)# (1) loop the same song
        
        self.loopBtn.clicked.connect(self.loop)# (3) loop the playlist  
        QShortcut('L', self, lambda:self.loop())
        
        self.randomBtn.clicked.connect(self.random)# (4) play random song without end
        QShortcut('R', self, lambda:self.random())
        
        # load playlist
        self.actionPlaylist1.triggered.connect(partial(self.load_playlist, 1))
        self.actionPlaylist1.setText(self.data['playlist1Name'])# load with the new playlist name
        
        self.actionPlaylist2.triggered.connect(partial(self.load_playlist, 2))
        self.actionPlaylist2.setText(self.data['playlist2Name'])# load with the new playlist name
        
        self.actionPlaylist3.triggered.connect(partial(self.load_playlist, 3))
        self.actionPlaylist3.setText(self.data['playlist3Name'])# load with the new playlist name

        # save playlist
        self.playlist1Btn.clicked.connect(partial(self.custom_playlist, 1))
        self.playlist2Btn.clicked.connect(partial(self.custom_playlist, 2))
        self.playlist3Btn.clicked.connect(partial(self.custom_playlist, 3))

        # when you save a playlist chose its name
        self.playlist1Btn.clicked.connect(partial(self.setPlaylistName, 1))
        self.playlist2Btn.clicked.connect(partial(self.setPlaylistName, 2))
        self.playlist3Btn.clicked.connect(partial(self.setPlaylistName, 3))

        # delete current playlist
        self.actionDeletePlaylist.triggered.connect(self.delete_playlist)


    

    
        


    

            
    
       
        
        
   

#================== Songs opening ==================#
    
    def open_folder(self):
        foldername = QFileDialog.getExistingDirectory(self, "Open folder", "c:\\")

        if foldername != '':
            self.playlist.clear()
            self.mediaList = []
            for song in os.listdir(foldername):
                media = f"{foldername}/{song}"
                self.playlist.addMedia(QMediaContent(QUrl(media)))
                self.mediaList.append(media)
                
            
            self.playlist.setCurrentIndex(0)

            self.playBtn.setEnabled(True)
            self.durationSlider.setEnabled(True)
            self.playlistIsEmpty = False

            self.isCustomPlaylist = False
            self.model.layoutChanged.emit()
            self.setTitle(0)

            # adjust play/pause icon
            self.mediaPlayer.pause()

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Song", "c:\\")

        if filename != '':
            if self.playlistIsEmpty == False:
                self.playlist.clear()
                self.mediaList = []
                self.playlistIsEmpty = True
            self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.mediaList.append(filename)

            self.playBtn.setEnabled(True)
            self.durationSlider.setEnabled(True)

            self.isCustomPlaylist = False
            self.model.layoutChanged.emit()
            self.setTitle(0)
            
            # adjust play/pause icon
            if self.playlist.mediaCount() == 1:
                self.playlist.setCurrentIndex(0)
                self.mediaPlayer.pause()
            

    def load_playlist(self, i):
        self.playlist.clear()
        self.mediaList.clear()
        #reload config
        self.data = yaml_loader()
        
        for song in self.data['playlist'+str(i)]:
            self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(song)))
            self.mediaList.append(song)
       
        
        
                
        self.playlist.setCurrentIndex(0)

        self.playBtn.setEnabled(True)
        self.durationSlider.setEnabled(True)
        self.playlistIsEmpty = False

        self.isCustomPlaylist = True    
        self.model.layoutChanged.emit()
        self.setTitle(i)

        # adjust play/pause icon
        self.mediaPlayer.pause()

        self.currentPlaylist = f'playlist{i}'
        
    
    def setTitle(self, i):
        if self.isCustomPlaylist == False:
            self.setWindowTitle(f"Sputofy - {self.playlist.currentMedia().canonicalUrl().fileName()} - {self.playlist.currentIndex()+1}/{self.playlist.mediaCount()}")
        else:
            if i != 0: 
                self.setWindowTitle(f"Sputofy - {self.data['playlist'+str(i)+'Name']} - {self.playlist.currentMedia().canonicalUrl().fileName()} - {self.playlist.currentIndex()+1}/{self.playlist.mediaCount()}")
#=======================================================# 


#================== Player Functions ==================#
    
    def play_video(self):
        if not self.durationSlider.isEnabled() == False: 
            if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
                self.mediaPlayer.pause()
            
            else:
                self.mediaPlayer.play()

    def duration_changed(self, duration):
        self.durationSlider.setRange(0, duration)
        if duration >= 0:
            self.total_timeLabel.setText(time_format(round(duration/1000)))
        self.durationSliderMaxValue = duration

    def position_changed(self, position):
        if position >= 0:
            self.time_remainingLabel.setText(time_format((position/1000)))
        # Disable the events to prevent updating triggering a setPosition event (can cause stuttering).
        
        self.durationSlider.blockSignals(True)
        self.durationSlider.setValue(position)
        self.durationSlider.blockSignals(False)

#=======================================================# 


#================== Playlist Settings ==================#
    #TODO useless
    def playlist_list(self):
        index = self.playlist.mediaCount()
        list = []
        for i in range(index):
            print(self.playlist.media(i).canonicalUrl().fileName())
            list.append(self.playlist.media(i).canonicalUrl().fileName())
        return list

    def custom_playlist(self, i):
        if not self.playlist.mediaCount() == 0:
            self.data['playlist'+str(i)] = self.mediaList
            yaml_dump(self.data)

        else:
            self.statusbar.showMessage("can't save an empty playlist")

    def setPlaylistName(self, i):
        if self.playlist.mediaCount() != 0:
            playlistName, is_notEmpty = QInputDialog.getText(self, "playlist", f"save {self.data['playlist'+str(i)+'Name']} as:")
            
            if playlistName != "":
                if i == 1:
                    self.actionPlaylist1.setText(playlistName)
                    self.data['playlist1Name'] = playlistName
                elif i == 2:
                    self.actionPlaylist2.setText(playlistName)
                    self.data['playlist2Name'] = playlistName
                elif i == 3:
                    self.actionPlaylist3.setText(playlistName)
                    self.data['playlist3Name'] = playlistName

                
            else:
                if i == 1:
                    self.actionPlaylist1.setText(self.data['playlist1Name'])
                elif i == 2:
                    self.actionPlaylist2.setText(self.data['playlist2Name'])
                elif i == 3:
                    self.actionPlaylist3.setText(self.data['playlist3Name'])
            
            yaml_dump(self.data)

    def delete_playlist(self):
        if not self.currentPlaylist == "":
            self.data[self.currentPlaylist] = []
            yaml_dump(self.data)
        else:
            self.statusbar.showMessage("can't delete a non custom playlist")

    def playlist_position_changed(self, i):
        if i > -1:
            ix = self.model.index(i)
            self.playlistView.setCurrentIndex(ix)

    def playlist_selection_changed(self, ix):
        # We receive a QItemSelection from selectionChanged.
        i = ix.indexes()[0].row()
        self.playlist.setCurrentIndex(i)
        self.mediaPlayer.play()

#=======================================================#


#================== Playback Settings ==================#    
    
    def loopSong(self):
        if self.playlist.playbackMode() != 1:

            self.playlist.setPlaybackMode(1)

            self.actionLoopIt.setText("Loop it: ON")
            self.loopBtn.setIcon(QIcon(os.path.join(res_path, "loopIconOFF.svg")))
            self.randomBtn.setIcon(QIcon(os.path.join(res_path, "randomIconOFF.svg")))
        else:
            self.playlist.setPlaybackMode(2)
            self.actionLoopIt.setText("Loop it: OFF")
    
    def loop(self):
        if self.playlist.playbackMode() != 3:
            self.playlist.setPlaybackMode(3)

            self.loopBtn.setIcon(QIcon(os.path.join(res_path, "loopIconON.svg")))
            self.randomBtn.setIcon(QIcon(os.path.join(res_path, "randomIconOFF.svg")))
            self.actionLoopIt.setText("Loop it: OFF")

        else:
            self.playlist.setPlaybackMode(2)
            self.loopBtn.setIcon(QIcon(os.path.join(res_path, "loopIconOFF.svg")))
            
    def random(self):
        if self.playlist.playbackMode() != 4:
            self.playlist.setPlaybackMode(4)

            self.randomBtn.setIcon(QIcon(os.path.join(res_path, "randomIconON.svg")))
            self.loopBtn.setIcon(QIcon(os.path.join(res_path, "loopIconOFF.svg")))
            self.actionLoopIt.setText("Loop it: OFF")

        else:
            self.playlist.setPlaybackMode(2)
            self.randomBtn.setIcon(QIcon(os.path.join(res_path, "randomIconOFF.svg")))
            
    def autoNextTrack(self):
        
        if self.mediaPlayer.mediaStatus() == QMediaPlayer.EndOfMedia:
            if self.playlist.playbackMode() == 2:
                # index starts from 0       mediacount starts from 1
                if self.playlist.currentIndex() != self.playlist.mediaCount()-1:
                    self.playlist.next()
                    self.mediaPlayer.play()
                else:
                    self.playlist.setCurrentIndex(0)
                    self.mediaPlayer.pause()

            # loop playlist
            elif self.playlist.playbackMode() == 3:
                self.playlist.next()
                self.mediaPlayer.play()
            
            # random song
            elif self.playlist.playbackMode() == 4:
                while self.playlist.previousIndex() == self.playlist.currentIndex():
                    self.playlist.setCurrentIndex(random.randint(0, self.playlist.mediaCount()-1))

#=======================================================#               
    

#================== Volume Settings ==================#     
    
    def volumeIcon(self, volume):
        self.volumeLabel.setText(f"{volume}%")
        if volume != 0:
            volumeIcon = QIcon()
            volumeIcon.addPixmap(QPixmap(os.path.join(res_path, "volumeIcon.svg")), QIcon.Normal, QIcon.Off)
            self.volumeBtn.setIcon(volumeIcon)
            self.previousVolume = self.volumeSlider.value()
            self.isMuted = False
        else:
            volumeMutedIcon = QIcon()
            volumeMutedIcon.addPixmap(QPixmap(os.path.join(res_path, "volumeMutedIcon.svg")), QIcon.Normal, QIcon.Off)
            self.volumeBtn.setIcon(volumeMutedIcon)
            self.isMuted = True
    
    def volumeToggle(self):
        if self.isMuted == False:
            self.volumeSlider.setValue(0)
            self.isMuted = True
        elif self.isMuted == True:
            
            if self.previousVolume == 0:
                self.volumeSlider.setValue(10)
            else: 
                self.volumeSlider.setValue(self.previousVolume)
            self.isMuted = False
    
#=======================================================#      
    
    def closeEvent(self, event): #event handler that take window information and save it in config before the window close
        # retrieve position
        xAxis = self.geometry().x()
        yAxis = self.geometry().y()
        
        self.data['last_position']['xPos'] = xAxis
        self.data['last_position']['yPos'] = yAxis
        
        # retrieve size
        width = self.width()
        height = self.height()
        
        self.data['last_window_size']['width'] = width
        self.data['last_window_size']['heigth'] = height
        
        # retrieve volume
        self.data['volume'] = self.mediaPlayer.volume()

        yaml_dump(self.data)

    def player_state(self, event):
        if event == QMediaPlayer.PlayingState:
            pauseIcon = QIcon()
            pauseIcon.addPixmap(QPixmap(os.path.join(res_path, "pauseIcon.svg")), QIcon.Normal, QIcon.Off)
            self.playBtn.setIcon(pauseIcon)
        elif event == QMediaPlayer.PausedState:
            playIcon = QIcon()
            playIcon.addPixmap(QPixmap(os.path.join(res_path, "playIcon.svg")), QIcon.Normal, QIcon.Off)
            self.playBtn.setIcon(playIcon)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    
    #255,112,0 = orange
    #53,53,53 and 25,25,25 = black

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, QColor(255, 112, 0 ))
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    # palette.setColor(QPalette.ToolTipBase, QColor(255, 112, 0 ))
    # palette.setColor(QPalette.ToolTipText, QColor(255, 112, 0 ))
    palette.setColor(QPalette.Text, QColor(255, 112, 0 ))
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, QColor(255, 112, 0 ))
    palette.setColor(QPalette.BrightText, Qt.red)
    # palette.setColor(QPalette.Link, QColor(255, 112, 0 ))
    palette.setColor(QPalette.Highlight, QColor(255, 112, 0 ))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)
    # app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
    
    window = Window()
    window.show()
    config(window.height(), window.width())

    sys.exit(app.exec_())

#TODO palette
# Icons'author links
#https://fontawesome.com/icons/headphones?style=solid
#https://fontawesome.com/icons/backward?style=solid
#https://fontawesome.com/icons/forward?style=solid
#https://fontawesome.com/icons/play?style=solid
#https://fontawesome.com/icons/pause?style=solid
#https://fontawesome.com/icons/random?style=solid
#https://www.flaticon.com/authors/itim2101
#https://fontawesome.com/icons/volume-up?style=solid
#https://fontawesome.com/icons/volume-mute?style=solid