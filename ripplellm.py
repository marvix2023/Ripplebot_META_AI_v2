import streamlit as st
import time
from prompt import firePrompt
import requests
from langchain_community.llms import Ollama
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
import PyPDF2


#load the pdf files from the path
loader = DirectoryLoader('data/',glob="*.pdf",loader_cls=PyPDFLoader)
signpost_data = loader.load()
#split text into chunks
text_splitter  = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
text_chunks = text_splitter.split_documents(signpost_data)

#create embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                   model_kwargs={'device':"cpu"})

#vectorstore
vector_store = FAISS.from_documents(text_chunks,embeddings)




def getAvatar(role):
    if role == 'assistant':
        return "ripple_bot_logo.png"
    else :
        return "llama-logo2.png"

def getContext():
    res = ""
    for item in st.session_state.messages[:-1]:
        res = res + f"role : {item['role']} content : {item['content']}\n"
    return res
def app():
        with st.sidebar:
            st.info(":red[Feel free to Chat with me! I am an AI Chatbot who cares about your mental wellbeing powered by Meta AI]")    
        
        st.markdown('###   I am Your Mental Health First Aider(AI-MHFA) Bot 🤖 Powered by Meta AI', unsafe_allow_html=True)

        
        if 'messages' not in st.session_state:
            st.session_state.messages = []

        #if 'temp' not in st.session_state:
            #st.session_state.temp = 0
            
        with st.chat_message(name="assistant", avatar='ripple_bot_logo.png'):
            st.warning("⚠️ Please note: I am an AI bot, not a human. While I can assist you with your queries, my responses are generated by artificial intelligence. Always consult with a human professional for critical or personal matters.")
            st.markdown('### Start Chatting with me! who cares about your mental wellbeing!')
            
            
        for message in st.session_state.messages:
            with st.chat_message(name=message["role"], avatar=getAvatar(message["role"])):
                st.markdown(f'{message["content"]}')
        
        if prompt := st.chat_input(placeholder="Type your question about mental wellbeing here..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message(name="user", avatar='llama-logo2.png'):
                st.markdown(prompt)
            
            with st.chat_message(name='assistant', avatar='ripple_bot_logo.png'):
                message_placeholder = st.empty()
                full_response = ""
                with st.spinner(text="Thinking... 💭💭💭"):
                    raw = firePrompt(prompt)
                    response = str(raw)
                    # Simulate stream of response with milliseconds delay
                    for chunk in response.split():
                        full_response += chunk + " "
                        time.sleep(0.05)
                        # Add a blinking cursor to simulate typing
                        message_placeholder.markdown(full_response + "▌", unsafe_allow_html=True)
                    message_placeholder.markdown(f'#### {full_response}', unsafe_allow_html=True)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
# To run the app
if __name__ == "__main__":
    app()
