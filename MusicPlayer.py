from tkinter import * 
from PIL import Image, ImageTk
import pygame
import os
import random

def loadImage(image, size=None):
    image = f"images/{image}"
    img = Image.open(image)
    if size:
        img = img.resize(size)
    return ImageTk.PhotoImage(img)

def formatTime(time):
    mins, secs = divmod(time, 60)
    mins = round(mins)
    secs = round(secs)
    return '{:02d}:{:02d}'.format(mins, secs)

class MusicPlayer:

    def __init__(self):
        self.themeColor = "#F44336"
        self.bgColor = "#161616"
        self.root = Tk()
        self.root.resizable(0,0)
        self.root.geometry("620x390")
        self.root.title("Music Player")
        self.root.configure(bg=self.bgColor)
        iconPath = r"C:\Users\joshi\Documents\Programs\Python\Music Player\images\Icon.ico"
        self.root.iconbitmap(iconPath)


        pygame.init()
        pygame.mixer.init()

        self.started_Playing = False
        self.init_GUI()
        self.init_Songs()

        self.mainWindow.mainloop()

    def init_GUI(self):
        self.optionsImage = loadImage("Options.png",(24,24))
        self.searchImage = loadImage("search.png",(20,20))
        self.musicImage = loadImage("Music.jpg",(200,200))
        self.pauseImage = loadImage("pause.png",(40,40))
        self.playImage = loadImage("play.png",(40,40))
        self.nextImage = loadImage("Forward.png",(24,24))
        self.prevImage = loadImage("Previous.png",(24,24))
        self.loop_off_Image = loadImage("Loop_off.png",(24,24))
        self.loop_on_Image = loadImage("Loop_on.png",(24,24))
        self.random_off_Image = loadImage("Random_off.png",(24,24))
        self.random_on_Image = loadImage("Random_on.png",(24,24))


        self.headerFrame = Frame(self.root, bg=self.bgColor)
        self.headerFrame.pack(side=TOP, fill="x")

        # self.optionsBtn = Button(self.headerFrame, image=self.optionsImage,command=self.toggleListBox, bg=self.bgColor, relief='flat')
        # self.optionsBtn.pack(side=LEFT)

        self.searchBtn = Button(self.headerFrame, image=self.searchImage, bg=self.bgColor, command=self.toggle_searchBtn, relief='flat')
        self.searchBtn.pack(pady=(8,0),padx=8, side=LEFT)

        self.searchEntry = Entry(self.headerFrame, bg="#4d4d4d",fg='white', width=80, highlightbackground=self.themeColor, highlightthickness=1,highlightcolor=self.themeColor, font=('arial',12))
        self.searchEntry.pack(pady=20, padx=10, side=LEFT)
        self.searchEntry.bind('<KeyRelease>', self.updateListbox)
        self.searchEntry.pack_forget()

        self.listWindow = Frame(self.root, bg=self.bgColor)
        self.listWindow.pack(pady=5,side=LEFT)

        self.songsList = Listbox(self.listWindow, height=60, width=40, bg=self.bgColor, fg="white", selectmode=SINGLE)
        self.songsList.pack(padx=10,pady=10)
        self.songsList.bind("<<ListboxSelect>>", self.selectSong)
        
        # self.songsList.pack_forget()

        self.mainWindow = Frame(self.root, bg=self.bgColor)
        self.mainWindow.pack(pady=10)

        self.SongImage = Label(self.mainWindow, image=self.musicImage)
        self.SongImage.pack(pady=5)

        self.songLabel = Label(self.mainWindow, text="", fg=self.themeColor, bg=self.bgColor, font=('arial',12))
        self.songLabel.pack()

        self.createProgressBar()
        self.updateProgressBar()


        buttons_Frame = Frame(self.mainWindow, bg=self.bgColor)
        buttons_Frame.pack()

        self.loopBtn = Button(buttons_Frame, image=self.loop_off_Image, command=self.toggle_Loop, bg=self.bgColor, relief='flat')
        self.loopBtn.pack(side=LEFT, padx=10)

        self.prevBtn = Button(buttons_Frame, image=self.prevImage, command=self.playPrevSong, bg=self.bgColor, relief='flat')
        self.prevBtn.pack(side=LEFT, padx=10)

        self.playBtn = Button(buttons_Frame, image=self.playImage, command=self.toggle_pause_btn, height=40, width=40, bg=self.bgColor, relief='flat', overrelief='flat')
        self.playBtn.pack(side=LEFT, padx=10)

        self.nextBtn = Button(buttons_Frame, image=self.nextImage, command=self.playNextSong, bg=self.bgColor, relief='flat')
        self.nextBtn.pack(side=LEFT, padx=10)

        self.randomBtn = Button(buttons_Frame, image=self.random_off_Image, command=self.toggle_Random_Btn, bg=self.bgColor, relief='flat')
        self.randomBtn.pack(side=LEFT, padx=10)

    def updateListbox(self,event=None):
        search_query = self.searchEntry.get().lower()
        self.songsList.delete(0, END)
        count = 0
        for song in self.songs:
            if search_query in song.lower():
                count +=1
                self.songsList.insert(END, song)
        self.totalSongs = count
        self.song_Index_List = [i for i in range(self.totalSongs)]     

    def toggle_searchBtn(self):
        if self.searchEntry.winfo_ismapped():
            self.searchEntry.pack_forget()
        else:
            self.searchEntry.pack(pady=5, side=RIGHT)

    def init_Songs(self):
        self.folder_path = "C:\\Users\\joshi\\Music"
        self.songs = os.listdir(self.folder_path)
        self.songs = [song for song in self.songs if song.endswith('.mp3')]

        self.songPlaying = False
        self.playRandomSong = False
        self.loop = False
        self.songLength = 0
        self.totalSongs = 0
        self.curr_Song_Index = -1
        self.curr_Song_Pointer = self.curr_Song_Index

        for song in self.songs:
            self.songsList.insert(self.totalSongs, song)
            self.totalSongs += 1

        self.song_Index_List = [i for i in range(self.totalSongs)]

        # for i in range(self.totalSongs):
        #     if i%2 ==0:
        #         self.songsList.itemconfig(i, {'bg':"#373737"})
        
        self.check_song_end()


    def filter_Song_name(self, song):
        
        filteredSong = ''
        index = 0
        for i in song:
            index+=1
            if index < 3:
                filteredSong += i
                continue
            if not i.isdigit():
                filteredSong += i
        
        ignoreChars = ['.','mp','@','-','+']
        for i in ignoreChars:
            if i in filteredSong:
                filteredSong = filteredSong.replace(i,'')

        return filteredSong

    def toggleListBox(self):
        if self.songsList.winfo_ismapped():
            self.songsList.pack_forget()
            self.mainWindow.pack()
        else:
            self.songsList.pack(padx=10,pady=10)

    def createProgressBar(self):
        progressBar_Frame = Frame(self.mainWindow, bg=self.bgColor)
        progressBar_Frame.pack()
        self.incrementProgress = False
        self.draggingDotPoint = False

        self.sliderStartPoint = 20
        self.slider_Len = 260
        self.incrementDuration = 1
        self.temp_incrementDuration = self.incrementDuration
        self.songProgress = 0
        self.dotSize = 0

        slider_Space_Width = 300
        slider_Space_Heigth = 10
        self.slider_Space = Canvas(progressBar_Frame, width=slider_Space_Width, height=slider_Space_Heigth, bg=self.bgColor, highlightbackground=self.bgColor)
        self.slider_Space.pack(pady=(20,0))

        self.slider_Space.bind("<Enter>", self.enter_Space)
        self.slider_Space.bind("<Leave>", self.leave_Space)
        self.slider_Space.bind("<Button-1>", self.change_dot_position)
        self.slider_Space.bind("<B1-Motion>", self.change_dot_position)
        self.slider_Space.bind("<ButtonRelease-1>", self.on_release)

        self.x = self.sliderStartPoint
        self.y = 6
        self.line = self.slider_Space.create_line(self.x, self.y, self.x+self.slider_Len, self.y, width=2, fill="grey")
        
        self.progressLine = self.slider_Space.create_line(self.x, self.y, self.x, self.y, width=2, fill=self.themeColor)
        self.progressDot = self.slider_Space.create_oval(self.x - self.dotSize, self.y - self.dotSize, self.x + self.dotSize, self.y+self.dotSize, fill=self.themeColor)

        self.progress_Len_Label = Label(progressBar_Frame, text="--:--",fg="grey", bg=self.bgColor)
        self.progress_Len_Label.pack(side=LEFT, padx=18)
        self.lengthLabel = Label(progressBar_Frame, text="--:--",fg="grey", bg=self.bgColor)
        self.lengthLabel.pack(side=RIGHT, padx=18)

    def updateProgressBar(self):
        if self.incrementProgress:
            x1, y1, x2, y2 = self.getAxis()
            self.slider_Space.coords(self.progressDot, x1, y1, x2, y2)
            self.slider_Space.coords(self.progressLine, self.x, self.y, x1, self.y)

            self.currSongTime = self.get_Curr_Song_Time()
            self.progress_Len_Label.config(text=f"{formatTime(self.currSongTime)}")

            if self.songProgress < self.slider_Len:
                if not self.draggingDotPoint:
                    self.songProgress += 1
                if not self.songPlaying:
                    self.incrementProgress = False

        self.mainWindow.after(int(self.incrementDuration), self.updateProgressBar)

    def getAxis(self):
        x1 = self.songProgress+(self.x - self.dotSize)
        x2 = self.songProgress+(self.x + self.dotSize)
        y1 = self.y-self.dotSize
        y2 = self.y+self.dotSize

        return x1,y1,x2,y2
    
    def enter_Space(self, event):
        self.slider_Space.config(cursor='hand2')
        self.dotSize = 5
        x1, y1, x2, y2 = self.getAxis()
        self.slider_Space.coords(self.progressDot, x1, y1, x2, y2)

    def leave_Space(self, event):
        self.dotSize = 0
        x1, y1, x2, y2 = self.getAxis()
        self.slider_Space.coords(self.progressDot, x1, y1, x2, y2)

    def change_dot_position(self, event):
        if self.started_Playing:
            if(self.sliderStartPoint < event.x < self.sliderStartPoint+self.slider_Len):
                self.dotSize = 5
                self.draggingDotPoint = True
                self.incrementDuration = 1
                self.songProgress = event.x - self.sliderStartPoint
                pygame.mixer.music.set_volume(0)

                if not self.songPlaying:
                    self.incrementProgress = True

    def on_release(self, event):
        if self.draggingDotPoint:
            self.draggingDotPoint = False
            self.incrementDuration = self.temp_incrementDuration
            pygame.mixer.music.set_volume(1)
            self.currSongTime = self.get_Curr_Song_Time()
            pygame.mixer.music.set_pos(self.currSongTime)

    def get_Curr_Song_Time(self):
        return (self.songProgress / self.slider_Len) * self.songLength

    def selectSong(self,event):
        self.curr_Song_Pointer = self.song_Index_List.index(self.songsList.curselection()[0])
        if self.searchEntry.winfo_ismapped():
            self.searchEntry.pack_forget()
            self.searchEntry.delete(0,END)
            # self.updateListbox()
        self.playSong()

    def playSong(self):
        self.curr_Song_Index = self.song_Index_List[self.curr_Song_Pointer]
        song = self.songsList.get(self.curr_Song_Index)
        self.songLabel.config(text=self.filter_Song_name(song))
        # song = self.songs[self.curr_Song_Index]
        song = os.path.join(self.folder_path, song)
        self.update_Song_Info(song)
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()

        self.incrementProgress = True
        self.songPlaying = False
        self.toggle_pause_btn()

    def highlightSong(self, songIndex):
        try:
            if self.started_Playing:
                self.songsList.itemconfig(self.prevIndex,{'fg':'white'})    
        except:
            pass    
        self.songsList.selection_clear(songIndex)
        self.songsList.itemconfig(songIndex,{'fg':self.themeColor})
        self.prevIndex = songIndex

    def update_Song_Info(self, song):
        self.songLength = pygame.mixer.Sound(song).get_length()
        self.SongTimeFormat = formatTime(self.songLength)
        self.lengthLabel.config(text=f"{self.SongTimeFormat}")
        self.incrementDuration = (self.songLength)*1000/self.slider_Len
        self.temp_incrementDuration = self.incrementDuration
        self.highlightSong(self.curr_Song_Index)
        self.songsList.see(self.curr_Song_Index)
        self.songProgress = 0
        self.started_Playing = True
    
    def toggle_Loop(self):
        self.loop = not self.loop
        if self.loop:
            self.loopBtn.configure(image=self.loop_on_Image)
        else:
            self.loopBtn.configure(image=self.loop_off_Image)

    def toggle_Random_Btn(self):
        self.playRandomSong = not self.playRandomSong

        if self.playRandomSong:
            self.randomBtn.configure(image=self.random_on_Image)
            self.temp = self.song_Index_List.copy()
            random.shuffle(self.song_Index_List)
        else:
            self.randomBtn.configure(image=self.random_off_Image)
            self.song_Index_List = self.temp.copy()

        if self.started_Playing:
            self.curr_Song_Pointer = self.song_Index_List.index(self.curr_Song_Index)
            
    def toggle_pause_btn(self):
        if self.songPlaying:
            pygame.mixer.music.pause()
            self.incrementProgress = False
            self.songPlaying = False
            self.playBtn.config(image = self.playImage)
        else:
            if not self.started_Playing:
                self.playNextSong()

            pygame.mixer.music.unpause()
            self.incrementProgress = True
            self.songPlaying = True
            self.playBtn.config(image = self.pauseImage)

    def playNextSong(self):
        self.curr_Song_Pointer += 1
        if self.curr_Song_Pointer >= self.totalSongs:
            self.curr_Song_Pointer = 0
        self.playSong()

    def playPrevSong(self):
        self.curr_Song_Pointer -= 1
        if self.curr_Song_Pointer < 0:
            self.curr_Song_Pointer = self.totalSongs-1
        self.playSong()

    def check_song_end(self):
        if not pygame.mixer.music.get_busy() and self.songPlaying:
            self.songProgress = 0
            if self.loop:
                self.playSong()
            else:
                self.playNextSong()
        self.mainWindow.after(1000, self.check_song_end)

if __name__ == "__main__":
    MusicPlayer()