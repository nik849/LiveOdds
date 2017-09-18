from numpy import where


def process(data, tc_data, leagues):
    """
    Processing method for returning liveodds from totalcorner request
    """
    overall_results = []
    overall_preds = []
    results_preds = {}
    results = {}
    for league, coeff in leagues.items():


        unwanted_keys = ['h_id', 'a_id', 'hc', 'ac', 'hrc', 'arc',
                         'hyc', 'ayc', 'hf_hc', 'hf_ac', 'hf_hg', 'hf_ag', 'ish',
                         'hp', 'ap', 'asian_corner']

        for match in tc_data:
            print(match["h"])
            print(match["a"])
            if match["status"] == 'full':
                #results.update({'Minute': data["Min"]})
                                #results.update(match)
                print(data["Min"])
                calcs = {}
                calcs["Nation"] = league
                if calcs["Nation"] == match["h"] or match["a"]:
                    calcs["CoNz"] = float(coeff)
                    match["attacks_h"] = []
                    match["shot_on_h"] = []
                    calcs["Datk"] = len(match["attacks_h"]) - len(match["attacks"])\
                        / int(data["Min"])
                    calcs["GttpH"] = len(match["shot_on_h"]) * float(data["Ptph"])
                    calcs["GttfH"] = len(match["shot_on_h"]) * float(data["Ptfh"])
                    calcs["GttpA"] = len(match["shot_on"]) * float(data["Ptpa"])
                    calcs["GttfA"] = len(match["shot_on"]) * float(data["Ptfa"])
                    calcs["GtapH"] = len(match["attacks_h"]) * float(data["PAtpH"])
                    calcs["GtapA"] = len(match["attacks"]) * float(data["Patpa"])
                    calcs["GtHm"] = int((calcs["GttpH"] + calcs["GttfH"] + calcs["GtapH"])\
                        + calcs["Datk"] / 3)
                    calcs["gtam"] = int((calcs["GttpH"] + calcs["GttfH"] + calcs["GtapH"])\
                        - calcs["Datk"] / 3)

                    calcs["SgtM"] = where(where(calcs["GtHm"] < float(data["CofMinH"]), 0,
                                          calcs["GtHm"]) + where(calcs["gtam"] <
                                          float(data["CofMinA"]), 0, calcs["gtam"])
                                          + calcs["CoNz"] < 0, 0, where(calcs["GtHm"] < calcs["gtam"], 0, calcs["GtHm"])
                                          + where(calcs["gtam"] < float(data["CofMinA"]), 0, calcs["gtam"]) + calcs["CoNz"])
                    calcs["Sgmx"] = int(match["hg"]) + int(match["ag"])

                    calcs["DeltaM"] = ((
                        int(match["hg"]) - calcs["GtHm"]) * (int(match["ag"]) -
                        calcs["gtam"]) * (calcs["Sgmx"] - calcs["SgtM"]
                                         )) / 3
                    calcs["GtFh"] = where(where(calcs["DeltaM"] > 1, ((int(match["hg"]) *
                        calcs["GtHm"]) / 2) / data["Min"] * data["CoefMinH"] -
                        (calcs["DeltaM"] / 3), ((int(match["hg"]) * calcs["GtHm"]) / 2)
                        / int(data["Min"]) * where(int(data["CoefMinH"]) < int(match["hg"]), int(match["hg"]),
                        where(calcs["DeltaM"] > 1, ((int(match["hg"]) * calcs["GtHm"]) / 2)
                        / data["Min"] * data["CoefMinH"] - (calcs["DeltaM"] / 3),
                        ((int(match["hg"]) * calcs["GtHm"]) / 2)) / data["Min"] *
                        data["CoefMinH"])))
                    calcs["GtFh"] = where(where(calcs["DeltaM"] > 1, ((int(match["hg"]) * \
                        calcs["GtHm"]) / 2) / data["Min"] * data["CoefMinH"] -
                        (calcs["DeltaM"] / 3), ((int(match["hg"]) * calcs["GtHm"]) / 2) /
                        data["Min"] * data["CoefMinH"]) < int(match["hg"]), int(match["hg"]),
                        where(calcs["DeltaM"] > 1, ((int(match["hg"]) * calcs["GtHm"]) / 2)
                        / data["Min"] * data["CoefMinH"] - (calcs["DeltaM"] / 3),
                        ((int(match["hg"]) * calcs["GtHm"]) / 2) / data["Min"] *
                        data["CoefMinH"]))
                    calcs["GtFa"] = where(where(calcs["DeltaM"] < -1, ((int(match["ag"]) *
                        calcs["gtam"]) / 2) / 50 * 90 + (calcs["DeltaM"] / 3),
                        ((int(match["ag"]) * calcs["gtam"]) / 2) / 50 * 90) < int(match["ag"]),
                        int(match["ag"]), where(calcs["DeltaM"] < -1, ((int(match["ag"]) *
                        calcs["gtam"]) / 2) / 50 * 90 + (calcs["DeltaM"] / 3),
                        ((int(match["ag"]) * calcs["gtam"]) / 2) / 50 * 90))

                    calcs["sgtft1"] = where(calcs["GtFh"] < 0, 5, calcs["GtFh"]) + \
                        where(calcs["GtFa"] < 0, 7, calcs["GtFa"]) + \
                        where(calcs["DeltaM"] > data["CoefMaxSgt"], data["ValueMax"],
                        where(calcs["DeltaM"] < data["CoefMinSgt"], data["ValueMin"],
                        0)) + float(calcs["CoNz"])
                    calcs["sgtft"] = ((calcs["GtFh"] * where(data["Min"] > 75,
                        calcs["Sgmx"], calcs["GtFh"]) * where(where(data["Min"] <
                        46 and data["Min"] > 35), calcs["Sgmx"], calcs["GtHm"] +
                        calcs["gtam"])) / 3) + (calcs["CoNz"] / 3)
                    if calcs["sgtft1"] - data["ValueMax"]:
                        string = 'Over'
                    else:
                        string = 'Under'
                    calcs["U/O"] = f'{string} {data["ValueMax"]}'
                    results.update(calcs)
                    overall_results.append(results)

            elif match["status"] == data["Min"]:
                results_preds.update({'Minute': data["Min"]})
                #results_preds.update(match)
                print(data["Min"])
                calcs = {}
                calcs["Nation"] = league
                if calcs["Nation"] == match["h"] or match["a"]:
                    calcs["CoNz"] = float(coeff)
                    match["attacks_h"] = []
                    match["shot_on_h"] = []
                    calcs["Datk"] = len(match["attacks_h"]) - len(match["attacks"])\
                        / int(data["Min"])
                    calcs["GttpH"] = len(match["shot_on_h"]) * float(data["Ptph"])
                    calcs["GttfH"] = len(match["shot_on_h"]) * float(data["Ptfh"])
                    calcs["GttpA"] = len(match["shot_on"]) * float(data["Ptpa"])
                    calcs["GttfA"] = len(match["shot_on"]) * float(data["Ptfa"])
                    calcs["GtapH"] = len(match["attacks_h"]) * float(data["PAtpH"])
                    calcs["GtapA"] = len(match["attacks"]) * float(data["Patpa"])
                    calcs["GtHm"] = int((calcs["GttpH"] + calcs["GttfH"] + calcs["GtapH"])\
                        + calcs["Datk"] / 3)
                    calcs["gtam"] = int((calcs["GttpH"] + calcs["GttfH"] + calcs["GtapH"])\
                        - calcs["Datk"] / 3)

                    calcs["SgtM"] = where(where(calcs["GtHm"] < float(data["CofMinH"]), 0,
                                          calcs["GtHm"]) + where(calcs["gtam"] <
                                          float(data["CofMinA"]), 0, calcs["gtam"])
                                          + calcs["CoNz"] < 0, 0, where(calcs["GtHm"] < calcs["gtam"], 0, calcs["GtHm"])
                                          + where(calcs["gtam"] < float(data["CofMinA"]), 0, calcs["gtam"]) + calcs["CoNz"])
                    calcs["Sgmx"] = int(match["hg"]) + int(match["ag"])

                    calcs["DeltaM"] = ((
                        int(match["hg"]) - calcs["GtHm"]) * (int(match["ag"]) -
                        calcs["gtam"]) * (calcs["Sgmx"] - calcs["SgtM"]
                                         )) / 3
                    calcs["GtFh"] = where(where(calcs["DeltaM"] > 1, ((int(match["hg"]) *
                        calcs["GtHm"]) / 2) / data["Min"] * data["CoefMinH"] -
                        (calcs["DeltaM"] / 3), ((int(match["hg"]) * calcs["GtHm"]) / 2)
                        / int(data["Min"]) * where(int(data["CoefMinH"]) < int(match["hg"]), int(match["hg"]),
                        where(calcs["DeltaM"] > 1, ((int(match["hg"]) * calcs["GtHm"]) / 2)
                        / data["Min"] * data["CoefMinH"] - (calcs["DeltaM"] / 3),
                        ((int(match["hg"]) * calcs["GtHm"]) / 2)) / data["Min"] *
                        data["CoefMinH"])))
                    calcs["GtFh"] = where(where(calcs["DeltaM"] > 1, ((int(match["hg"]) * \
                        calcs["GtHm"]) / 2) / data["Min"] * data["CoefMinH"] -
                        (calcs["DeltaM"] / 3), ((int(match["hg"]) * calcs["GtHm"]) / 2) /
                        data["Min"] * data["CoefMinH"]) < int(match["hg"]), int(match["hg"]),
                        where(calcs["DeltaM"] > 1, ((int(match["hg"]) * calcs["GtHm"]) / 2)
                        / data["Min"] * data["CoefMinH"] - (calcs["DeltaM"] / 3),
                        ((int(match["hg"]) * calcs["GtHm"]) / 2) / data["Min"] *
                        data["CoefMinH"]))
                    calcs["GtFa"] = where(where(calcs["DeltaM"] < -1, ((int(match["ag"]) *
                        calcs["gtam"]) / 2) / 50 * 90 + (calcs["DeltaM"] / 3),
                        ((int(match["ag"]) * calcs["gtam"]) / 2) / 50 * 90) < int(match["ag"]),
                        int(match["ag"]), where(calcs["DeltaM"] < -1, ((int(match["ag"]) *
                        calcs["gtam"]) / 2) / 50 * 90 + (calcs["DeltaM"] / 3),
                        ((int(match["ag"]) * calcs["gtam"]) / 2) / 50 * 90))

                    calcs["sgtft1"] = where(calcs["GtFh"] < 0, 5, calcs["GtFh"]) + \
                        where(calcs["GtFa"] < 0, 7, calcs["GtFa"]) + \
                        where(calcs["DeltaM"] > data["CoefMaxSgt"], data["ValueMax"],
                        where(calcs["DeltaM"] < data["CoefMinSgt"], data["ValueMin"],
                        0)) + float(calcs["CoNz"])
                    calcs["sgtft"] = ((calcs["GtFh"] * where(data["Min"] > 75,
                        calcs["Sgmx"], calcs["GtFh"]) * where(where(data["Min"] <
                        46 and data["Min"] > 35), calcs["Sgmx"], calcs["GtHm"] +
                        calcs["gtam"])) / 3) + (calcs["CoNz"] / 3)
                    if calcs["sgtft1"] - data["ValueMax"]:
                        string = 'Over'
                    else:
                        string = 'Under'
                    calcs["U/O"] = f'{string} {data["ValueMax"]}'
                    results_preds.update(calcs)
                    overall_preds.append(results_preds)

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

    return overall_preds, overall_results
