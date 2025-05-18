from dotenv import load_dotenv
load_dotenv()   

import os
import streamlit as st
import google.generativeai as genai


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load gemini model

model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question,stream=True)
    return response

# Initialize the Streamlit app

st.set_page_config(page_title="Q&A Chatbot", page_icon=":robot_face:") 

st.header("Q&A Chatbot with Gemini")


# Initialize session state for chat history
if "chat_history"not in st.session_state:
    st.session_state["chat_history"]= []

input =st.text_input("Ask a querry:", key="input")
submit =st.button("Ask The Question")

if submit and input:
    response = get_gemini_response(input)
    #Add user question and gemini response to chat history
    st.session_state["chat_history"].append({"You",input})
    st.subheader("The Response is ")
    for chunk in response:
        st.write(chunk.text)
        st.session_state["chat_history"].append({"Gemini",chunk.text})

# Display chat history
st.subheader("Chat History is")
for role,text in st.session_state["chat_history"]:
    st.write(f"{role}:{text}")