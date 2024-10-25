from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import string
import warnings
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime  # Import datetime module

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
        options = ("How may I help you? type one of the following options:<br>"
                   "Sign up support<br>"
                   "Log in support<br>"
                   "Forgot password<br>"
                   "Payment for parking<br>"
                   "Payment for water")
        return f"{time_based_greeting}! {options}"
    return None

# Initialize session variable to store context
session_context = {
    "last_topic": None,  # Keeps track if the user is asking about parking or water
    "first_message": True  # Tracks whether this is the first user message
}

# Response generation function
import re  # Import regex module

def response(user_response, sent_tokens, TfidfVec, threshold=0.2):
    robo_response = ''

    # Detect if the user is asking about parking or water
    if 'parking' in user_response:
        session_context['last_topic'] = 'parking'  # Store context
        robo_response = ("Please select an option:<br>"
                         "For App users press 1 and press enter<br>"
                         "For USSD users press 2 and press enter")
        return robo_response
    elif 'water' in user_response:
        session_context['last_topic'] = 'water'  # Store context
        robo_response = ("Please select an option:<br>"
                         "For App users press 1 and press enter<br>"
                         "For USSD users press 2 and press enter")
        return robo_response

    # Process the user's selection for parking or water services based on context
    if user_response.strip() == '1':  # App users
        if session_context['last_topic'] == 'parking':
            robo_response = ("Step 1: Log in<br>"
                             "Step 2: Select Access Parking Module<br>"
                             "Step 3: Click Add Vehicle<br>"
                             "Step 4: Enter your plate number and vehicle category<br>"
                             "Step 5: Choose payment period and zone<br>"
                             "Step 6: Pay via Mpesa.")
        elif session_context['last_topic'] == 'water':
            robo_response = ("Step 1: Log in<br>"
                             "Step 2: Select Access Water Module<br>"
                             "Step 3: View and pay your bill online.")
    elif user_response.strip() == '2':  # USSD users
        if session_context['last_topic'] == 'parking':
            robo_response = ("Step 1: Dial *282#<br>"
                             "Step 2: Select 1: My Services<br>"
                             "Step 3: Select 1: Parking<br>"
                             "Step 4: Choose vehicle, period, and zone<br>"
                             "Step 5: Pay via Mpesa.")
        elif session_context['last_topic'] == 'water':
            robo_response = ("Step 1: Dial *282#<br>"
                             "Step 2: Select 1: My Services<br>"
                             "Step 3: Select 2: Water<br>"
                             "Step 4: Confirm and pay via Mpesa.")

    # Default fallback
    else:
        sent_tokens.append(user_response)
        tfidf = TfidfVec.fit_transform(sent_tokens)
        vals = cosine_similarity(tfidf[-1], tfidf)
        idx = vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-2]

        if req_tfidf < threshold:
                            
            robo_response = ("I'm sorry, I don't understand your request. How may I help you? Please type one of the following options:<br>"
                            "Sign up support<br>"
                            "Log in support<br>"
                            "Forgot password<br>"
                            "Pay for parking"
                            "Pay for water")
        else:
            robo_response = sent_tokens[idx]
        sent_tokens.pop()

    # Format the response by replacing keywords with HTML line breaks using regex
    formatted_response = re.sub(r'\b(step|press|For)\b', r'<br>\1', robo_response, flags=re.IGNORECASE)

    return formatted_response

# Flask app initialization
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load corpus
with open('data.txt', 'r', errors='ignore') as f:
    raw = f.read().lower()
    sent_tokens = nltk.sent_tokenize(raw)

# Initialize TF-IDF Vectorizer
TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english', max_df=0.85, min_df=2, ngram_range=(1, 2))


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message").lower()
    print(f"Received message: {user_message}")

    if session_context['first_message']:
        session_context['first_message'] = False
        initial_message = "How may I help you?"
    else:
        initial_message = ""

    if user_message in ['bye', 'exit', 'quit']:
        bot_response = "Bye! Take care."
        further_help_message = ""
    elif user_message in ['thanks', 'thank you']:
        bot_response = "You are welcome!"
        further_help_message = ""
    else:
        greet = greeting(user_message)
        if greet:
            bot_response = greet
            further_help_message = ""
        else:
            bot_response = response(user_message, sent_tokens, TfidfVec)
            
            # Detect if the response contains steps (numbers or bullet points)
            step_pattern = re.compile(r'(\d+\.\s|\•|\-|\*|step\s\d+)', re.IGNORECASE)
            if step_pattern.search(bot_response):
                further_help_message = ("How much further may I help you? type any option so i can sort you out quickly:<br>"
                                        "Sign up support<br>"
                                        "Log in support<br>"
                                        "Forgot password<br>"
                                        "Payment for parking<br>"
                                        "Payment for water")
            else:
                further_help_message = ""

    return jsonify({
        "response": f"{initial_message} {bot_response}".strip(),
        "further_help": further_help_message
    })


if __name__ == '__main__':
    app.run(debug=True)
