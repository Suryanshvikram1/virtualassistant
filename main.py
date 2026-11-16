# Original terminal-based version is kept.
from voice.speech_to_text import listen
from voice.text_to_speech import speak
from assistant import AstraAssistant

def main():
    assistant = AstraAssistant()
    speak("Hello! I am Astra, your personal AI assistant.")
    while True:
        try:
            user_text = listen()
            if not user_text:
                continue
            if any(x in user_text.lower() for x in ("stop listening", "exit assistant", "quit", "goodbye")):
                speak("Goodbye!")
                break
            response = assistant.handle(user_text)
            print(f"\\nAstra: {response}\\n")
            speak(response)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
