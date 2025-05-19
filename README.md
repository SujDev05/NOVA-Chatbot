# NOVA: Voice Assistant with Speech-to-Text, Chat, and Text-to-Speech

NOVA is an intelligent voice assistant built for real-time conversation using voice input and output. It integrates speech recognition, a conversational AI model, and text-to-speech—all in a streamlined browser-based interface using Streamlit.

---

## Features

- Records microphone input for 10 seconds.
- Converts speech to text using Vosk (offline speech-to-text).
- Sends recognized text to a local Mistral model via the Ollama API.
- Speaks the assistant’s response using pyttsx3.
- Displays conversation history in a web-based chat interface.

---

## Setup & Run Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/SujDev05/NOVA-Chatbot.git
cd NOVA-Chatbot
```

### 2. Set Up a Virtual Environment

```bash
python3 -m venv myenv
source myenv/bin/activate   # On Windows: myenv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install streamlit pyttsx3 vosk sounddevice openai
```

### 4. Download the Vosk Model

Download the small English model from [Vosk GitHub](https://alphacephei.com/vosk/models)

Extract it and place it in the project directory as `vosk-model-small-en-us-0.15`.

Make sure the model path in `_STT` class matches this directory.

### 5. Configure Ollama API

Ensure the Ollama server is running locally:

- URL: `http://localhost:11434/v1`
- API Key: `ollama`

You can modify this in the `Conversation` class inside `nova_app.py`.

### 6. Run the Application

```bash
streamlit run nova_app.py
```

Open the browser at the given URL (typically http://localhost:8501).

Click “Process Audio” to begin voice interaction.

---

## Notes

- Ensure microphone access is granted.
- pyttsx3 uses system voices and may behave differently across platforms.
- Ollama must be running before starting the assistant.

---

## License

This project is open source and available under the MIT License.


## Author

This project is done by Sujana S
