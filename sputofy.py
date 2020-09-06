## !/usr/bin/env python
from __future__ import unicode_literals

import os
import random
import sys

from functools import partial

import pafy
from mhyt import yt_download

import yaml
import youtube_dl

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QAbstractListModel, Qt, QUrl, QPoint
from PyQt5.QtGui import QIcon, QPixmap, QPalette, QColor, QCursor
from PyQt5.QtMultimedia import (QMediaContent, QMediaPlayer,
                            QMediaPlayerControl, QMediaPlaylist, QMediaResource)
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtWidgets import (QFileDialog, QMainWindow, QStyle, 
                                QShortcut, QInputDialog, QAction, QMenu, QListWidgetItem, QPushButton, QMessageBox)


from libs.YouTube_to_MP3.YouTube_to_MP3Window import Ui_Dialog
from libs.SputofyGui.SputofyGui import Ui_MainWindow
from libs.paths import *



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

    def default_folder(self):# get user in order to create the folder in the desktop
        user = os.getlogin()
        default_folderConfig = {
            "default_folder": "C:\\Users\\"+user+"\\Desktop\\sputofy_songs"}
        yaml_dump(default_folderConfig)

    def last_window_size(self):
        self.data['last_window_size']['width'] = self.width
        self.data['last_window_size']['heigth'] = self.height
        yaml_dump(self.data)


class PlaylistModel(QAbstractListModel):
    def __init__(self, playlist, *args, **kwargs):
        super(PlaylistModel, self).__init__(*args, **kwargs)
        self.playlist = playlist

    def data(self, index, role):
        if role == Qt.DisplayRole:
            media = self.playlist.media(index.row())
            song = os.path.splitext(media.canonicalUrl().fileName())[0]# remove file extension
            songPosition = f"#{index.row()+1}    {song}"
            return songPosition

    def rowCount(self, index):
        return self.playlist.mediaCount()

class YouTubeToMP3Window(QtWidgets.QWidget, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


        self.startBtn.clicked.connect(self.startDownload)
        self.download_folderBtn.clicked.connect(self.openDownloadFolder)

    def showWindow(self):
        self.youtube_link.setText("")
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

        # url = "https://youtu.be/p7pERnZ9RRc"
        # video = pafy.new(url)

        # audiostreams = video.audiostreams
        # for a in audiostreams:
        #     print(a.bitrate, a.extension, a.get_filesize())
        # audiostreams[2].download()
        
        # bestaudio = video.getbestaudio()
        # bestaudio.download()

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            if YTlink: 
                try:
                    ydl.download([YTlink])
                    info_dict = ydl.extract_info(YTlink)
                    video_title = info_dict.get('title', None)
                    
                    self.statusbar.showMessage(f"[downloaded] {video_title}", 4000)
                    self.close()
                except:
                    self.statusbar.showMessage("[ERROR]:cannot download this video", 4000)
            else:
                self.statusbar.showMessage("[ERROR]:insert a valid url", 4000)
            
class Window(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        # load config
        self.data = yaml_loader()

        # load ui
        self.setupUi(self)
        
        self.setWindowTitle("Sputofy")
        self.setWindowIcon(QIcon(os.path.join(res_path, "logo.svg")))

        # window's settings
        self.xCor = self.data['last_position']['xPos']
        self.yCor = self.data['last_position']['yPos']
        self.widthSize = self.data['last_window_size']['width']
        self.heightSize = self.data['last_window_size']['heigth']

        self.setGeometry(self.xCor, self.yCor, self.widthSize,self.heightSize)
        
        # load YouTubeToMP3
        self.YouTubeToMP3 = YouTubeToMP3Window()
        
        # open YouTubeToMP3 using button
        self.actionYT_MP3.triggered.connect(self.YouTubeToMP3.showWindow)

        # info action
        self.actionInfo.triggered.connect(self.infoHandle)

        #===========================  mediaplayer  ==============================
        
        # create media player object
        self.mediaPlayer = QMediaPlayer(None)

        # open button
        self.actionOpen_Song.triggered.connect(self.open_song)
        self.actionOpen_Folder.triggered.connect(self.open_folder)


        # play button
        self.playBtn.setEnabled(False)
        self.playBtn.clicked.connect(self.play_video)# when btn is pressed: if it is playing it pause, if it is paused it plays
        # QShortcut(QKeySequence("Space"), self).activated.connect(self.play_video)metodo da ricordare in caso di problemi #TODO

        
        # duration slider
        self.durationSlider.setEnabled(False)
        self.durationSliderMaxValue = 0
        self.durationSlider.valueChanged.connect(self.mediaPlayer.setPosition)# set mediaPlayer position using the value took from the slider
        QShortcut('Right', self, lambda:self.durationSlider.setValue(self.durationSlider.value()+10000))# 1s = 1000ms
        QShortcut('Left', self, lambda:self.durationSlider.setValue(self.durationSlider.value()-10000))# 1s = 1000ms


        QShortcut('Shift+Right', self, lambda:self.durationSlider.setValue(self.durationSliderMaxValue-1000))# jump to the end-1s of song
        QShortcut('Shift+Left', self, lambda:self.durationSlider.setValue(0))# restart song

        
        # volumeSlider
        self.volumeSlider.setProperty("value", 100)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setValue(self.data['volume'] if self.data['volume']!=0 else self.data['volume']+1)# set slider value | if saved volume is equal to 0 load with volume = 1 else load the saved volume
        self.mediaPlayer.setVolume(self.data['volume'] if self.data['volume']!=0 else self.data['volume']+1)# set mediaPlayer volume | if saved volume is equal to 0 load with volume = 1 else load the saved volume
        self.volumeLabel.setText(f"{self.data['volume']}%" if self.data['volume']!=0 else f"{self.data['volume']+1}%")# set volume label text | if saved volume is equal to 0 load with volume = 1 else load the saved volume
        self.volumeSlider.valueChanged.connect(self.mediaPlayer.setVolume)# set mediaPlayer volume using the value took from the slider
        
        QShortcut('Up', self, lambda:self.volumeSlider.setValue(self.volumeSlider.value()+1))# volume + 1
        QShortcut('Down', self, lambda:self.volumeSlider.setValue(self.volumeSlider.value()-1))# volume - 1

        QShortcut('Shift+Up', self, lambda:self.volumeSlider.setValue(100))# set maximum volume
        QShortcut('Shift+Down', self, lambda:self.volumeSlider.setValue(0))# set minimun volume(mute)


        # volumeBtn
        self.volumeBtn.clicked.connect(self.volumeToggle)# mute/unmute volume pressing btn
        self.isMuted = False# starting with a non-muted volume
        self.previousVolume = self.data['volume']# loading last registered volume


        # media player signals
        self.mediaPlayer.durationChanged.connect(self.duration_changed)# set range of duration slider
        self.mediaPlayer.positionChanged.connect(self.position_changed)# duration slider progress
        self.mediaPlayer.stateChanged.connect(self.player_state)# see when it's playing or in pause 
        self.mediaPlayer.volumeChanged.connect(self.volumeIcon)# change volumebtn icon

        #===========================  playlist  ==============================
        
        # create the playlist
        self.playlist = QMediaPlaylist()
        self.playlist.setPlaybackMode(2)
        self.mediaPlayer.setPlaylist(self.playlist)

        # clear the playlist
        self.playlistIsEmpty = True

        # playlistList model
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
        self.playlist.currentMediaChanged.connect(self.setTitle)
        
        
        # playlist buttons
        self.nextBtn.clicked.connect(self.playlist.next)# seek track forward

        self.prevBtn.clicked.connect(self.playlist.previous)# seek track backward

        self.mediaPlayer.mediaStatusChanged.connect(self.autoNextTrack)# once song is ended seek track forward and play it
                                                                         

        self.actionLoopIt.triggered.connect(self.loopSong)# (1) loop the same song

        self.actionShuffle.triggered.connect(self.shufflePlaylist)# change song's order

        self.loopBtn.clicked.connect(self.loop)# (3) loop the playlist  
        
        self.randomBtn.clicked.connect(self.random)# (4) play random song without end
        
        # create new playlist
        self.actionCreatePlaylist.triggered.connect(self.custom_playlist)
        
        # delete current playlist
        self.actionDeletePlaylist.triggered.connect(self.delete_playlist)

        # remove all songs
        self.actionClearQueue.triggered.connect(self.clear_queue)

        # load playlist
        # self.playlistList = self.data['playlistList']
        self.actionDict = {} # dictionary of action Objects

        for action in self.data['playlistList']:
            self.actionDict[action] = self.menuPlaylist.addAction(action, partial(self.load_playlist, action))
        
        if len(self.data['playlistList']) == 0:
            self.menuPlaylist.menuAction().setVisible(False)

#================== Songs opening ==================#
    
    def open_folder(self):
        foldername = QFileDialog.getExistingDirectory(self, "Open folder", "c:\\")

        if foldername != '':
            self.playlist.clear()
            self.mediaList.clear()
            
            for song in os.listdir(foldername):
                media = f"{foldername}/{song}"
                self.playlist.addMedia(QMediaContent(QUrl(media)))
                self.mediaList.append(media)
                
            
            self.playlist.setCurrentIndex(0)

            self.playBtn.setEnabled(True)
            self.durationSlider.setEnabled(True)
            
            self.playlistIsEmpty = False
            self.isCustomPlaylist = False

            self.model.layoutChanged.emit()# load songs in list view
            self.setTitle()

            self.mediaPlayer.pause()# adjust play/pause icon

    def open_song(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Song", "c:\\", "mp3 Audio(.mp3)")

        if filename != '':
            if self.playlistIsEmpty == False:
                self.playlist.clear()
                self.mediaList.clear()
                self.playlistIsEmpty = True

            self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.mediaList.append(filename)

            self.playBtn.setEnabled(True)
            self.durationSlider.setEnabled(True)

            self.isCustomPlaylist = False

            self.model.layoutChanged.emit()# load song in list view
            self.setTitle()
            
            # adjust play/pause icon
            if self.playlist.mediaCount() == 1:# if there is 1 song and you add another 
                self.playlist.setCurrentIndex(0)
                self.mediaPlayer.pause()
           
    def load_playlist(self, playlistName):
        self.playlist.clear()
        self.mediaList.clear()
        
        #reload config
        self.data = yaml_loader()
        
        for song in self.data['playlistList'][playlistName]:
            self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(song)))
            self.mediaList.append(song)

        self.playlist.setCurrentIndex(0)

        self.playBtn.setEnabled(True)
        self.durationSlider.setEnabled(True)
        
        self.playlistIsEmpty = False
        self.isCustomPlaylist = True

        self.model.layoutChanged.emit()# load songs in list view
        
        self.currentPlaylist = playlistName# name of current loaded playlist
        self.setTitle()
        
        self.statusbar.showMessage(f'Playlist "{playlistName}" loaded', 4000)
        self.menuPlaylist.menuAction().setVisible(True)
        
        # adjust play/pause icon
        self.mediaPlayer.pause()
  
    def setTitle(self):
        if self.playlist.mediaCount() == 0:
            self.setWindowTitle("Sputofy")
        
        else:    
            if self.isCustomPlaylist == False:
                self.setWindowTitle(f"Sputofy - {os.path.splitext(self.playlist.currentMedia().canonicalUrl().fileName())[0]} - {self.playlist.currentIndex()+1}/{self.playlist.mediaCount()}")
            else:
                self.setWindowTitle(f"Sputofy - {self.currentPlaylist} - {os.path.splitext(self.playlist.currentMedia().canonicalUrl().fileName())[0]} - {self.playlist.currentIndex()+1}/{self.playlist.mediaCount()}")
            
#=======================================================# 


#================== Player Functions ==================#
    
    def play_video(self):
        if not self.durationSlider.isEnabled() == False:# if slider was enabled 
            if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
                self.mediaPlayer.pause()
            
            else:
                self.mediaPlayer.play()

    def duration_changed(self, duration):
        self.durationSlider.setRange(0, duration)
        
        if duration >= 0:
            self.totalTime_Label.setText(time_format(round(duration/1000)))# duration is in ms 
        self.durationSliderMaxValue = duration

    def position_changed(self, position):
        if position >= 0:
            self.elapsedTime_Label.setText(time_format((position/1000)))# position is in ms
        
        # Disable the events to prevent updating triggering a setPosition event (can cause stuttering).
        self.durationSlider.blockSignals(True)
        self.durationSlider.setValue(position)
        self.durationSlider.blockSignals(False)

#=======================================================# 


#================== Playlist Settings ==================#
    #TODO useless
    def playlist_array(self):
        index = self.playlist.mediaCount()
        mediaList = []
        for i in range(index):
            # songPath = (self.playlist.media(path).canonicalUrl().path())#.split("/",1)[1]
            # mediaList.append(songPath)
            # print(self.playlist.media(i).canonicalUrl().path())
            mediaList.append(self.playlist.media(i).canonicalUrl().fileName())
        return mediaList

    def custom_playlist(self):
        if not self.playlist.mediaCount() == 0:
            name, is_notEmpty = QInputDialog.getText(self, "playlist", "save playlist as:")
            
            if name != "":

                self.data['playlistList'][name] = self.mediaList
                yaml_dump(self.data)
                
                # addin new action Object to dictionary
                self.actionDict[name] = self.menuPlaylist.addAction(name, partial(self.load_playlist, name))

                self.load_playlist(name)# instantly loading the new playlist
            else:
                self.statusbar.showMessage("playlist not created (you should give a name to your baby :/)", 4000)
        else:
            self.statusbar.showMessage("there are no songs to playlist", 4000)

    def delete_playlist(self):
        if self.isCustomPlaylist == True:
            
            if len(self.data['playlistList']) == 1:
                self.menuPlaylist.menuAction().setVisible(False)

            self.data['playlistList'].pop(self.currentPlaylist)# remove playlist from dictionary

            
            self.menuPlaylist.removeAction(self.actionDict[self.currentPlaylist])# remove relative action
            self.actionDict.pop(self.currentPlaylist)# remove relative action Object

            self.playlist.clear()
            self.model.layoutChanged.emit()
            self.setWindowTitle("Sputofy")

            yaml_dump(self.data)

            self.statusbar.showMessage('succesfully deleted "'+self.currentPlaylist+'" playlist', 4000)
        else:
            self.statusbar.showMessage("cannot delete a non custom playlist", 4000)

    def clear_queue(self):
        self.playlist.clear()
        self.mediaList.clear()
        self.playBtn.setEnabled(False)
        self.model.layoutChanged.emit()

    def playlist_position_changed(self, i):
        if i > -1:
            ix = self.model.index(i)
            self.playlistView.setCurrentIndex(ix)

    def playlist_selection_changed(self, ix):
        # We receive a QItemSelection from selectionChanged.
        i = ix.indexes()[0].row()
        self.posizione = i
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
    
    def shufflePlaylist(self):
        if  not self.playlist.mediaCount() == 0:
            self.playlist.shuffle()
            self.model.layoutChanged.emit()
        else:
            self.statusbar.showMessage("there are no songs to shuffle", 4000)

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
                else:# if ended song was the last one set the index to the first one and pause 
                    self.playlist.setCurrentIndex(0)
                    self.mediaPlayer.pause()

            # loop playlist
            elif self.playlist.playbackMode() == 3:
                self.playlist.next()
                self.mediaPlayer.play()
            
            # random song
            elif self.playlist.playbackMode() == 4:
                while self.playlist.previousIndex() == self.playlist.currentIndex():# preventing repeating the same song
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
    
    def mousePressEvent(self, event):# remove the border around the buttons created by using tab key 
        focused_widget = QtWidgets.QApplication.focusWidget()
        try:
            focused_widget.clearFocus()
        except:
            pass
        QMainWindow.mousePressEvent(self, event)

    def player_state(self, event):# event handler that adjust the play/pause icon
        if event == QMediaPlayer.PlayingState:
            pauseIcon = QIcon()
            pauseIcon.addPixmap(QPixmap(os.path.join(res_path, "pauseIcon.svg")), QIcon.Normal, QIcon.Off)
            self.playBtn.setIcon(pauseIcon)
        elif event == QMediaPlayer.PausedState:
            playIcon = QIcon()
            playIcon.addPixmap(QPixmap(os.path.join(res_path, "playIcon.svg")), QIcon.Normal, QIcon.Off)
            self.playBtn.setIcon(playIcon)

    def closeEvent(self, event): # event handler that take window information and save it in config before the window close
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

    def infoHandle(self):
        # info = "©2020\na_str0\n\n"
        info = "Sputofy\n1.0.0\n©2020"+\
        "Sputofy is a free audio player based on the converted youtube songs made by a_str0\n\n"+\
        "Sputofy is written using python 3.x and PyQt5 modules"
                
        msg = QMessageBox.about(self, "About", info)
    

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
    app.setStyleSheet("QToolTip { color: rgb(255,112,0); background-color: #000; border: 1px solid rgb(255,112,0); } QMenu::separator{background: rgb(255,112,0); height: 1px}")
    
    window = Window()
    window.show()
    config(window.height(), window.width())

    sys.exit(app.exec_())


# Icons'author links
#https://fontawesome.com/icons/headphones?style=solid   (logo)
#https://fontawesome.com/icons/backward?style=solid     (prevBtn)
#https://fontawesome.com/icons/forward?style=solid      (nextBtn)
#https://fontawesome.com/icons/play?style=solid         (playBtn)
#https://fontawesome.com/icons/pause?style=solid        (playBtn)
#https://fontawesome.com/icons/random?style=solid       (randomBtn)
#https://www.flaticon.com/free-icon/exchange_1251615?term=loop&page=1&position=1    created by itim2101 from  www.flaticon.com       (loopBtn)
#https://fontawesome.com/icons/volume-up?style=solid    (volumeBtn)
#https://fontawesome.com/icons/volume-mute?style=solid  (volumeBtn)