from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', is_home=True)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # if request.method == 'POST':
    #     # handle form data
    #     name = request.form['name']
    #     email = request.form['email']
    #     password = request.form['password']
    #     # add logic (e.g., save to DB)
    #     return "Signed up successfully!"
    return render_template('signup.html', is_home=False)

@app.route('/login')
def login():
    return render_template('login.html', is_home=False)


if __name__ == '__main__':
    app.run(debug=True)
