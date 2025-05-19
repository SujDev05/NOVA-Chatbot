import openai
import streamlit as st
import pyttsx3
from vosk import Model, KaldiRecognizer
import sounddevice as sd
import json
import queue
import time
import multiprocessing  # Import multiprocessing for separate process handling

# Standalone function for pyttsx3 TTS to avoid pickling issues
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()

# Initialize message list in Streamlit's session state
if 'message_list' not in st.session_state:
    st.session_state.message_list = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# Text-to-Speech class using multiprocessing
class _TTS:
    def __init__(self):
        pass

    def start(self, text_):
        # Run pyttsx3 in a separate process
        process = multiprocessing.Process(target=speak, args=(text_,))
        process.start()
        process.join()  # Wait for the process to complete

# Speech-to-Text class using Vosk with microphone input
class _STT:
    def __init__(self, model_path="/Users/sujana/Documents/AI_project/vosk-model-small-en-us-0.15"):
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.q = queue.Queue()  # Queue to store audio data

    def callback(self, indata, frames, time, status):
        """Callback function to feed audio data to the queue."""
        if status:
            print(status)
        self.q.put(bytes(indata))

    def listen_from_mic(self, duration=10):
        """Capture audio from the microphone for a limited duration."""
        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                               channels=1, callback=self.callback):
            print("Listening...")
            start_time = time.time()
            result_text = ""
            while True:
                if time.time() - start_time > duration:
                    print("Stopped listening after 10 seconds.")
                    break

                if not self.q.empty():
                    data = self.q.get()
                    if self.recognizer.AcceptWaveform(data):
                        result = json.loads(self.recognizer.Result())
                        result_text += result.get("text", "") + " "

            # Get any remaining text from partial recognition
            final_result = json.loads(self.recognizer.FinalResult())
            result_text += final_result.get("text", "")
            
            print("Recognized Text:", result_text)
            return result_text

# Conversation class for interaction with the assistant
class Conversation:
    client = openai.OpenAI(
        base_url='http://localhost:11434/v1',
        api_key='ollama',
    )

    def message(self, question):
        q = {
            "role": "user",
            "content": question
        }

        st.session_state.message_list.append(q)

        # Debugging: Print the recognized question
        print("Recognized Question:", question)

        try:
            response = self.client.chat.completions.create(
                model="mistral",
                messages=st.session_state.message_list
            )

            # Debugging: Print the raw response
            print("API Response:", response)

            q = {
                "role": "assistant",
                "content": response.choices[0].message.content
            }

            st.session_state.message_list.append(q)

            # Return the response content for displaying
            return response.choices[0].message.content
        except Exception as e:
            st.error("Error communicating with the model: {}".format(e))
            return "Sorry, I'm having trouble processing your request."

if __name__ == "__main__":
    
    st.title('NOVA')

    # Display a welcome message from the assistant
    if len(st.session_state.message_list) == 1:
        with st.chat_message("assistant"):
            st.write("Hello Sujana! Click the 'Process Audio' button to start.")

    conversation = Conversation()
    stt = _STT("vosk-model-small-en-us-0.15")  # Path to your Vosk model directory
    tts = _TTS()

    # Button to process audio from the microphone
    if st.button("Process Audio"):
        with st.spinner('Listening ...'):
            # Recognize speech from the microphone for 10 seconds
            prompt = stt.listen_from_mic(duration=10)
            
            if prompt:
                # Print recognized text for debugging
                print("Recognized Text:", prompt)
                with st.spinner('Thinking...'):
                    # Process the recognized text and get a response
                    answer = conversation.message(prompt)
                    
                    # Print assistant's response for debugging
                    print("Assistant's Response:", answer)
                    
                    # Speak the assistant's response
                    tts.start(answer)
                    
                    # Display the conversation history
                    for l in st.session_state.message_list:
                        if l['role'] == 'user':
                            with st.chat_message("user"):
                                st.write(l['content'])
                        elif l['role'] == 'assistant':
                            with st.chat_message("assistant"):
                                st.write(l['content'])
            
            # Limit the message history to prevent performance issues
            if len(st.session_state.message_list) > 10:  # Keep only the last 10 messages
                st.session_state.message_list = st.session_state.message_list[-10:]
