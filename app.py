from apscheduler.scheduler import Scheduler
from flask import Flask, render_template, request, session

from liveodds.api import totalcorner
from liveodds.config import totalcorner_test_token
from liveodds.processing import process

app = Flask(__name__)
app.secret_key = 'key'
cron = Scheduler(daemon=True)
cron.start()

tc = totalcorner(token=totalcorner_test_token)
tc_update = []
data_update = []


@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('/index.html')


@app.route('/index.html', methods=['POST', 'GET'])
def index():
    return render_template('/index.html')


@app.route('/submit', methods=['POST', 'GET'])
def submit():

    global data
    global data_update
    leaguestr = request.form.get("inputCoNz")
    try:
        leagues = (dict(item.split("\t") for item in leaguestr.splitlines()))
    except:
        try:
            leagues = (dict(item.split(",") for item in leaguestr.splitlines()))
        except:
            pass
    finally:
        leagues = {}
        leagues['0'] = 0
    data = {}
    data["Min"] = int(request.form.get("inputMinute"))
    data["Ptph"] = float(request.form.get("inputPtph"))
    data["Ptfh"] = float(request.form.get("inputPtfh"))
    data["Ptpa"] = float(request.form.get("inputPtpa"))
    data["Ptfa"] = float(request.form.get("inputPtfa"))
    data["PAtpH"] = float(request.form.get("inputPAtpH"))
    data["Patpa"] = float(request.form.get("inputPatpa"))
    data["CofMinH"] = float(request.form.get("inputCofMinH"))
    data["CofMinA"] = float(request.form.get("inputCofMinA"))
    data["CoefMinH"] = int(request.form.get("inputCoefMinH"))
    data["CoefMinA"] = int(request.form.get("inputCoefMinA"))
    data["CoefMaxSgt"] = float(request.form.get("inputCoefMaxSgt"))
    data["CoefMinSgt"] = float(request.form.get("inputCoefMinSgt"))
    data["ValueMax"] = float(request.form.get("inputValueMax"))
    data["ValueMin"] = float(request.form.get("inputValueMin"))

    with app.test_request_context():

        print(data)
        tc_data = tc.get_odds()
        for i in tc.get_odds():
            tc_update.append(i)
            print(i)

        results_preds, results = process(data, tc_data, leagues)
        return render_template('/index.html', result_pred=results_preds,
                               result=results)


if __name__ == "__main__":
    app.run(debug=True)
