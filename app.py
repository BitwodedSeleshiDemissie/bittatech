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

# Direct connection string for your Render-hosted PostgreSQL database
DATABASE_URL = 'postgresql://bittatech_data_user:N7oibExmokOMOAhaMxXclZyRh5vyg8jp@dpg-ctec3aaj1k6c73at5hjg-a/bittatech_data'

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to connect to the PostgreSQL database
def get_db():
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        return conn
    except Exception as e:
        logging.error(f"Database connection error: {e}")
        raise

# Function to initialize the database and create the table
def create_table():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT NOT NULL,
            message TEXT NOT NULL
        )''')
        conn.commit()
        cursor.close()
        conn.close()
        logging.debug("Table 'messages' checked/created.")
    except Exception as e:
        logging.error(f"Error creating table: {e}")

# Function to insert a message into the database
def insert_message(name, email, subject, message):
    try:
        conn = get_db()
        cursor = conn.cursor()
        query = '''
            INSERT INTO messages (name, email, subject, message)
            VALUES (%s, %s, %s, %s)
        '''
        cursor.execute(query, (name, email, subject, message))
        conn.commit()
        cursor.close()
        conn.close()
        logging.debug("Message stored in the database successfully.")
    except Exception as e:
        logging.error(f"Error inserting message: {e}")


# Create the table if it doesn't exist on app startup
create_table()

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')
# Route for the service
@app.route('/service')
def service():
    return render_template('service.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()

        if not name or not email or not subject or not message:
            logging.warning("One or more fields are empty.")
            return "Please fill in all fields."

        try:
            # Insert the form data into the database
            insert_message(name, email, subject, message)
            logging.debug("Message stored in the database successfully.")
            return redirect(url_for('thank_you'))  # Redirect to a thank-you page
        except Exception as e:
            logging.error(f"Error processing the contact form: {e}")
            return "There was an error processing your message. Please try again later."

    return render_template('contact.html')
@app.route('/project')
def project():
    return render_template('project.html')


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
        cursor.execute('SELECT * FROM messages')
        messages = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('view_messages.html', messages=messages)
    except Exception as e:
        logging.error(f"Error retrieving messages: {e}")
        return "There was an error retrieving the messages."

# Route for app development services page
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
