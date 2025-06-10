from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', is_home=True, not_dashboard=True)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # if request.method == 'POST':
    #     # handle form data
    #     name = request.form['name']
    #     email = request.form['email']
    #     password = request.form['password']
    #     # add logic (e.g., save to DB)
    #     return "Signed up successfully!"
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

@app.errorhandler(404)
def ot_found(e):
    return render_template("404.html",  is_home=False, not_dashboard=False)

if __name__ == '__main__':
    app.run(debug=True)
