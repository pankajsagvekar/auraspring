from flask import Flask, render_template, request, jsonify
import os
import google.generativeai as genai
from dotenv import load_dotenv
import markdown


app = Flask(__name__)

load_dotenv()

SYSTEM_PROMPT = "You are a helpful and friendly AI mental health assistant. Keep answers supportive, calm, and empathetic. Avoid medical advice—suggest helpful resources instead."

# Secure Gemini API setup
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

@app.route('/')
def home():
    return render_template('index.html', is_home=True, not_dashboard=True)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html', is_home=False, not_dashboard=True)

@app.route('/login')
def login():
    return render_template('login.html', is_home=False, not_dashboard=True)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', is_home=False, not_dashboard=False)

@app.route('/moodtracker')
def moodtracker():
    return render_template('moodtracker.html', is_home=False, not_dashboard=False)

@app.route('/ai_chatbot')
def ai_chatbot():
    return render_template('ai_chatbot.html', is_home=False, not_dashboard=False)

@app.route('/resources_library')
def resources_library():
    return render_template('resources_library.html', is_home=False, not_dashboard=False)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    try:
        full_prompt = f"{SYSTEM_PROMPT}\nUser: {user_message}\nAI:"
        gemini_response = model.generate_content(full_prompt)
        markdown_text = gemini_response.text.strip()
        html_output = markdown.markdown(markdown_text)
    except Exception as e:
        html_output = "<p>Sorry, something went wrong.</p>"

    return jsonify({"reply": html_output})

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html", is_home=False, not_dashboard=False)

if __name__ == '__main__':
    app.run(debug=True)
