from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # You can add your authentication logic here
    # For simplicity, let's just print the credentials for now
    print(f'Username: {username}, Password: {password}')

    return 'Login successful!'


if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')
