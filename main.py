import streamlit as st
from streamlit_option_menu import option_menu

import firebase_admin
#from dotenv import load_dotenv
from PIL import Image
import login
import home
import ripplellm
from llama_index.llms.ollama import Ollama
import time
#from prompt import firePrompt
#load_dotenv()

st.set_page_config(page_title = "Ripple Bot", initial_sidebar_state='expanded')


st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: white;
    }
</style>
""", unsafe_allow_html=True)


class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):

        self.apps.append({
            "title": title,
            "function": func
        })
        
def run():
        # app = st.sidebar(
        with st.sidebar:   
            img = Image.open( "ripplelogo.png")
            st.image(img, width =250)
            app = option_menu(
                menu_title='Main Menu',
                options=['Home','Login', "AI Mental WellBeing ChatBot"],
                icons=['house-fill','person-circle'],
                menu_icon='chat-text-fill',
                default_index=0,
                styles={
                    "container": {"padding": "0!important","background-color":'#660000'},
                    "icon": {"color": "blue", "font-size": "20px"}, 
                    "menu_title":{"background-color": "blue"} ,    
                    "nav-link": {"color":"white","font-size": "20px", "text-align": "center", "margin":"0px", "--hover-color": "#660000"},
                    "nav-link-selected": {"background-color": "green"},}
            )
        

        
        if app =="Home":
            home.app()
        if app == "Login":
            login.app()         
        if app == "AI Mental WellBeing ChatBot":
            ripplellm.app()
           
                 

run()
