from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import google.generativeai as genai
import markdown

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY', 'fallback-secret-key')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auraspring.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    name     = db.Column(db.String(100), nullable=False)
    email    = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class MoodEntry(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    mood      = db.Column(db.String(10), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id   = db.Column(db.Integer, db.ForeignKey('user.id'))

# Ensure tables exist in *every* environment (local & Render)

with app.app_context():
    db.create_all()       # creates tables only if they do not exist
SYSTEM_PROMPT = (
    "You are a helpful and friendly AI mental health assistant. "
    "Keep answers supportive, calm, and empathetic. "
    "Avoid medical advice—suggest helpful resources instead."
)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")


@app.route('/')
def home():
    return render_template('index.html', is_home=True, not_dashboard=True)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name     = request.form['name']
        email    = request.form['email']
        password = request.form['password']

        if User.query.filter_by(email=email).first():
            return "User with this email already exists."

        user = User(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        return redirect(url_for('dashboard'))
    return render_template('signup.html', is_home=False, not_dashboard=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            return "Invalid email or password."
    return render_template('login.html', is_home=False, not_dashboard=True)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', is_home=False, not_dashboard=False)

@app.route('/moodtracker', methods=['GET', 'POST'])
def moodtracker():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    if request.method == 'POST':
        mood = request.form['mood']
        db.session.add(MoodEntry(mood=mood, user_id=user_id))
        db.session.commit()

    moods = MoodEntry.query.filter_by(user_id=user_id).order_by(MoodEntry.timestamp).all()
    mood_values = [['😢','😰','😐','😊','😡'].index(m.mood) for m in moods]
    labels      = [m.timestamp.strftime('%b %d') for m in moods]

    return render_template('moodtracker.html',
                           labels=labels,
                           moods=mood_values,
                           is_home=False,
                           not_dashboard=False)

@app.route('/ai_chatbot')
def ai_chatbot():
    return render_template('ai_chatbot.html', is_home=False, not_dashboard=False)

@app.route('/resources_library')
def resources_library():
    return render_template('resources_library.html', is_home=False, not_dashboard=False)

@app.route('/chat', methods=['POST'])
def chat():
    data        = request.get_json()
    user_message = data.get("message", "")

    try:
        full_prompt   = f"{SYSTEM_PROMPT}\nUser: {user_message}\nAI:"
        gemini_resp   = model.generate_content(full_prompt)
        html_output   = markdown.markdown(gemini_resp.text.strip())
    except Exception:
        html_output = "<p>Sorry, something went wrong.</p>"

    return jsonify({"reply": html_output})

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html", is_home=False, not_dashboard=False)

@app.route('/about')
def about():
    return render_template('about.html', is_home=False, not_dashboard=True)

@app.route('/contact')
def contact():
    return render_template('contact.html', is_home=False, not_dashboard=True)


if __name__ == '__main__':
    app.run(debug=True)