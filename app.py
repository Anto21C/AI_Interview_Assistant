import streamlit as st
from responder import get_ai_response
from vosk import Model, KaldiRecognizer
import sounddevice as sd
import queue
import json
import time
import pyttsx3

st.title("AI Interview Assistant 🤖 (Continuous Voice)")

# Load Vosk model
model = Model("model/vosk-model-small-en-us-0.15")
q = queue.Queue()

# TTS Engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)

# Microphone callback
def audio_callback(indata, frames, time_, status):
    if status:
        print(status)
    q.put(bytes(indata))

def listen_until_silence(silence_limit=1.0):
    """
    Continuously listens until user stops speaking for silence_limit seconds
    """
    rec = KaldiRecognizer(model, 16000)
    rec.SetWords(True)
    last_speech_time = time.time()
    transcription = ""

    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=audio_callback):
        st.info("Listening... Speak now!")
        while True:
            while not q.empty():
                data = q.get()
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    text = result.get("text", "")
                    if text.strip():
                        transcription += " " + text
                        last_speech_time = time.time()
            # Stop when silence exceeds limit
            if transcription and (time.time() - last_speech_time > silence_limit):
                return transcription.strip()

# Main loop
while True:
    question = listen_until_silence(silence_limit=1.0)
    st.write(f"**You said:** {question}")

    ai_answer = get_ai_response(question)

    # Word-by-word display
    placeholder = st.empty()
    text = ""
    for word in ai_answer.split():
        text += word + " "
        placeholder.text(text)
        time.sleep(0.15)  # Adjust for human-like typing

    # Optional: Speak the answer
    engine.say(ai_answer)
    engine.runAndWait()
