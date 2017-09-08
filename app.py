from flask import Flask, render_template

from liveodds.api import totalcorner
from liveodds.config import totalcorner_test_token

app = Flask(__name__)
app.secret_key = 'key'

tc = totalcorner(token=totalcorner_test_token)


@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('/index.html')


@app.route('/index.html', methods=['POST', 'GET'])
def index():
    return render_template('/index.html')


if __name__ == "__main__":
    app.run(debug=True)
