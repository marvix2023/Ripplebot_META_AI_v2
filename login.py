import streamlit as st
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from firebase_admin import auth
import json
import requests
import time

cred = credentials.Certificate("ripplebot-b95fb-firebase-adminsdk-o5d64-42fe08a2e4.json")
#firebase_admin.initialize_app(cred)
    
def app():
# Usernm = []
    with st.sidebar:
        st.info(":red[This page is to Login/Sign up with your work email address and password to chat with Ripple's custom Bot designed by Ripple's team who are expertise in Mental Well-being of employees in your organisation powered by Meta AI]")
    st.title('Welcome to Chat with :blue[Ripple AI Bot] :robot_face:')

    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail = '' 
    if "messages" not in st.session_state:
        st.session_state.messages = []
    #if "show_final_msg1" not in st.session_state:
        #st.session_state["show_final_msg1"] = False


    #for message in st.session_state.messages:
        #with st.chat_message["role"]:
            #st.markdown(message["content"])
    

    def sign_up_with_email_and_password(email, password, username=None, return_secure_token=True):
        try:
            rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signUp"
            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": return_secure_token
            }
            if username:
                payload["displayName"] = username 
            payload = json.dumps(payload)
            r = requests.post(rest_api_url, params={"key": "AIzaSyApr-etDzcGcsVcmaw7R7rPxx3A09as7uw"}, data=payload)
            try:
                return r.json()['email']
            except:
                st.warning(r.json())
        except Exception as e:
            st.warning(f'Signup failed: {e}')

    def sign_in_with_email_and_password(email=None, password=None, return_secure_token=True):
        rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"

        try:
            payload = {
                "returnSecureToken": return_secure_token
            }
            if email:
                payload["email"] = email
            if password:
                payload["password"] = password
            payload = json.dumps(payload)
            print('payload sigin',payload)
            r = requests.post(rest_api_url, params={"key": "AIzaSyApr-etDzcGcsVcmaw7R7rPxx3A09as7uw"}, data=payload)
            try:
                data = r.json()
                user_info = {
                    'email': data['email'],
                    'username': data.get('displayName')  # Retrieve username if available
                }
                return user_info
            except:
                st.warning(data)
        except Exception as e:
            st.warning(f'Signin failed: {e}')

    def reset_password(email):
        try:
            rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode"
            payload = {
                "email": email,
                "requestType": "PASSWORD_RESET"
            }
            payload = json.dumps(payload)
            r = requests.post(rest_api_url, params={"key": "AIzaSyApr-etDzcGcsVcmaw7R7rPxx3A09as7uw"}, data=payload)
            if r.status_code == 200:
                return True, "Reset email Sent"
            else:
                # Handle error response
                error_message = r.json().get('error', {}).get('message')
                return False, error_message
        except Exception as e:
            return False, str(e)

    # Example usage
    # email = "example@example.com" 
   
    def typewriter(text: str, speed =12):
        tokens = text.split()
        container = st.empty()
        for index in range(len(tokens) + 1):
            curr_full_text = " ".join(tokens[:index])
            container.markdown(curr_full_text)
            time.sleep(1/speed)    
    
    def suicide_msg():
        typewriter("I am really sorry to hear that you are feeling this way, it can be so hard to see a way out sometimes.\
                                The fact that you have acknowledged this and reached out is really encouraging. I want to help and keep you safe.\
                                If you want to speak to someone urgently, please ring 999, or contact the Samaritans on 116-123, you’ll be able to talk to someone directly.\
                                They are trained professionals who care and listen non-judgmentally.I know it’s scary, but your feelings are valid and your life matters.")
        st.link_button("1. Suicidal Thoughts - here are some resources that may help","https://www.samaritans.org/how-we-can-help/if-youre-having-difficult-time/i-want-kill-myself/",type ="primary")
        st.link_button("2. Suicidal Thoughts - here are some resources that may help","https://www.mind.org.uk/media-a/6164/suicidal-feelings-2020.pdf",type ="primary")
            
   
                                                                                                           
    #def suicidal_thoughts():
         # attempt = st.radio("🤖 Thank you for telling me that. I’m so sorry to hear you’re going through this.  Have you thought of how you would do that?", ('Yes', 'No'),index = None)
          #if attempt == "Yes": 
               # resource = st.radio("🤖 Please can I ask, do you have the resources to follow through on that plan?",('Yes','No'), index=None)
                #if resource == "Yes" or resource == "No":
                    #atmpt_thought = st.radio("🤖 Have you attempted to end your life before?", ("Yes","No"), index = None)
                    #if atmpt_thought:
                      #suicide_msg()
                        
                        
          #elif attempt == "No":
             #atmpt_thought = st.radio("🤖 Have you attempted to end your life before?", ("Yes","No"), index = None)
             #if atmpt_thought:
                  #suicide_msg() 
                                                          
                    

    def f(): 
        try:
            # user = auth.get_user_by_email(email)
            # print(user.uid)
            # st.session_state.username = user.uid
            # st.session_state.useremail = user.email
 
            userinfo = sign_in_with_email_and_password(st.session_state.email_input,st.session_state.password_input)
            st.session_state.username = userinfo['username']
            st.session_state.useremail = userinfo['email']
           
            
            global Usernm
            Usernm=(userinfo['username'])
            
            st.session_state.signedout = True
            st.session_state.signout = True    
  
            
        except: 
            st.warning('Login Failed')

    def t():
        st.session_state.signout = False
        st.session_state.signedout = False   
        st.session_state.username = ''


    def forget():
        email = st.text_input('Email')
        if st.button('Send Reset Link'):
            print(email)
            success, message = reset_password(email)
            if success:
                st.success("Password reset email sent successfully.")
            else:
                st.warning(f"Password reset failed: {message}") 
        
    
        
    if "signedout"  not in st.session_state:
        st.session_state["signedout"] = False
    if 'signout' not in st.session_state:
        st.session_state['signout'] = False    
        

        
    
    if  not st.session_state["signedout"]: # only show if the state is False, hence the button has never been clicked
        choice = st.selectbox('Login/Signup',['Login','Sign up'])
        email = st.text_input('Work Email Address')
        password = st.text_input('Password',type='password')
        st.session_state.email_input = email
        st.session_state.password_input = password

        

        
        if choice == 'Sign up':
            username = st.text_input("Enter your unique employee username")
            
            if st.button('Create my account'):
                # user = auth.create_user(email = email, password = password,uid=username)
                user = sign_up_with_email_and_password(email=email,password=password,username=username)
                
                st.success('Account created successfully!')
                st.markdown('Please Login using your work email and password')
                st.balloons()
        else:
            # st.button('Login', on_click=f)          
            st.button('Login', on_click=f)
            # if st.button('Forget'):
            forget()
            # st.button('Forget',on_click=forget)

    if "signout" not in st.session_state:
        st.session_state.signout = True        


        
    if st.session_state.signout:
                #st.text('Employee Name '+st.session_state.username)
                #st.text('Work Email id: '+st.session_state.useremail)
                
                st.header('Start Your Chat with Ripple AI Bot 😎')
                
                emotion = st.radio("🤖 Hi there! I am here to chat with you about how you are feeling today. How are you getting on?",
                                        ["Please Choose",":smile:[Very Good]", ":slightly_smiling_face: [Good]",":expressionless: [Ok]",":slightly_frowning_face: [ Poor ]",":frowning: [Very Poor]"],index = 0)
                feelmsg = st.write("You feel:", emotion)

                if "Very Poor" in emotion or "Poor" in emotion:
                    st.info("I am really sorry to hear that you have been feeling this way. Reaching out can be tricky, so thanks for reaching out. You are in the right place.")
                elif "Ok" in emotion:
                    st.info("Thanks for sharing how you're feeling! Remember, it's all part of the journey. If there's anything you'd like to talk about or if you need a little pick-me-up, I'm here for you. 😊 Keep going, you are doing great!")
                elif "Very Good" in emotion or "Good" in emotion:
                    st.info("That is wonderful to hear! 🌟 Keep riding that positive wave, and remember, even on the good days, you are making progress. If there's anything else on your mind or if you ever need a little boost, I'm always here to chat. 😊 Stay awesome!")
                else:
                    st.info("I am your supportive mental health first aider powered by AI, Please choose how you are feeling today 👆")       
                
                if emotion:
                    st.write("🤖 Hello 👋 Can I ask if you have spoken to anyone about this?")
                    speak = st.radio("Please tell", ("Yes","No"), index=None, horizontal =True)
                    if speak:
                        feel = st.radio ("🤖 Thanks for telling me that.What best describes how you feel at the moment?",("Low mood", "Numb", "Flat", "Anxious and Worried", "Suicidal Thoughts"), index = None)   
                    
                    # If the user choosen the Suicidal Thoughts
                        if feel == "Suicidal Thoughts":
                            suicide_msg()
                        else: 
                     
                            period = st.radio("🤖 Okay, thanks for letting me know. Do you mind if I ask you how long you’ve been feeling this way?", ['A day','A few days','A week','A couple of weeks','A month','Longer'], index = None, key =6)
                            if period in ['A day' , 'A few days' , 'A week' , 'A couple of weeks' , 'A month' , 'Longer']:
                                  st.write("🤖That sounds really tough, I appreciate you sharing that with me.")
                                  st.write("🤖Dealing with difficult feelings can often have a negative impact on your day-to-day life. What does that look like for you?")
                                   
                                   
                                  feel2 = st.multiselect("🤖 Choose from here",
                                                   ['Isolating yourself','Tired','Eating more/less', 'Stressed','Upset','Unhealthy decisions','Feeling like a burden', 'Irritable','Angry'])
                                 
                                  if feel2:
                                      time.sleep(2)
                                      st.info("It is only natural to feel like this - your problems are real and valid. \
                                                    Reaching out can be tricky when you are not feeling great, so good on you for reaching out.\
                                                    You are in the right place.")
                                      
                                      suicide_feel = st.checkbox("Select this box if you have Suicidal Thoughts")
                                      if suicide_feel:
                                        suicide_msg()
                                      else:   
                                  #for feeling in feel2:
                                      #if feeling in ['Isolating yourself','Tired','Eating more/less', 'Stressed','Upset','Unhealthy decisions','Feeling like a burden', 'Irritable','Angry']:
                                           #if feeling == True:
                                                
                                            atmpt = st.radio("🤖 Is there anything else I can do at this stage?",("No,Thanks", "Yes,Please"),index = None)
                                          
                                            if atmpt == "No,Thanks":
                                                typewriter("Thank you so much for reaching out to me. I know it feels incredibly difficult now, but things do get better.")
                                                time.sleep(1)
                                            if atmpt == "Yes,Please":
                                                    signpost = st.multiselect("When you are ready, could you tell me a little bit more about what’s making you feel this way?",
                                                                             ["Workload", "Money", "Work relationships", "Personal relationships", "Physical Health", "Mental Health",
                                                                            "Childcare","Sleep","Menopause", "Housing", "Caring Responsibilities","Aging relatives","Bereavment",
                                                                            "Loss significant Change","Romantic realtionships","Anxiety", "Low mood", "Flat mood", "Eating Disorder",
                                                                            "Stress","Alcohol & Substance Issues", "Loneliness & Isolation","Suicidal Thoughts","Self Harm", "Changes in Thinking"],key="signpost_final_message")
                                                    time.sleep(3)
                                                    if signpost:
                                                        typewriter("Thanks for telling me. I am sorry to hear you are going through this.\
                                                                            It is important to make use of your support network.\
                                                                                If you feel like you can, perhaps check-in with a friend or family member, it can really help sometimes.\
                                                                                Remember what they say, a problem shared is a problem halved.\
                                                                                By talking to me, you have made the first step already.You know there is a lot of support out there that might help.\
                                                                                Here are a few suggestions you could maybe try.Have a look if you feel up to it.\
                                                                                There is also lots of advice from your Employee Assistance Programme, it is all totally confidential and free.\
                                                                                Thanks for chatting with me today. Take care, give yourself a break, and remember that I'm here if you need anything.")
                                                           
                                                    for option in signpost:
                                                                    
                                                                        if option == "Workload":
                                                                 
                                                                                st.link_button("1.Workload - here are some resources that may help","https://www.mind.org.uk/information-support/tips-for-everyday-living/how-to-be-mentally-healthy-at-work/work-and-stress/#ProblemsWithYourWorkload",type ="primary") 
                                                                            
                                                                        if option == "Money":
                                                                                st.link_button("1. Money - here are some resources that may help","https://www.moneyhelper.org.uk/en/homes",type ="primary")
                                                                                st.link_button("2. Money - here are some resources that may help","https://www.stepchange.org/",type ="primary")
                                                                            
                                                                        if option == "Work relationships":
                                                                                st.link_button(" 1. Work relationships - here are some resources that may help ","https://www.acas.org.uk/how-to-raise-a-problem-at-work#:~:text=explain%20what%20the%20problem%20is%20and%20what%20you,manager%20should%20allow%20you%20to%20explain%20the%20problem.",type ="primary")
                                                                            
                                                                        if option == "Personal relationships":
                                                                                st.link_button("1. Personal relationships - here are some resources that may help","https://www.nhs.uk/every-mind-matters/lifes-challenges/maintaining-healthy-relationships-and-mental-wellbeing/",type ="primary")
                                                                                st.link_button("2. Personal relationships - here are some resources that may help","https://www.relate.org.uk/",type ="primary")
                                                                                st.link_button("3. Personal relationships - here are some resources that may help","https://www.citizensadvice.org.uk/family/",type ="primary")
                                                                            
                                                                        if option == "Physical Health":
                                                                                st.link_button("1.Physical Health - here are some resources that may help","https://www.mentalhealth.org.uk/explore-mental-health/a-z-topics/physical-health-and-mental-health",type ="primary")
                                                                            
                                                                        if option == "Mental Health": 
                                                                                st.link_button("1.Mental Health - here are some resources that may help","https://www.mentalhealth.org.uk/explore-mental-health/a-z-topics/physical-health-and-mental-health",type ="primary")
                                                                                st.link_button("2.Mental Health - here are some resources that may help","https://www.nhs.uk/every-mind-matters/supporting-others/helping-others/",type ="primary")
                                                                                st.link_button("3.Mental Health - here are some resources that may help","https://www.mind.org.uk/media/8540/supporting-yourself-while-caring-for-someone-2021.pdf",type ="primary")
                                                                            
                                                                        if option == "Childcare": 
                                                                                st.link_button("1.Childcare - here are some resources that may help ","https://www.gov.uk/help-with-childcare-costs",type ="primary")
                                                                                st.link_button("2.Childcare - here are some resources that may help ","https://workingfamilies.org.uk/s",type ="primary")
                                                                            
                                                                        if option == "Sleep": 
                                                                                st.link_button("1.Sleep - here are some resources that may help ","https://www.nhs.uk/every-mind-matters/mental-health-issues/sleep/",type ="primary")
                                                                                st.link_button("2.Sleep - here are some resources that may help ","https://www.mind.org.uk/media-a/5827/sleep-problems-2020.pdf",type ="primary")
                                                                            
                                                                        if option == "Menopause": 
                                                                                st.link_button("1.Menopause - here are some resources that may help ","https://www.themenopausecharity.org//",type ="primary")
                                                                                st.link_button("2.Menopause - here are some resources that may help  ","https://www.nhs.uk/conditions/menopause/",type ="primary")
                                                                            
                                                                        if option == "Housing":
                                                                                st.link_button("1.Housing - here are some resources that may help ","https://www.moneyhelper.org.uk/en/homes",type ="primary")
                                                                                st.link_button("2.Housing - here are some resources that may help ","https://www.mind.org.uk/information-support/guides-to-support-and-services/housing/support-for-housing-problems/",type ="primary")
                                                                                st.link_button("3.Housing - here are some resources that may help ","https://www.shelter.org.uk/",type ="primary")
                                                                                st.link_button("4.Housing - here are some resources that may help ","https://www.citizensadvice.org.uk/housing/",type ="primary")
                                                                            
                                                                        if option == "Caring Responsibilities":
                                                                                st.link_button("1.Caring Responsibilities - here are some resources that may help","https://www.nhs.uk/conditions/social-care-and-support-guide/caring-for-children-and-young-people/how-to-care-for-children-with-complex-needs/",type ="primary")
                                                                                st.link_button("2.Caring Responsibilities - here are some resources that may help","https://www.first4adoption.org.uk/adoption-support/",type ="primary")
                                                                                st.link_button("3.Caring Responsibilities - here are some resources that may help","https://www.familylives.org.uk/",type ="primary")
                                                                            
                                                                        if option == "Aging relatives":
                                                                                st.link_button("1.Aging relatives - here are some resources that may help","https://www.familylives.org.uk/",type ="primary")
                                                                            
                                                                        if option == "Bereavement":
                                                                                st.link_button("1. Bereavement - here are some resources that may help","https://www.thegoodgrieftrust.org/",type ="primary")
                                                                                st.link_button("2. Bereavement - here are some resources that may help","https://www.mind.org.uk/media-a/3361/bereavement-2019-for-pdf-download.pdf",type ="primary")
                                                                                st.link_button("3. Bereavement - here are some resources that may help","https://uksobs.com/",type ="primary")
                                                                                st.link_button("3. Bereavement - here are some resources that may help","https://www.cruse.org.uk/",type ="primary")                    
                                                                            
                                                                        if option == "Loss significant Change":
                                                                                st.link_button("1. Loss significant Change - here are some resources that may help","https://www.gov.uk/calculate-your-redundancy-pay",type ="primary")
                                                                                st.link_button("2. Loss significant Change - here are some resources that may help","https://www.ageuk.org.uk/information-advice/work-learning/retirement/preparing-emotionally-for-retirement/",type ="primary")
                                                                                st.link_button("3. Loss significant Change - here are some resources that may help","https://www.bhf.org.uk/informationsupport/heart-matters-magazine/wellbeing/retirement/retirement-tips",type ="primary")
                                                                            
                                                                        if option == "Aging relatives":
                                                                                st.link_button("1.Aging relatives - Click to view AI suggested signpost","https://www.carersuk.org/media/4bomxzth/cuk-looking-after-someone-2022-23-england.pdf",type ="primary")
                                                                            
                                                                        if option == "Romantic relationships":
                                                                                st.link_button("1. Romantic relationships - here are some resources that may help","https://www.nhs.uk/every-mind-matters/lifes-challenges/maintaining-healthy-relationships-and-mental-wellbeing/",type ="primary")
                                                                                st.link_button("2. Romantic relationships - here are some resources that may help","https://www.relate.org.uk/",type ="primary")
                                                                                st.link_button("3. Romantic relationships - here are some resources that may help","https://www.citizensadvice.org.uk/family/",type ="primary")                    
                                                                                                
                                                                        if option == "Anxiety":
                                                                                st.link_button("1. Anxiety - here are some resources that may help","https://www.nhs.uk/every-mind-matters/mental-health-issues/anxiety/",type ="primary")
                                                                                st.link_button("2. Anxiety - here are some resources that may help","https://nopanic.org.uk/",type ="primary")
                                                                                st.link_button("3. Anxiety - here are some resources that may help","https://www.nhs.uk/mental-health/conditions/anxiety/",type ="primary")                          
                                                                        if option == "Low mood":
                                                                                st.link_button("1.Low mood - here are some resources that may help","https://www.nhs.uk/every-mind-matters/mental-health-issues/low-mood/",type ="primary")
                                                                                st.link_button("2.Low mood - here are some resources that may help","https://www.nhs.uk/mental-health/self-help/guides-tools-and-activities/mental-wellbeing-audio-guides//",type ="primary")                    
                                                                        if option == "Flat mood":
                                                                                st.link_button("1. Flat mood - here are some resources that may help","https://www.mind.org.uk/information-support/types-of-mental-health-problems/dissociation-and-dissociative-disorders/about-dissociation/",type ="primary")                    
                                                                                                
                                                                        if option == "Eating Disorder":
                                                                                st.link_button("1. Eating Disorder - here are some resources that may help","https://www.nhs.uk/mental-health/feelings-symptoms-behaviours/behaviours/eating-disorders/overview/",type ="primary")
                                                                                st.link_button("2. Eating Disorder - here are some resources that may help","https://www.beateatingdisorders.org.uk/",type ="primary")                               
                                                                            
                                                                        if option == "Stress":
                                                                                st.link_button("1. Stress - here are some resources that may help","https://www.stress.org.uk/",type ="primary")                               
                                                                                                        
                                                                        if option == "Alcohol & Substance Issues":
                                                                                st.link_button("1. Alcohol & Substance Issues - here are some resources that may help","https://www.nhs.uk/live-well/addiction-support/drug-addiction-getting-help/",type ="primary")
                                                                                st.link_button("2. Alcohol & Substance Issues - here are some resources that may help","https://humankindcharity.org.uk/drug-and-alcohol-recovery/",type ="primary")
                                                                                st.link_button("3. Alcohol & Substance Issues - here are some resources that may help","https://www.talktofrank.com/",type ="primary")
                                                                                st.link_button("3. Alcohol & Substance Issues - here are some resources that may help","https://www.nhs.uk/live-well/alcohol-advice/alcohol-support/",type ="primary")
                                                                                                
                                                                        if option == "Loneliness & Isolation":
                                                                                st.link_button("1. Loneliness & Isolation - here are some resources that may help","https://www.ageuk.org.uk/northern-ireland/information-advice/health-wellbeing/loneliness/how-to-overcome-loneliness/",type ="primary")
                                                                                st.link_button("2. Loneliness & Isolation - here are some resources that may help","https://www.mentalhealth.org.uk/sites/default/files/2022-06/MHAW22-Loneliness-Help-and-Advice.pdf",type ="primary")                               
                                                                            
                                                                        if option == "Suicidal Thoughts":
                                                                                st.link_button("1. Suicidal Thoughts - here are some resources that may help","https://www.samaritans.org/how-we-can-help/if-youre-having-difficult-time/i-want-kill-myself/",type ="primary")
                                                                                st.link_button("2. Suicidal Thoughts - here are some resources that may help","https://www.mind.org.uk/media-a/6164/suicidal-feelings-2020.pdf",type ="primary")                               
                                                                                                                    
                                                                        if option == "Self Harm":
                                                                                st.link_button("1. Self Harm - here are some resources that may help","https://www.nhs.uk/mental-health/feelings-symptoms-behaviours/behaviours/self-harm/",type ="primary")
                                                                                st.link_button("2. Self Harm - here are some resources that may help","https://harmless.org.uk/",type ="primary")                               
                                                                        
                                                                        if option == "Changes in Thinking":
                                                                                st.link_button("1. Changes in Thinking - here are some resources that may help","https://www.nhs.uk/mental-health/conditions/psychosis/overview/",type ="primary")   
                                                             
                                         
                                    
                st.button('Sign out', on_click=t) 
 
         
    def ap():
        st.write('Posts')
