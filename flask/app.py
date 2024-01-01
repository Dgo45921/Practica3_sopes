from flask import Flask, render_template, request
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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if authenticate_user(username, password):
        return render_template("home.html")
    else:
        return render_template("not_found.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
