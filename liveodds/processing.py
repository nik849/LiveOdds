from numpy import where


def process(data, tc_data, leagues):
    """
    Processing method for returning liveodds from totalcorner request
    """
    results_preds = {}
    results = {}
    for league, coeff in leagues.items():
        print(coeff)

    unwanted_keys = ['h_id', 'a_id', 'hc', 'ac', 'hrc', 'arc',
                     'hyc', 'ayc', 'hf_hc', 'hf_ac', 'hf_hg', 'hf_ag', 'ish',
                     'hp', 'ap', 'asian_corner']

    for match in tc_data:
        if match["status"] == 'full':
            results.update(match)
            calcs = {}
            calcs["Datk"] = len(match["attacks_h"]) - len(match["attacks"])\
                / int(data["Min"])
            calcs["GttpH"] = len(match["shot_on_h"]) * float(data["Ptph"])
            calcs["GttfH"] = len(match["shot_on_h"]) * float(data["Ptfh"])
            calcs["GttpA"] = len(match["shot_on"]) * float(data["Ptpa"])
            calcs["GttfA"] = len(match["shot_on"]) * float(data["Ptfa"])
            calcs["GtatpH"] = len(match["attacks_h"]) * float(data["PAtpH"])
            calcs["GtapA"] = len(match["attacks"]) * float(data["Patpa"])
            calcs["GtHm"] = None
            calcs["gtam"] = None
            calcs["SgtM"] = None
            calcs["DeltaM"] = None
            calcs["GtFh"] = None
            calcs["GtFa"] = None
            calcs["sgtft1"] = None
            calcs["sgtft"] = None
            calcs["U/O"] = None
            results.update(calcs)

        elif match["status"] == data["Min"]:
            results_preds.update({'Minute': data["Min"]})
            results_preds.update(match)
            calcs = {}
            calcs["Datk"] = len(match["attacks_h"]) - len(match["attacks"])\
                / int(data["Min"])
            calcs["GttpH"] = len(match["shot_on_h"]) * float(data["Ptph"])
            calcs["GttfH"] = len(match["shot_on_h"]) * float(data["Ptfh"])
            calcs["GttpA"] = len(match["shot_on"]) * float(data["Ptpa"])
            calcs["GttfA"] = len(match["shot_on"]) * float(data["Ptfa"])
            calcs["GtapH"] = len(match["attacks_h"]) * float(data["PAtpH"])
            calcs["GtapA"] = len(match["attacks"]) * float(data["Patpa"])
            calcs["GtHm"] = (calcs["GttpH"] + calcs["GttfH"] + calcs["GtapH"])\
                + calcs["Datk"] / 3
            calcs["gtam"] = (calcs["GttpH"] + calcs["GttfH"] + calcs["GtapH"])\
                - calcs["Datk"] / 3
            calcs["SgtM"] = where(where(calcs["GtHm"] < data["CofMinH"], 0,
                                  calcs["GtHm"]) + where(calcs["gtam"] <
                                  data["CofMinA"], 0, calcs["gtam"]) +
                                  data["CoNz"] < 0, 0, where(calcs["GtHm"] <
                                  data["CofMinH"], 0, calcs["GtHm"]) +
                                  where(calcs["gtam"] < data["CofMinA"], 0,
                                  calcs["gtam"]) + data["CoNz"])
            calcs["Sgmx"] = data["hg"] + data["ag"]
            calcs["DeltaM"] = ((
                match["hg"] - calcs["GtHm"]) * (match["ag"] -
                calcs["gtam"]) * (calcs["Sgmx"] - calcs["SgtM"]
                                 )) / 3
            calcs["GtFh"] = where(where(calcs["DeltaM"] > 1, ((match["hg"] *
                calcs["GtHm"]) / 2) / data["Min"] * data["CoefMinH"] -
                (calcs["DeltaM"] / 3), ((match["hg"] * calcs["GtHm"]) / 2)
                / data["Min"] * data["CoefMinH"]) < match["hg"], match["hg"],
                where(calcs["DeltaM"] > 1, ((match["hg"] * calcs["GtHm"]) / 2)
                / data["Min"] * data["CoefMinH"] - (calcs["DeltaM"] / 3),
                ((match["hg"] * calcs["GtHm"]) / 2) / data["Min"] *
                data["CoefMinH"]))
            calcs["GtFa"] = where(where(calcs["DeltaM"] > 1, ((match["hg"] *
                calcs["GtHm"]) / 2) / data["Min"] * data["CoefMinH"] -
                (calcs["DeltaM"] / 3), ((match["hg"] * calcs["GtHm"]) / 2) /
                data["Min"] * data["CoefMinH"]) < match["hg"], match["hg"],
                where(calcs["DeltaM"] > 1, ((match["hg"] * calcs["GtHm"]) / 2)
                / data["Min"] * data["CoefMinH"] - (calcs["DeltaM"] / 3),
                ((match["hg"] * calcs["GtHm"]) / 2) / data["Min"] *
                data["CoefMinH"]))
            calcs["GtFa"] = where(where(calcs["DeltaM"] < -1, ((match["ag"] *
                calcs["gtam"]) / 2) / 50 * 90 + (calcs["DeltaM"] / 3),
                ((match["ag"] * calcs["gtam"]) / 2) / 50 * 90) < match["ag"],
                match["ag"], where(calcs["DeltaM"] < -1, ((match["ag"] *
                calcs["gtam"]) / 2) / 50 * 90 + (calcs["DeltaM"] / 3),
                ((match["ag"] * calcs["gtam"]) / 2) / 50 * 90))
            calcs["sgtft1"] = where(calcs["GtFh"] < 0, 5, 0, calcs["GtFh"]) + \
                where(calcs["GtFa"] < 0, 7, 0, calcs["GtFa"]) + \
                where(calcs["DeltaM"] > data["CoefMaxSgt"], data["ValueMax"],
                where(calcs["DeltaM"] < data["CoefMinSgt"], data["ValueMin"],
                0)) + data["CoNz"]
            calcs["sgtft"] = ((calcs["GtFh"] * where(data["Min"] > 75,
                calcs["Sgmx"], calcs["GtFh"]) * where(where(data["Min"] <
                46, data["Min"] > 35), calcs["Sgmx"], calcs["GtHm"] +
                calcs["gtam"])) / 3) + (data["CoNz"] / 3)
            if calcs["sgtft1"] - data["ValueMax"]:
                string = 'Over'
            else:
                string = 'Under'
            calcs["U/O"] = f'{string} {data["ValueMax"]}'
            results_preds.update(calcs)

    if len(results) > 0:
        for key in unwanted_keys:
            try:
                del results[key]
            except KeyError:
                pass
    if len(results_preds) > 0:
        for key in unwanted_keys:
            try:
                del results_preds[key]
            except KeyError:
                pass

    return results_preds, results
