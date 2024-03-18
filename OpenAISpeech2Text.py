import tkinter as tk
from tkinter import filedialog
import pygame
from openai import OpenAI

class AudioPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OpenAI Speech to Text")
        self.root.geometry("400x220")
        
        # Create a label to display the current path of the selected audio file
        self.file_path_label = tk.Label(root, text="No audio file selected", wraplength=300)
        
        # Create buttons for opening, playing, pausing, resuming and restarting audio files
        self.open_button = tk.Button(root, text="Open Audio File", command=self.open_audio)
        self.translate_button = tk.Button(root, text="Translate into English", state=tk.DISABLED, command=self.translate_audio)
        self.transcript_button = tk.Button(root, text="Transcript (Original Language)", state=tk.DISABLED, command=self.transcript_audio)
        self.play_button = tk.Button(root, text="Play Music", state=tk.DISABLED, command=self.play_audio)
        self.pause_button = tk.Button(root, text="Pause Music", state=tk.DISABLED, command=self.pause_audio)
        self.resume_button = tk.Button(root, text="Resume Music", state=tk.DISABLED, command=self.resume_audio)
        self.restart_button = tk.Button(root, text="Restart Music", state=tk.DISABLED, command=self.restart_audio)
        
        self.open_button.grid(row=0, column=0, pady=10, padx=10, columnspan=4, sticky="nsew")
        self.translate_button.grid(row=1, column=0, pady=10, padx=10, columnspan=2, sticky="nsew")
        self.transcript_button.grid(row=1, column=2, pady=10, padx=10, columnspan=2, sticky="nsew")
        self.play_button.grid(row=2, column=0, pady=10, padx=10, sticky="nsew")
        self.pause_button.grid(row=2, column=1, pady=10, padx=10, sticky="nsew")
        self.resume_button.grid(row=2, column=2, pady=10, padx=10, sticky="nsew")
        self.restart_button.grid(row=2, column=3, pady=10, padx=10, sticky="nsew")
        self.file_path_label.grid(row=3, column=0, columnspan=4, pady=10, sticky="nsew")

        # Initialize pygame
        pygame.mixer.init()

        # Register a callback to stop audio when the window is closed
        root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Initialize playback state
        self.paused = False

    # Open selected audio file
    def open_audio(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
        if file_path:
            self.audio_file = file_path
            self.file_path_label.config(text=f"Selected Audio File:\n {self.audio_file}")
            self.translate_button.config(state=tk.NORMAL)
            self.transcript_button.config(state=tk.NORMAL)
            self.play_button.config(state=tk.NORMAL)
            self.restart_button.config(state=tk.NORMAL)

    # Call openAI library to translate audio file into English
    def translate_audio(self):
        client = OpenAI()
        audio_file= open(self.audio_file, "rb")
        transcript = client.audio.translations.create(
          model="whisper-1", 
          file=audio_file, 
          response_format="text"
        )
        print(transcript)

    # Call OpenAI library to transcript audio file (original language)
    def transcript_audio(self):
        client = OpenAI()
        audio_file= open(self.audio_file, "rb")
        transcript = client.audio.transcriptions.create(
          model="whisper-1", 
          file=audio_file, 
          response_format="text"
        )
        print(transcript)

    # Play the selected audio file
    def play_audio(self):
        pygame.mixer.music.load(self.audio_file)
        pygame.mixer.music.play()
        self.play_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)

    # Pause the selected audio file
    def pause_audio(self):
        pygame.mixer.music.pause()
        self.pause_button.config(state=tk.DISABLED)
        self.resume_button.config(state=tk.NORMAL)
        self.paused = True

    # Resume the paused audio file
    def resume_audio(self):
        pygame.mixer.music.unpause()
        self.resume_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)
        self.paused = False
        
    # Play the selected audio file from the beginning
    def restart_audio(self):
        pygame.mixer.music.rewind()

    # Stop playing the audio file if application if terminated
    def on_closing(self):
        # Check if audio is currently playing
        if pygame.mixer.music.get_busy():
            # Stop audio playback before closing the application
            pygame.mixer.music.stop()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioPlayerApp(root)
    root.mainloop()
