from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Route for home page
@app.route('/')
def index():
    return render_template('index.html')  # Ensure index.html is in the templates folder

# Route for contact form page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Insert data into the database
        conn = sqlite3.connect('contacts.db')
        c = conn.cursor()
        c.execute('INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)',
                  (name, email, message))
        conn.commit()
        conn.close()

        # Redirect to a thank you page after successful submission
        return redirect('/thank-you')

    return render_template('contact.html')  # Ensure contact.html is in the templates folder

# Route for thank you page after form submission
@app.route('/thank-you')
def thank_you():
    return render_template('thank-you.html')  # Ensure you create a thank-you.html file

if __name__ == '__main__':
    init_db()  # Initialize the database when the app starts
    app.run(debug=True)
