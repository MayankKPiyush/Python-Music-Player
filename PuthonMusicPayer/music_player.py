from tkinter import *
from tkinter import filedialog
import pygame.mixer as mixer
import os

mixer.init()

is_paused = False

def play_pause_song(song_name: StringVar, songs_list: Listbox, status: StringVar, button: Button):
    global is_paused
    if is_paused:
        mixer.music.unpause()
        status.set("Song PLAYING")
        button.config(text="Pause")
        is_paused = False
    else:
        if mixer.music.get_busy():
            mixer.music.pause()
            status.set("Song PAUSED")
            button.config(text="Play")
            is_paused = True
        else:
            selected_song = songs_list.get(ACTIVE)
            if selected_song:
                song_name.set(selected_song)
                mixer.music.load(selected_song)
                mixer.music.play()
                status.set("Song PLAYING")
                button.config(text="Pause")
                is_paused = False

def play_next_song(song_name: StringVar, songs_list: Listbox, status: StringVar, button: Button):
    current_selection = songs_list.curselection()
    if current_selection:
        next_index = current_selection[0] + 1
        if next_index < songs_list.size():
            songs_list.selection_clear(0, END)
            songs_list.select_set(next_index)
            songs_list.activate(next_index)
            next_song = songs_list.get(next_index)
            song_name.set(next_song)
            mixer.music.load(next_song)
            mixer.music.play()
            status.set("Song PLAYING")
            button.config(text="Pause")
        else:
            status.set("End of Playlist")

def play_previous_song(song_name: StringVar, songs_list: Listbox, status: StringVar, button: Button):
    current_selection = songs_list.curselection()
    if current_selection:
        prev_index = current_selection[0] - 1
        if prev_index >= 0:
            songs_list.selection_clear(0, END)
            songs_list.select_set(prev_index)
            songs_list.activate(prev_index)
            prev_song = songs_list.get(prev_index)
            song_name.set(prev_song)
            mixer.music.load(prev_song)
            mixer.music.play()
            status.set("Song PLAYING")
            button.config(text="Pause")
        else:
            status.set("Start of Playlist")
    else:
        status.set("No song selected")

def load(listbox):
    directory = filedialog.askdirectory(title='Open a songs directory')
    if directory:
        os.chdir(directory)
        tracks = os.listdir()
        listbox.delete(0, END)
        for track in tracks:
            if track.endswith(".mp3"):
                listbox.insert(END, track)

def set_volume(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)

root = Tk()
root.geometry('700x300')
root.title('Python Music Player')
root.resizable(0, 0)
root.configure(bg='#121212')

song_frame = LabelFrame(root, text='Current Song', bg='#1e1e1e', fg='#e0e0e0', font=('Helvetica', 12))
song_frame.place(x=0, y=0, width=400, height=80)

button_frame = LabelFrame(root, text='Control Buttons', bg='#1e1e1e', fg='#e0e0e0', font=('Helvetica', 12))
button_frame.place(y=80, width=400, height=120)

listbox_frame = LabelFrame(root, text='Playlist', bg='#1e1e1e', fg='#e0e0e0', font=('Helvetica', 12))
listbox_frame.place(x=400, y=0, height=250, width=300)

current_song = StringVar(root, value='<Not selected>')
song_status = StringVar(root, value='<Not Available>')

playlist = Listbox(listbox_frame, font=('Helvetica', 11), selectbackground='#ffa500', bg='#2a2a2a', fg='#e0e0e0', selectforeground='black')

scroll_bar = Scrollbar(listbox_frame, orient=VERTICAL)
playlist.config(yscrollcommand=scroll_bar.set)
scroll_bar.config(command=playlist.yview)

scroll_bar.pack(side=RIGHT, fill=Y)
playlist.pack(fill=BOTH, padx=5, pady=5)

Label(song_frame, text='CURRENTLY PLAYING:', bg='#1e1e1e', fg='#e0e0e0', font=('Helvetica', 10)).place(x=5, y=20)

song_lbl = Label(song_frame, textvariable=current_song, bg='#2a2a2a', fg='#e0e0e0', font=("Helvetica", 12), width=25)
song_lbl.place(x=150, y=20)

button_style = {'bg': '#3a3a3a', 'fg': '#e0e0e0', 'font': ("Helvetica", 13), 'activebackground': '#4a4a4a'}

prev_btn = Button(button_frame, text='Prev', width=7, command=lambda: play_previous_song(current_song, playlist, song_status, play_pause_btn), **button_style)
prev_btn.place(x=45, y=10)

play_pause_btn = Button(button_frame, text='Play', width=7, command=lambda: play_pause_song(current_song, playlist, song_status, play_pause_btn), **button_style)
play_pause_btn.place(x=135, y=10)

next_btn = Button(button_frame, text='Next', width=7, command=lambda: play_next_song(current_song, playlist, song_status, play_pause_btn), **button_style)
next_btn.place(x=225, y=10)

load_btn = Button(button_frame, text='Load Directory', width=35, command=lambda: load(playlist), **button_style)
load_btn.place(x=10, y=55)

volume_scale = Scale(button_frame, from_=100, to=0, orient=VERTICAL, command=set_volume, bg='#2a2a2a', fg='#e0e0e0', highlightbackground='#1e1e1e')
volume_scale.set(50)
volume_scale.place(x=340, y=8, height=80)

Label(root, textvariable=song_status, bg='#121212', fg='#e0e0e0', font=('Helvetica', 9)).pack(side=BOTTOM, fill=X)

root.mainloop()
