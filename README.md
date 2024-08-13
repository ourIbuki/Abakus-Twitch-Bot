# Abakus | Servant (Twitch Widget) 🎮🎥

Willkommen zu **Abakus | Servant**! Dieses Projekt bietet dir ein einfaches und leistungsstarkes Tool, um Sounds und GIFs in deinem Twitch-Stream aus Chat-Nachrichten heraus abzuspielen. Das Projekt kombiniert die Möglichkeiten von Python, Flask, und TwitchIO, um eine unterhaltsame und interaktive Erfahrung für dich und deine Zuschauer zu schaffen. 

## Features ✨
- **Sound-Abspielung**: Spiele Sounds ab, wenn bestimmte Chat-Befehle erkannt werden.
- **GIF-Abspielung**: Zeige animierte GIFs in deinem Stream, basierend auf Chat-Befehlen.
- **Chat Counter**: Zeigt einen Counter für benutzerdefinierte Emotes an.
- **Benutzerfreundliche GUI**: Eine moderne und anpassbare Benutzeroberfläche mit einfachem Zugriff auf die wichtigsten Funktionen.
- **Dark Mode**: Dunkles, modernes Design als Standard.

## Installation 🛠️

1. **Klonen des Repositories:**
    ```bash
    git clone https://github.com/ourIbuki/Abakus-Twitch-Bot.git
    cd Abakus-Twitch-Bot
    ```

2. **Installiere die Abhängigkeiten:**
    Stelle sicher, dass du Python 3.x installiert hast. Installiere dann die benötigten Pakete mit:
    ```bash
    pip install -r requirements.txt
    ```

3. **Starte das Programm:**
    ```bash
    python servant.py
    ```

## Nutzung 🚀

### Hinzufügen von Sounds 🎵
- Öffne die `servant.py` Datei.
- Füge deinen Soundpfad in den `sound_paths` Dictionary ein:
    ```python
    sound_paths = {
        "<message name>": r"C:\Novelnia\Servant\sounds\<sound name>.mp3",
        # Füge hier weitere Sounds hinzu
    }
    ```

### Hinzufügen von GIFs 🎞️
- Öffne die `servant.py` Datei.
- Füge deinen GIF-Pfad in den `gif_paths` Dictionary ein:
    ```python
    gif_paths = {
        "!<command name>": "/static/gifs/<gif name>.gif",
        # Füge hier weitere GIFs hinzu
    }
    ```

### Nutzung in OBS 🖥️
- Füge die URL `http://localhost:5000` als Browser-Quelle in OBS hinzu, um den Chat Counter anzuzeigen.
- Nutze `http://localhost:3000` als Quelle für die GIF-Anzeige.

## Anpassungen 🔧

- **Dark Mode**: Der Dark Mode ist standardmäßig aktiviert.
- **Button Farben**: Die Buttons ändern ihre Farbe, um den Status der Widgets anzuzeigen (`enabled` = grün, `disabled` = rot).

## Entwicklung 💻

Beiträge sind willkommen! Erstelle einfach ein Issue oder einen Pull-Request auf GitHub, um beizutragen.

---

Danke, dass du **Abakus | Servant** nutzt! 🎉
