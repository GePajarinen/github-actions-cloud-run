from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'Welcome to Github actions from Cloud Run v.1'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
