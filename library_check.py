from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtCore import QUrl

sound = QSoundEffect()
sound.setSource(QUrl.fromLocalFile("core/Computer Error Alert-SoundBible.com-783113881.wav"))  # Use the absolute path to your sound file
sound.setVolume(1.0)
sound.play()

input("Press Enter to exit after the sound plays.")

