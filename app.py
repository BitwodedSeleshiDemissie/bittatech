import logging
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
def hash_password(password):
    return generate_password_hash(password)
def check_password(stored_password, provided_password):
    return check_password_hash(stored_password, provided_password)

def create_user(name, email, hashed_password):
    # Connect to PostgreSQL database
    conn = psycopg2.connect(
        dbname="bittatech_data",  
        user="bittatech_data_user",    
        password="N7oibExmokOMOAhaMxXclZyRh5vyg8jp",  
        host="dpg-ctec3aaj1k6c73at5hjg-a",  
        port="5432"           # Default PostgreSQL port
    )
    cursor = conn.cursor()

    # Insert the new user into the users table
    cursor.execute(
        "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
        (name, email, hashed_password)
    )

    # Commit the changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()





# Initialize Flask app
app = Flask(__name__)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465  # SSL port for Gmail
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')  # Email stored securely in environment variables
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  # App password stored securely
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')  # Default sender email

# Initialize Flask-Mail
mail = Mail(app)
# The flask authentication thing that we are using is based from a flask-login library

# Flask-Login configuration
app.config['SECRET_KEY'] = 'secret'
login_manager = LoginManager()
login_manager.init_app(app)

# Database URL
DATABASE_URL = 'postgresql://bittatech_data_user:N7oibExmokOMOAhaMxXclZyRh5vyg8jp@dpg-ctec3aaj1k6c73at5hjg-a/bittatech_data'

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
def get_user_by_email(email):
    # Use the provided connection string's components
    conn = psycopg2.connect(
        dbname="bittatech_data",              # Database name
        user="bittatech_data_user",           # Username
        password="N7oibExmokOMOAhaMxXclZyRh5vyg8jp",  # Password
        host="dpg-ctec3aaj1k6c73at5hjg-a",    # Host
        port="5432"                           # Port
    )
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    # Query to check if a user with the given email exists
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()  # Returns None if no user is found

    # Close the database connection
    cursor.close()
    conn.close()

    return user

def __init__(self, id, name, surname, email, password):

    self.id = id
    self.name = name
    self.surname = surname
    self.email = email
    self.password = password


@login_manager.user_loader
def load_user(user_id):
    db_user = get_user_by_id(user_id)  # Replace with your DAO function to fetch user
    if db_user:
        return User(
            id=db_user['id'],
            name=db_user['name'],
            surname=db_user['surname'],
            email=db_user['email'],
            password=db_user['password']
        )
    return None

# Database connection function
def get_db():
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        return conn
    except Exception as e:
        logging.error(f"Database connection error: {e}")
        raise
    
#create user table 
def users():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        conn.commit()
        cursor.close()
        conn.close()
        logging.debug("Table 'users' checked/created.")
    except Exception as e:
        logging.error(f"Error creating table: {e}")


# Create messages table
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

# Insert message into database
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

# DAO function to fetch user (placeholder)
def get_user_by_id(user_id):
    # Replace with actual logic to fetch user from the database
    return None

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

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
            insert_message(name, email, subject, message)
            return redirect(url_for('thank_you'))
        except Exception as e:
            logging.error(f"Error processing the contact form: {e}")
            return "There was an error processing your message. Please try again later."

    return render_template('contact.html')

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

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

# Additional routes for pages
@app.route('/service')
def service():
    return render_template('service.html')

@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/app-development')
def app_development():
    return render_template('app_development.html')

@app.route('/email-marketing')
def email_marketing():
    return render_template('email_marketing.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/ppc-advertising')
def ppc_advertising():
    return render_template('ppc_advertising.html')

@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy_policy.html')

@app.route('/seo-optimization')
def seo_optimization():
    return render_template('seo_optimization.html')

@app.route('/social-media-marketing')
def social_media_marketing():
    return render_template('social_media_marketing.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # Add user authentication logic
        return redirect(url_for('profile'))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if user already exists (you can implement this function)
        existing_user = get_user_by_email(email)
        if existing_user:
            return "User already exists. Please log in."

        # Hash the password before storing it
        hashed_password = hash_password(password)

        # Insert new user into the database (you can implement this function)
        create_user(name, email, hashed_password)

        return redirect(url_for('login'))  # Redirect to login after signup

    return render_template('signup.html')




@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/testimonial')
def testimonial():
    return render_template('testimonial.html')

@app.route('/web-design')
def web_design():
    return render_template('web_design.html')

# Custom 404 Error Page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Initialize database table
create_table()

# Main entry point
if __name__ == "__main__":
    # Create required tables
    create_users_table()
    create_messages_table()  # Renamed for clarity
    
    # Start the Flask app
    app.run(debug=True)
