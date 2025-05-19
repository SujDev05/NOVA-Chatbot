import openai
import streamlit as st
import pyttsx3

if 'message_list' not in st.session_state:
    st.session_state.message_list = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]      

class _TTS:
    def __init__(self):
        self.engine = pyttsx3.init()  # Initialize the text-to-speech engine

    def start(self, text_):
        self.engine.say(text_)  # Queue the text to be spoken
        self.engine.runAndWait()  # Wait for the speech to finish

    def __del__(self):
        # Clean up the engine if needed
        del self.engine

class Conversation:
    client = openai.OpenAI(
        base_url='http://localhost:11434/v1',
        api_key='ollama',  # api_key is required, but unused for local models
    )
    
    def message(self, question):
        q = {
            "role": "user",
            "content": question
        }
        
        st.session_state.message_list.append(q)
        
        response = self.client.chat.completions.create(
            model="mistral",
            messages=st.session_state.message_list
        )
        
        q = {
            "role": "assistant",
            "content": response.choices[0].message.content
        }
        
        st.session_state.message_list.append(q)
        
        return response.choices[0].message.content

if __name__ == "__main__":
    
    st.title('NOVA chat')

    message = st.chat_message("assistant")
    message.write("Hello Sujanax!")

    conversation = Conversation()
    
    prompt = st.chat_input("Ask a question")
    if prompt:
        
        with st.spinner('Thinking...'):
                
            answer = conversation.message(prompt)
            
            tts = _TTS()
            tts.start(answer)  # Speak the assistant's response
            del tts  # Delete the instance to clean up
            
            for l in st.session_state.message_list:
                
                if l['role'] == 'user':
                    with st.chat_message("user"):
                        st.write(l['content'])
                elif l['role'] == 'assistant':
                    with st.chat_message("assistant"):
                        st.write(l['content'])