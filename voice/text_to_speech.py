import tempfile
from pathlib import Path
import pyttsx3

def speak(text):
    """Speak immediately for the original terminal version."""
    engine = pyttsx3.init()
    engine.setProperty("rate", 170)
    engine.setProperty("volume", 1.0)
    engine.say(str(text))
    engine.runAndWait()
    engine.stop()

def text_to_speech_file(text):
    """Generate a WAV file for playback in the Streamlit interface."""
    temp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    output = temp.name
    temp.close()
    engine = pyttsx3.init()
    engine.setProperty("rate", 170)
    engine.setProperty("volume", 1.0)
    engine.save_to_file(str(text), output)
    engine.runAndWait()
    engine.stop()
    if Path(output).exists() and Path(output).stat().st_size > 0:
        return output
    Path(output).unlink(missing_ok=True)
    return None
