import os

import redis
from flask import Flask, render_template_string, request, session, redirect, url_for
from flask_session import Session

from uuid import uuid4

app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY', default='BAD_SECRET_KEY')
redis_server = os.getenv('REDIS_SERVER', default='127.0.0.1')

# Configure Redis for storing the session data on the server-side
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis.from_url(f'redis://{redis_server}:6379')

# Create and initialize the Flask-Session object AFTER `app` has been configured
server_session = Session(app)


@app.route('/set_email', methods=['GET', 'POST'])
def set_email():
    if request.method == 'POST':
        # Save the form data to the session object
        session['email'] = request.form['email_address']
        session["token"] = str(uuid4())
        return redirect(url_for('get_email'))

    return """
        <form method="post">
            <label for="email">Enter your email address:</label>
            <input type="email" id="email" name="email_address" required />
            <button type="submit">Submit</button
        </form>
        """


@app.route('/')
def get_email():
    try:

        host_name = os.uname()[1]
        email = session["email"]
        token = session["token"]
        return f"""
        
        email: {email} <br>
        token: {token} <br>
        hostname: {host_name} <br>
        """
    except Exception as e:
        print(e)
        return render_template_string("""
                <h1>Welcome! Please enter your email <a href="{{ url_for('set_email') }}">here.</a></h1>
        """)
    # return render_template_string("""
    #         {% if session['email'] %}
    #             <h1>Welcome {{ session['email'] }}!</h1>
    #             <h1>Welcome {{ os.getenv("HOSTNAME") }}!</h1>
    #         {% else %}
    #             <h1>Welcome! Please enter your email <a href="{{ url_for('set_email') }}">here.</a></h1>
    #         {% endif %}
    #     """)


@app.route('/delete_email')
def delete_email():
    # Clear the email stored in the session object
    session.pop('email', default=None)
    return '<h1>Session deleted!</h1>'


if __name__ == '__main__':
    app.run()
