import io
import speech_recognition as sr

recognizer = sr.Recognizer()

def listen():
    """Microphone listener for the original terminal version."""
    try:
        with sr.Microphone() as source:
            print("Listening... Speak now.")
            recognizer.adjust_for_ambient_noise(source, duration=0.6)
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=12)
        return recognizer.recognize_google(audio, language="en-IN")
    except sr.WaitTimeoutError:
        print("No speech detected.")
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand.")
    except sr.RequestError as exc:
        print(f"Speech recognition error: {exc}")
    except OSError as exc:
        print(f"Microphone error: {exc}")
    return None

def recognize_audio_bytes(audio_bytes, language="en-IN"):
    """Transcribe WAV bytes captured by the Streamlit browser recorder."""
    with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
        audio = recognizer.record(source)
    return recognizer.recognize_google(audio, language=language)
