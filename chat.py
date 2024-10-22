import streamlit as st
from streamlit_chat import message
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import CTransformers
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain_community.llms import Ollama
import PyPDF2
import ollama
#load the pdf files from the path
loader = DirectoryLoader('data/',glob="*.pdf",loader_cls=PyPDFLoader)
resume_text = loader.load()

#split text into chunks
text_splitter  = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
text_chunks = text_splitter.split_documents(resume_text)

#create embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                   model_kwargs={'device':"cpu"})

#vectorstore
vector_store = FAISS.from_documents(text_chunks,embeddings)

# Initialize session state for conversation history and resume analysis
if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How can I assist you with your mental wellbeing today?"}]
if 'resume_analysis' not in st.session_state:
    st.session_state.resume_analysis = ""
if 'resume_uploaded' not in st.session_state:
    st.session_state.resume_uploaded = False
if resume_text and  not st.session_state.resume_uploaded:
      st.session_state.resume_analysis = resume_text
      st.session_state.resume_uploaded = True 


      st.session_state.messages.append({
              "role": "assistant",
              "content": "Thank you for asking your query."
          })
      st.chat_message("assistant", avatar="🤖").write(st.session_state.messages[-1]["content"])
      
          # Analyze resume
      with st.spinner("Thinking..."):
              analysis_response = ollama.chat(model='olamma3.2', messages=[
                  {"role": "user", "content": f"Analyze this query:\n\n{resume_text}"}
              ])
              analysis_text = analysis_response['message']['content']
          
      st.session_state.messages.append({
              "role": "assistant",
              "content": f"Here's is the anaswer:\n\n{analysis_text}"
          })
      st.chat_message("assistant", avatar="🤖").write(st.session_state.messages[-1]["content"])
      
      # Display chat history
for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.chat_message(msg["role"], avatar="🧑‍💻").write(msg["content"])
        else:
            st.chat_message(msg["role"], avatar="🤖").write(msg["content"])

# Define a function to generate a response with prompt engineering and spinner
def generate_response(prompt):
    # Keywords related to career guidance
    career_keywords = [ "workplace", "mental well-being"]
    # Check if the question is career-related
    if any(keyword in prompt.lower() for keyword in career_keywords):
        # Create a context-rich prompt for the model
        prompt_with_context = f"""Context: You are a highly knowledgeable career assistant. Your task is to provide insightful advice on mental wellbeing at workplace and in all other scenarios.
        User Query: {prompt} Please provide a detailed and helpful response."""

        with st.spinner("Generating response..."):
            response = ollama.chat(model='gemma:2b', stream=False, messages=[{"role": "user", "content": prompt_with_context}])
            return response['message']['content']
    else:
        # Response for non-relevant questions
        return "I'm here to assist with answering your query related to your mental wellbeing,  and related topics. Please ask a relevant question about your mental wellbeing."

# Input for user query
if prompt := st.chat_input("Ask me anything about mental wellbeing!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user", avatar="🧑‍💻").write(prompt)
    
    # Generate response based on the filtered input
    response_content = generate_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response_content})
    st.chat_message("assistant", avatar="🤖").write(response_content)







