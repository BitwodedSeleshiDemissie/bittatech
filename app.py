from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
app = Flask(__name__)
# Set the path for the SQLite database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'contacts.db')

# Function to initialize the database
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                subject TEXT,
                message TEXT,
                submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

# Initialize the database on app startup
init_db()

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        # Insert data into the database
        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO contacts (name, email, subject, message) VALUES (?, ?, ?, ?)",
                    (name, email, subject, message)
                )
                conn.commit()
        except sqlite3.Error as e:
            return f"An error occurred: {e}"

        print("Form submitted successfully, redirecting to thank_you page.")
        return redirect(url_for('thank_you'))  # Redirect to the thank-you page

    return render_template('contact.html')


# Route for thank-you page
@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

# Other routes
@app.route('/app-development')
def app_development():
    return render_template('app_development.html')

@app.route('/email-marketing')
def email_marketing():
    return render_template('email_marketing.html')

@app.route('/ppc-advertising')
def ppc_advertising():
    return render_template('ppc_advertising.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy_policy.html')

@app.route('/seo-optimization')
def seo_optimization():
    return render_template('seo_optimization.html')

@app.route('/service')
def service():
    return render_template('service.html')

@app.route('/social-media-marketing')
def social_media_marketing():
    return render_template('social_media_marketing.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/testimonial')
def testimonial():
    return render_template('testimonial.html')

@app.route('/web-design')
def web_design():
    return render_template('web_design.html')

@app.route('/Help')
def help():
    return render_template('help.html')

@app.route('/FQAss')
def faq():
    return render_template('faq.html')

# Custom 404 Error Page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Main entry point
if __name__ == '__main__':
    app.run(debug=True)

