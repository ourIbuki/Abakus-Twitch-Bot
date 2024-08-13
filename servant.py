# Twitch Widget by Ibuki @ Novelnia v1 (Changes on the Code is allowd but not Supported)

# Add a Sound / Effect --> Use the sound_path attribute z.B. ("<message name>": r"<sound path>.mp3",)
# Add a Gif --> Use the gif_paths attribute z.B. ("!<command name>": "<path to gif must be in /static/>.gif",)
# Use the Chat Counter as OBS Widget. --> Lounge py and the Server (flask) sould start automatically then you add localhost:5000 to your OBS Webwiew.
# When Programm is starting a Windows sould open where you can toggle on the bottom the widgets and a chat/logs window in the center.

# You can use and change the Code! But i wont help you with anything try ChatGPT, Google or Books.

import asyncio
from twitchio.ext import commands
import tkinter as tk
from tkinter import scrolledtext, messagebox
from ttkthemes import ThemedTk
from datetime import datetime
import threading
import pygame
from flask import Flask, render_template, jsonify, send_file
from collections import defaultdict, deque
import time
import emoji
import pyttsx3
from flask_socketio import SocketIO, emit

# User Settings
abakus_twitch_token = "XXX"
abakus_twitch_alias = "XXX"
abakus_twitch_link = "https://www.twitch.tv/XXX"
abakus_ccserver_secret = "XXX"
abakus_gifserver_secret = "XXX"

# Initialisiere Pygame Mixer für Sound
pygame.mixer.init()

# Initialisiere pyttsx3 für TTS
engine = pyttsx3.init()

# Pfade zu den MP3-Dateien
sound_paths = {
    "<user text name (text without !)>": r"C:\Novelnia\Servant\sounds\<sound name>.mp3"
}

# Pfade zu den GIF-Dateien
gif_paths = {
    "<user command name (text with !)>": "/static/gifs/<gif name>.gif"
}

# Flask Web App für den Chat-Counter
app_chat = Flask(__name__)
app_chat.config['SECRET_KEY'] = abakus_ccserver_secret

# Flask Web App für den GIF-Player
app_gif = Flask(__name__)
app_gif.config['SECRET_KEY'] = abakus_gifserver_secret
socketio = SocketIO(app_gif)  # WebSocket für den GIF-Player

# Shared State
message_counts = defaultdict(int)
message_timestamps = defaultdict(deque)
current_emotes = []
max_emotes = 5
emote_times = defaultdict(float)
chat_counter_enabled = True
sounds_enabled = True
tts_enabled = False
gif_enabled = True  # Flag für GIFs

# Chat-Counter Routes
@app_chat.route('/')
def index_chat():
    return render_template('chat_counter.html')

@app_chat.route('/data')
def data_chat():
    now = time.time()
    global current_emotes
    current_emotes = [emote for emote in current_emotes if now - emote_times[emote['text']] < 10]

    return jsonify({
        'emotes': current_emotes,
        'show_widget': bool(current_emotes)
    })

# GIF-Player Routes
@app_gif.route('/')
def index_gif():
    return render_template('gif_player.html')

@app_gif.route('/get-gif/<filename>')
def get_gif(filename):
    gif_path = f"C:/Novelnia/Servant/gifs/{filename}"
    return send_file(gif_path, mimetype='image/gif')

@app_gif.route('/test-gif')
def test_gif():
    socketio.emit('playGif', {'gifPath': gif_paths['!schlag']})
    return "Test GIF signal sent!"

@socketio.on('connect')
def handle_connect(auth):
    print("Client connected")
    socketio.emit('playGif', {'gifPath': gif_paths['!schlag']})

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(token=abakus_twitch_token, prefix='', initial_channels=[abakus_twitch_alias])
        self.root = ThemedTk(theme="equilux")  # Dark mode standardmäßig aktiviert
        self.root.title("Abakus | Servant (" + abakus_twitch_alias +  ")")
        
        # Layout anpassen
        self.main_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        
        self.text_area = scrolledtext.ScrolledText(self.main_frame, wrap=tk.WORD, width=50, height=20, font=("Arial", 15), bg="#1e1e1e", fg="white", insertbackground="white")
        self.text_area.grid(row=0, column=0, columnspan=4, pady=10, sticky="nsew")
        self.text_area.configure(state='disabled')

        self.log_message("Bot started...")

        # Modernisierte Buttons
        self.create_buttons()

        # Layout anpassen, damit es sich der Fenstergröße anpasst
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.columnconfigure(2, weight=1)
        self.main_frame.columnconfigure(3, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=0)

    def create_buttons(self):
        # Buttons mit Farbänderung basierend auf Status
        self.chat_counter_button = tk.Button(self.main_frame, text="Chat Counter", command=self.toggle_chat_counter, bg="green" if chat_counter_enabled else "red", fg="white")
        self.chat_counter_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.sounds_button = tk.Button(self.main_frame, text="Sounds", command=self.toggle_sounds, bg="green" if sounds_enabled else "red", fg="white")
        self.sounds_button.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.tts_button = tk.Button(self.main_frame, text="TTS", command=self.toggle_tts, bg="green" if tts_enabled else "red", fg="white")
        self.tts_button.grid(row=1, column=2, padx=5, pady=5, sticky="ew")

        self.gif_button = tk.Button(self.main_frame, text="GIFs", command=self.toggle_gifs, bg="green" if gif_enabled else "red", fg="white")
        self.gif_button.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

    def update_button_colors(self):
        self.chat_counter_button.config(bg="green" if chat_counter_enabled else "red")
        self.sounds_button.config(bg="green" if sounds_enabled else "red")
        self.tts_button.config(bg="green" if tts_enabled else "red")
        self.gif_button.config(bg="green" if gif_enabled else "red")

    def log_message(self, message):
        """Logge eine Nachricht im GUI-Textbereich."""
        self.text_area.configure(state='normal')
        self.text_area.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')} - {message}\n")
        self.text_area.configure(state='disabled')
        self.text_area.yview(tk.END)

    def toggle_chat_counter(self):
        global chat_counter_enabled
        chat_counter_enabled = not chat_counter_enabled
        self.update_button_colors()
        self.log_message(f"[Abakus] Chat counter {'enabled' if chat_counter_enabled else 'disabled'}.")

    def toggle_sounds(self):
        global sounds_enabled
        sounds_enabled = not sounds_enabled
        self.update_button_colors()
        self.log_message(f"[Abakus] Sounds {'enabled' if sounds_enabled else 'disabled'}.")

    def toggle_tts(self):
        global tts_enabled
        tts_enabled = not tts_enabled
        self.update_button_colors()
        self.log_message(f"[Abakus] TTS {'enabled' if tts_enabled else 'disabled'}.")

    def toggle_gifs(self):
        global gif_enabled
        gif_enabled = not gif_enabled
        self.update_button_colors()
        self.log_message(f"[Abakus] GIFs {'enabled' if gif_enabled else 'disabled'}.")

    async def event_ready(self):
        self.log_message(f'Logged in as ' + abakus_twitch_alias + '(' + abakus_twitch_link + ')')
        self.log_message(f'[Abakus] !>> Running the ChatCounter Server @ localhost:5000')
        self.log_message(f'[Abakus] !>> Running the GifPlayer Server @ localhost:3000')
        print(f'Logged in as | ' + abakus_twitch_alias)

    async def event_message(self, message):
        if message.echo or not chat_counter_enabled:
            return

        global current_emotes, emote_times

        self.log_message(f'[MSG] {message.author.name} > {message.content}')
        
        words = message.content.split()
        now = time.time()
        for word in words:
            if not word.strip():  # Skip empty words
                continue

            message_counts[word] += 1
            message_timestamps[word].append(now)
            if len(message_timestamps[word]) > 3:
                message_timestamps[word].popleft()

            if len(message_timestamps[word]) == 3 and (now - message_timestamps[word][0] <= 10):
                emote_times[word] = now
                emote_found = next((emote for emote in current_emotes if emote['text'] == word), None)
                if emote_found:
                    emote_found['count'] = message_counts[word]
                else:
                    if len(current_emotes) < max_emotes:
                        current_emotes.append({'text': word, 'count': message_counts[word]})
                    else:
                        current_emotes.pop(0)
                        current_emotes.append({'text': word, 'count': message_counts[word]})

                if tts_enabled:
                    engine.say(word)
                    engine.runAndWait()

        if sounds_enabled:
            content_lower = message.content.lower()
            if content_lower in sound_paths:
                self.play_sound(content_lower)
                chat_response = content_lower.capitalize() if content_lower != 'clap' else 'Clap'
                await message.channel.send(f"({message.author.name}): {chat_response}!")
                self.log_message(f'{message.author.name} >> {content_lower} (Sound)')

        if gif_enabled:
            content_lower = message.content.lower()
            if content_lower in gif_paths:
                self.log_message(f'Triggering GIF for command: {content_lower}')  # Debug message
                self.play_gif(content_lower)
                await message.channel.send(f"({message.author.name}): {content_lower} GIF triggered!")
                self.log_message(f'{message.author.name} >> {content_lower} (GIF)')

    def play_sound(self, sound_key):
        def run():
            pygame.mixer.music.load(sound_paths[sound_key])
            pygame.mixer.music.play()
        self.root.after(0, run)

    def play_gif(self, gif_key):
        def run():
            self.log_message(f'Sending playGif message for: {gif_key}')  # Debug message
            socketio.emit('playGif', {'gifPath': gif_paths[gif_key]})
        self.root.after(0, run)

    def show_message(self, title, message):
        def run():
            self.root.update()
            messagebox.showinfo(title, message)
        self.root.after(0, run)

def run_flask_chat():
    from waitress import serve
    serve(app_chat, host="0.0.0.0", port=5000)

def run_flask_gif():
    socketio.run(app_gif, host="0.0.0.0", port=3000)

def run_bot():
    try:
        bot.run()
    except Exception as e:
        bot.show_message("Error", str(e))

if __name__ == "__main__":
    bot = Bot()
    flask_chat_thread = threading.Thread(target=run_flask_chat)
    flask_gif_thread = threading.Thread(target=run_flask_gif)
    flask_chat_thread.start()
    flask_gif_thread.start()
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    bot.root.mainloop()
