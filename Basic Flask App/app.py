# app.py
from flask import Flask, render_template, request

app = Flask(__name__)

# Route to handle the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle the form submission
@app.route('/submit', methods=['POST'])
def submit():
    # Extract form data
    user_input = request.form['user_input']
    # You can process the input or return it
    return f"You entered: {user_input}"

if __name__ == "__main__":
    app.run(debug=True)
