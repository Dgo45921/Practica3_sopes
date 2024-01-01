from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

db_config = {
    'host': 'mysql-service',
    'user': 'root',
    'password': 'root',
    'database': 'dhuite202003585db',
    'port': '3306'
}


def authenticate_user(username, password):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        # Query to check if the username and password match
        query = "SELECT * FROM dhuite202003585users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            return True
        else:
            return False

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()


def update_password(username, new_password):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Query to update the user's password
        query = "UPDATE dhuite202003585users SET password = %s WHERE username = %s"
        cursor.execute(query, (new_password, username))
        connection.commit()

        return True

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()


@app.route('/')
def index():
    return render_template('index.html')


def create_user(username, password):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Check if the username already exists
        cursor.execute("SELECT * FROM dhuite202003585users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            return False, "Username already exists"

        # Insert the new user into the database
        cursor.execute("INSERT INTO dhuite202003585users (username, password) VALUES (%s, %s)", (username, password))
        connection.commit()

        return True, "User created successfully"

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False, "Error creating user"

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()


@app.route('/create-user', methods=['GET', 'POST'])
def create_user_route():
    if request.method == 'GET':
        return render_template('create_user.html')
    elif request.method == 'POST':
        username = request.form['newUsername']
        password = request.form['newPassword']

        success, message = create_user(username, password)

        if success:
            return render_template('index.html', message='user created succesfully :)')
        else:
            return render_template('error.html', message=message)


@app.route('/change-password', methods=['POST', 'GET'])
def display_change_password_view():
    if request.method == 'GET':
        return render_template('change_password.html')

    elif request.method == 'POST':
        username = request.form['username']
        current_password = request.form['currentPassword']
        new_password = request.form['newPassword']
        confirm_password = request.form['confirmPassword']

        if authenticate_user(username, current_password) and new_password == confirm_password:
            if update_password(username, new_password):
                return render_template('index.html', message='password changed :)')
            else:
                return render_template('error.html', message='Error updating password')
        else:
            return render_template('error.html', message='Authentication failed or passwords do not match')

    else:
        # Handle other HTTP methods
        return 'Unsupported HTTP method'


def get_all_usernames():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Query to retrieve all usernames
        cursor.execute("SELECT username FROM dhuite202003585users")
        usernames = [row[0] for row in cursor.fetchall()]

        return usernames

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if authenticate_user(username, password):
        all_usernames = get_all_usernames()
        return render_template("home.html", all_usernames=all_usernames)
    else:
        return render_template("not_found.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
