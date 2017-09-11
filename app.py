from flask import Flask, render_template, request

from liveodds.api import totalcorner
from liveodds.config import totalcorner_test_token
from liveodds.processing import process


app = Flask(__name__)
app.secret_key = 'key'

tc = totalcorner(token=totalcorner_test_token)


@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('/index.html')


@app.route('/index.html', methods=['POST', 'GET'])
def index():
    return render_template('/index.html')


@app.route('/submit', methods=['POST', 'GET'])
def submit():
    nationstr = request.form.get("inputCoNz")
    nations = (dict(item.split("\t") for item in nationstr.splitlines()))
    print(nations)
    data = {}
    data["Min"] = request.form.get("inputMinute")
    data["Ptph"] = request.form.get("inputPtph")
    data["Ptfh"] = request.form.get("inputPtfh")
    data["Ptpa"] = request.form.get("inputPtpa")
    data["Ptfa"] = request.form.get("inputPtfa")
    data["PAtpH"] = request.form.get("inputPAtpH")
    data["Patpa"] = request.form.get("inputPatpa")
    data["CofMinH"] = request.form.get("inputCofMinH")
    data["CofMinA"] = request.form.get("inputCofMinA")
    data["CoefMinH"] = request.form.get("inputCoefMinH")
    data["CoefMinA"] = request.form.get("inputCoefMinA")
    data["CoefMaxSgt"] = request.form.get("inputCoefMaxSgt")
    data["CoefMinSgt"] = request.form.get("inputCoefMinSgt")
    data["ValueMax"] = request.form.get("inputValueMax")
    data["ValueMin"] = request.form.get("inputValueMin")
    print(data)

    results = process(data)
    return render_template('/fulltime.html' **results)


if __name__ == "__main__":
    app.run(debug=True)
