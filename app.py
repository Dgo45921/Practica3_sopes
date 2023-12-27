from flask import Flask, render_template, request, jsonify
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'imbilelou'
app.config['MYSQL_DATABASE_DB'] = 'users'
app.config['MYSQL_DATABASE_HOST'] = '34.170.111.220'
mysql.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Check if the user exists in the database
    try:
        # Create MySQL connection and cursor
        conn = mysql.connect()
        cursor = conn.cursor()

        # Check if the user exists in the database
        query = "SELECT * FROM credentials WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        # Return the result
        if result:
            return 'Login successful!'
        else:
            return 'User not found. Please check your credentials.'

    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')
