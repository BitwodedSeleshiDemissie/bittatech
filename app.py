import logging
import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message

# Initialize Flask app
app = Flask(__name__)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465  # SSL port for Gmail
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'your-email-password'  # Replace with your email password or app password
app.config['MAIL_DEFAULT_SENDER'] = 'your-email@gmail.com'

# Initialize Flask-Mail
mail = Mail(app)

# Database configuration (using PostgreSQL)
DATABASE_URL = os.getenv('DATABASE_URL')  # Get the database URL from Render environment variable

# Function to connect to the PostgreSQL database
def get_db():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    return conn

# Function to initialize the database and create table
def create_table():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        subject TEXT NOT NULL,
        message TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

# Create the table if it doesn't exist on app startup
create_table()

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for the contact form page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        # Save the data to the PostgreSQL database
        try:
            conn = get_db()  # Get database connection
            cursor = conn.cursor()
            
            # Insert form data into the database
            cursor.execute('''
            INSERT INTO messages (name, email, subject, message)
            VALUES (%s, %s, %s, %s)
            ''', (name, email, subject, message))

            conn.commit()  # Commit the transaction
            conn.close()  # Close the connection

            logging.debug("Message stored in the database successfully.")
            return redirect(url_for('thank_you'))  # Redirect to thank you page

        except Exception as e:
            logging.error(f"Error inserting data into the database: {e}")
            return "There was an error processing your message. Please try again later."

    return render_template('contact.html')

# Route for the thank-you page
@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

# Route to view all submitted messages (for admin)
@app.route('/view_messages')
def view_messages():
    try:
        conn = get_db()  # Get database connection
        cursor = conn.cursor()
        
        # Retrieve all the messages
        cursor.execute('SELECT * FROM messages')
        messages = cursor.fetchall()  # Fetch all rows

        conn.close()  # Close the connection

        return render_template('view_messages.html', messages=messages)

    except Exception as e:
        logging.error(f"Error retrieving messages: {e}")
        return "There was an error retrieving the messages."

# Other routes
@app.route('/app-development')
def app_development():
    return render_template('app_development.html')

# Custom 404 Error Page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Main entry point
if __name__ == '__main__':
    app.run(debug=False)
