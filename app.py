from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import random
import string
import warnings
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime
import re

# Suppress warnings
warnings.filterwarnings('ignore')

# Download NLTK Data
nltk.download('punkt')
nltk.download('wordnet')

# Initialize NLTK resources
lemmer = WordNetLemmatizer()

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

# Greeting inputs and responses
GREETING_INPUTS = ["hi", "hy", "hello", "hey", "good morning", "good afternoon", "good evening"]
EXIT_INPUTS = {"bye", "exit", "quit", "thanks", "thank you"}


# Time-based greeting function
def get_time_based_greeting():
    current_hour = datetime.now().hour
    if current_hour < 12:
        return "Good morning"
    elif 12 <= current_hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"

def greeting(sentence):
    # Check if the whole sentence is in GREETING_INPUTS
    if sentence.lower() in GREETING_INPUTS:
        time_based_greeting = get_time_based_greeting()
        options = ("How may I help you? Select one of the following options:<br>"
                   "1) Sign up support<br>"
                   "2) Log in support<br>"
                   "3) Forgot password<br>"
                   "4) Payment for parking<br>"
                   "5) Payment for Landrates <br>"
                   "6) Payment for Cess <br>"
                   "7) Payment for PSV <br>"
                   "8) Payment for House Rent <br>"
                   "9) Payment for Way leaves <br>"
                   "10) Hawkers")
        return f"{time_based_greeting}! {options}"
    return None

# Response generation function
def response(user_response, sent_tokens, TfidfVec, threshold=0.2):
    robo_response = ''
    
    sent_tokens.append(user_response)
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]

    if req_tfidf < threshold:
        robo_response = ("I'm sorry, I don't understand your request<br> How may I help you? To sort you out quickly select from the below options:<br>"
                         "1) Sign up support<br>"
                         "2) Log in support<br>"
                         "3) Forgot password<br>"
                         "4) parking<br>"
                         "5) Landrates <br>"
                         "6) Cess <br>"
                         "7) PSV <br>"
                         "8) House Rent <br>"
                         "9) Way leaves <br>"
                         "10) Hawkers <br>"
                         "11) Markets")
    else:
        robo_response = sent_tokens[idx]
    sent_tokens.pop()

    # Format the response by replacing keywords with HTML line breaks using regex
    formatted_response = re.sub(r'\b(step|press|For)\b', r'<br>\1', robo_response, flags=re.IGNORECASE)

    return formatted_response

# Flask app initialization
app = Flask(__name__, static_folder='./txt-base64-chat-page/dist/assets', template_folder='./txt-base64-chat-page/dist')
CORS(app)  

# Load corpus
with open('data.txt', 'r', errors='ignore') as f:
    raw = f.read().lower()
    sent_tokens = nltk.sent_tokenize(raw)

# Initialize TF-IDF Vectorizer
TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english', max_df=0.85, min_df=2, ngram_range=(1, 2))

# Define detailed instructions for each option
option_responses = {
    "1": ("Sign up<br><br>Please follow the following instructions for a successful sign up:<br>"
          "Step 1: Click the \"Sign Up\" button (top right) and enter your details<br>"
          "Step 2: Enter your email, click \"Send OTP,\" check your email for the code, and click \"Verify\"<br>"
          "Step 3: Enter your phone number, click \"Send OTP,\" check your SMS for the code, and click \"Verify\""),

    "2": ("Log In <br>"
          "Step 1: Click on the log in button on top.<br>"
          "Step 2: Fill in your email address and your password and click log in."), 

    "3": (" Forgot Password<br>"
          "Step 1: Click on the forgot password button on top.<br>"),

    "4": ("Parking <br>"
          "For App users <br>"
          "Step 1: Log in <br>"
          "Step 2: Select Access Parking Module<br>"
          "Step 3: Click Add Vehicle <br>"
          "Step 4: Enter your plate number (no spaces) and vehicle category, then click Add <br>"
          "Step 5: Click Submit <br>"
          "Step 6: Select the added vehicle, choose your payment period (daily, monthly, etc) <br>"
          "Step 7: Choose a parking zone and Lipa via Mpesa Express or Mpesa <br>"
          "Access parking system For non-app users (USSD users): <br>"
          "Step 1: Dial *282#  <br>"
          "Step 2: Select 1: My Services  <br>"
          "Step 3: Select 1: Parking <br>"
          "Step 4: Select 2: Pay for Existing (or 1 for New) <br>"
          "Step 5: Choose vehicle, period, and zone <br>"
          "Step 6: Confirm and enter Mpesa PIN <br>"),

    "5": ("Landrates <br>"
          "Step 1: After Logging in select land rates module <br>"
          "Step 2: Top right select 'pay for land service' <br>"
          "Step 3: Choose any service you want to pay for land <br>"
          "Step 4: Fill in all the necessary information and click next <br>"
          "Step 5: Upload all the necessary documnts and click finish <br>"
          "Step 6: For Land transfer Please select Land Usage and proceed to payment <br>"
          "Step 7: For Land clearance Please select clearance certificate fee and proceed to payment <br>"
          "Step 8: For Land sub division fee Please select Sub-division fees and proceed to payment"),

    "6": ("Payment for Cess <br>"
          "Step 1: After Logging in select Cess module <br>"
          "Step 2: Click on New Application <br>"
          "Step 3: Fill in the details <br>"
          "Step 4: Click on the check box <br>"
          "Step 5: Click on the	submit button <br>"
          "Step 6: Click on pay and proceed to payment"),

    "7": ("Payment for PSV Levy <br>"
          "Step 1: After Logging in select PSV Levy module <br>"
          "Step 2: Click add vehicle <br>"
          "Step 3: Enter your number plate and click the blue box button to add your number plate <br>"
          "Step 4: Insert another number plate and click the submit button <br>"
          "Step 5: Click on the green button to make payment <br>"
          "Step 6: After payment click on the blue button to dowload your sticker and click on the red button to delete your vehicle"),

    "8": ("Payment for House Rent <br>"
          "Step 1: After Logging in select House Rent module <br>"
          "Step 2: View a list of all registered houses under your details <br>"
          "Step 3: Click the purple icon on the right to view your house rent statement <br>"
          "Step 4: Click the green button writen pay to make online payment <br>"
          "Step 5: Enter the phone number you wish to make payments from and click send payment request.You will receive an mpesa STK push to insert your pin number and complete the transaction <br>"
          "Step 6: Upon successful payment, you will be redirected back to your registered houses <br>"
          "Step 7: Click on my receipt to view a copy of your receipt or to download your receipt"),

    "9": ("Payment for Wayleaves <br>"
          "Step 1: After Logging in select Wayleaves module <br>"
          "Step 2: Click the blue eye icon button to view the application details <br>"
          "Step 3: Click the 'Download structure file' to download the application <br>"
          "Step 4: Click the button in red to 'reject' or the button in blue to 'approve' the application <br>"
          "Step 5: In Receipt page you can click the filter button to use any preferences <br>"
          "Step 6: Click the purple and green button to export as pdf or excel <br>"
          "Step 8: Click on the blue eye icon to view or download the receipt <br>"
          "Step 9: Follow the same from step 5 to step 8 for bills and licenses"),

    "10": ("Hawkers <br>"
           "Step 1: After Logging in select Hawking module <br>"
           "Step 2: Click the search button to filter hawkers report <br>"
           "Step 3: Click the purple or green button to download hawkers collection report <br>"
           "Step 4: Go through above process 2 and process 3 to access hawkers zonal report"),

    "11": ("Markets <br>"
           "Step 1: After Logging in select Markets module <br>"
           "Step 2: Click on the purple icon to view the statement <br>"
           "Step 3: Click the green icon written pay to pay for your stall <br>"
           "Step 4: Proceed to payment")

}

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message").lower().strip()
    print(f"Received message: {user_message}")

    # Check if the user input is a single alphabetic word, excluding greetings and exit phrases
    if len(user_message.split()) == 1 and user_message.isalpha() and user_message not in GREETING_INPUTS and user_message not in EXIT_INPUTS:
        bot_response = "I'm sorry, I don't understand. Please select one of the options below:<br>" \
                       "1) Sign up support<br>" \
                       "2) Log in support<br>" \
                       "3) Forgot password<br>" \
                       "4) Payment for parking<br>" \
                       "5) Payment for Landrates <br>" \
                       "6) Payment for Cess <br>" \
                       "7) Payment for PSV <br>" \
                       "8) Payment for House Rent <br>" \
                       "9) Payment for Way leaves <br>" \
                       "10) Hawkers <br>" \
                       "11) Markets"
        further_help_message = ""
    elif user_message in GREETING_INPUTS:
        bot_response = greeting(user_message)
        further_help_message = ""
    elif user_message in EXIT_INPUTS:
        bot_response = "Bye! Take care." if user_message not in {"thanks", "thank you"} else "You are welcome!"
        further_help_message = ""
    elif user_message in option_responses:
        bot_response = option_responses[user_message]
        further_help_message = ""
    elif "wayleaves" in user_message:
        bot_response = (
            "Step 1: After Logging in select Wayleaves module <br>"
            "Step 2: Click the blue eye icon button to view the application details <br>"
            "Step 3: Click the \"Download structure file\" to download the application <br>"
            "Step 4: Click the button in red to \"reject\" or the button in blue to \"approve\" the application <br>"
            "Step 5: In Receipt page you can click the filter button to use any preferences <br>"
            "Step 6: Click the purple and green button to export as pdf or excel <br>"
            "Step 8: Click on the blue eye icon to view or download the receipt <br>"
            "Step 9: Follow the same from step 5 to step 8 for bills and licenses."
        )
        further_help_message = ""
    else:
        bot_response = response(user_message, sent_tokens, TfidfVec)
        
        step_pattern = re.compile(r'(\d+\.\s|\•|\-|\*|step\s\d+)', re.IGNORECASE)
        further_help_message = ("How much further may I help you? type any option so I can sort you out quickly:<br>"
                                "1) Sign up support<br>"
                                "2) Log in support<br>"
                                "3) Forgot password<br>"
                                "4) Payment for parking<br>"
                                "5) Payment for Landrates <br>"
                                "6) Payment for Cess <br>"
                                "7) Payment for PSV <br>"
                                "8) Payment for House Rent <br>"
                                "9) Payment for Way leaves <br>"
                                "10) Hawkers <br>"
                                "11) Markets") if step_pattern.search(bot_response) else ""

    return jsonify({
        "response": bot_response.strip(),
        "further_help": further_help_message
    })

# entry point to app
@app.route('/')
def home_page():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
