import streamlit as st


def app():
    with st.sidebar:
        st.info(":red[This is Ripple & Co's Home page to know who they are and how they deliver high quality programmes to increase wellbeing and productivity.]")
    st.subheader('Ripple AI Powered Chatbot is a chat application created for employees to know their mental wellbeing at Workplace.')
    st.info (""" ### Ripple&Co was created for a single purpose: to help people thrive. We believe that simple, every day actions create a positive ripple effect, \
    extending far beyond the individual.We strive to enhance wellbeing so that everyone can live a happy life and be the best version of themselves.\
    We are trusted to deliver high quality programmes to increase wellbeing and productivity.""")
    st.subheader("Reach Us")
    st.info(""" ##### Get in touch to find out how Ripple&Co can help to transform your business.""")
    st.info( """ ##### Call us: 03335330253 """)
    st.info( """ ##### Email: hello@rippleandco.com""")
    st.link_button("Click here to know more about Ripple&Co", "https://www.rippleandco.com/about-us", type = "primary")
    #redirect_button("https://www.rippleandco.com/about-us","Click here to know more about Ripple&Co")

def redirect_button(url: str, text: str= None, color= "#660000"):
    st.markdown(
    f"""
    <a href="{url}" target="_self">
        <div style="
            display: inline-block;
            padding: 1em 2em;
            color: #FFFFFF;
            background-color: {color};
            border-radius: 10px;
            text-decoration: none;">
            {text}
        </div>
    </a>
    """,
    unsafe_allow_html=True
    )

