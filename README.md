# 🌸 AuraSpring – AI-Powered Springtime Mood Companion  
**Developed for IngeniumSTEM Spring Hacks 1.0**

AuraSpring is a calming web companion designed to help individuals manage **Seasonal Affective Disorder (SAD)** during the spring season. Built with Flask and integrated with Google's Gemini AI, it offers mood tracking, emotional insights, and a supportive chatbot for mental wellness.

---

## 🌟 Features

- 📝 **Mood Tracker**  
  Log your daily mood using emojis and visualize trends over time.

- 💬 **AI Chatbot Companion**  
  Powered by Gemini AI, this chatbot offers comforting and empathetic responses.

- 📚 **Resource Library**  
  Access curated spring-focused mental health tips and self-care resources.

- 📊 **Mood Visualization**  
  View your emotional patterns with interactive charts.

- 🔐 **User Accounts**  
  Secure login, signup, and personalized dashboards.

---

## Tech Stack

| Layer       | Tech Used                                 |
|-------------|--------------------------------------------|
| **Backend** | Flask, SQLite (or PostgreSQL optional)     |
| **Frontend**| HTML, Tailwind CSS, Chart.js, Lottie       |
| **AI API**  | Gemini AI (Google Generative AI)           |
| **Hosting** | Render (Free Web Service)                  |

---

## 🚀 Getting Started

### 📦 Prerequisites

- Python 3.x  
- `pip` (Python package installer)  
- Gemini API Key from [Google AI Studio](https://makersuite.google.com/app)

---

### 🔧 Local Installation

```bash
# 1. Clone the repo
git clone https://github.com/your-username/auraspring.git
cd auraspring

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create environment variable file
touch .env
Inside .env, add:
SECRET_KEY=your-secret-key
GEMINI_API_KEY=your-gemini-api-key

# 5. Run the app
python app.py
