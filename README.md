# AI_Interview_Assistant
An AI-powered interview assistant that:  Continuously listens to the user’s voice.  Detects when the user stops speaking.  Transcribes the speech into text using Vosk.  Sends the text to GPT-OSS-20B via OpenRouter for human-like, natural responses.  Displays answers word by word in Streamlit.  Optionally reads the answers aloud using TTS (pyttsx3).

## Features
- Continuous voice listening
- Real-time transcription using Vosk
- Human-like answers using GPT-OSS-20B via OpenRouter
- Word-by-word display and TTS

## Setup
1. Download the Vosk model and place it in `model/`
2. Create a `.env` file with your OpenRouter API key:
3. Install dependencies:
4. Run the app:

## Notes
- `.env` and Vosk model are **not included** in the repository for security and size reasons.

      
