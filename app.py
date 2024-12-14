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
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')  # Replace with your email (stored securely in environment variables)
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  # Replace with your app password (stored securely)
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')  # Default sender email

# Initialize Flask-Mail
mail = Mail(app)

import logging
import psycopg2

# Direct connection string for your Render-hosted PostgreSQL database
DATABASE_URL = 'postgresql://bittatech_data_user:N7oibExmokOMOAhaMxXclZyRh5vyg8jp@dpg-ctec3aaj1k6c73at5hjg-a/bittatech_data'

# Function to connect to the PostgreSQL database
def get_db():
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')  # Use sslmode='require' to ensure a secure connection
        return conn
    except Exception as e:
        logging.error(f"Database connection error: {e}")
        raise  # Re-raise the exception to ensure the error is properly handled

# Function to initialize the database and create the table
def create_table():
    try:
        conn = get_db()  # Get database connection
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT NOT NULL,
            message TEXT NOT NULL
        )''')
        conn.commit()  # Commit the changes
        conn.close()  # Close the connection
        logging.debug("Table 'messages' checked/created.")
    except Exception as e:
        logging.error(f"Error creating table: {e}")  # Log errors if any


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
        # Get form data and ensure no value is None
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()

        # Validate form fields
        if not name or not email or not subject or not message:
            logging.warning("One or more fields are empty.")
            return "Please fill in all fields."

        # Save the data to the PostgreSQL database
        try:
            conn = get_db()
            cursor = conn.cursor()
            
            # Insert form data into the database
            cursor.execute('''INSERT INTO messages (name, email, subject, message)
                              VALUES (%s, %s, %s, %s)''', (name, email, subject, message))

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
        conn = get_db()
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
    # Setup logging configuration
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=False)
