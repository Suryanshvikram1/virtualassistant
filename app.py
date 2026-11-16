import io
from pathlib import Path
import streamlit as st
import speech_recognition as sr
from pypdf import PdfReader
from assistant import AstraAssistant
from voice.text_to_speech import text_to_speech_file

st.set_page_config(page_title="Astra | AI Virtual Assistant", page_icon="🤖")
st.title("🤖 Astra — AI Virtual Assistant")
st.caption("Use the text chat or the dedicated microphone recorder.")

if "assistant" not in st.session_state:
    st.session_state.assistant = AstraAssistant()
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""

with st.sidebar:
    st.header("Settings")
    speak_replies = st.toggle("Speak replies aloud", value=True)
    st.caption("Voice recording uses your browser microphone.")
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.assistant.reset_history()
        st.rerun()

with st.expander("📄 Upload a PDF"):
    pdf = st.file_uploader("Choose a text-based PDF", type=["pdf"])
    if pdf:
        try:
            reader = PdfReader(io.BytesIO(pdf.getvalue()))
            st.session_state.pdf_text = " ".join(
                (page.extract_text() or "") for page in reader.pages
            )[:12000]
            st.success(f"Loaded {pdf.name}")
            if not st.session_state.pdf_text:
                st.warning("No selectable text found. Scanned PDFs need OCR.")
        except Exception as exc:
            st.error(f"PDF error: {exc}")

def transcribe(audio_file):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(io.BytesIO(audio_file.getvalue())) as source:
            audio = recognizer.record(source)
        return recognizer.recognize_google(audio, language="en-IN")
    except sr.UnknownValueError:
        st.warning("I couldn't understand that recording. Please try again.")
    except sr.RequestError as exc:
        st.error(f"Speech recognition service error: {exc}")
    except Exception as exc:
        st.error(f"Audio processing error: {exc}")
    return None

def respond(text):
    text = text.strip()
    if not text:
        return
    st.session_state.messages.append({"role": "user", "content": text})
    if st.session_state.pdf_text:
        answer = st.session_state.assistant.answer_with_context(
            text, st.session_state.pdf_text
        )
    else:
        answer = st.session_state.assistant.handle(text)
    st.session_state.messages.append({"role": "assistant", "content": answer})
    if speak_replies:
        try:
            audio_path = text_to_speech_file(answer)
            if audio_path:
                st.session_state.last_audio = Path(audio_path).read_bytes()
                Path(audio_path).unlink(missing_ok=True)
        except Exception as exc:
            st.warning(f"Could not generate voice reply: {exc}")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.session_state.get("last_audio"):
    with st.expander("🔊 Play latest spoken reply"):
        st.audio(st.session_state.last_audio, format="audio/wav")

typed = st.chat_input("Type your message to Astra...")
if typed:
    respond(typed)
    st.rerun()

st.divider()
st.subheader("🎙️ Speak to Astra")
st.write("Record a message, stop recording, then click Send voice message.")
recording = st.audio_input("Record voice message")
if recording is not None:
    st.audio(recording)
    if st.button("Send voice message", type="primary", use_container_width=True):
        with st.spinner("Converting speech to text..."):
            transcript = transcribe(recording)
        if transcript:
            st.info(f"You said: {transcript}")
            respond(transcript)
            st.rerun()
