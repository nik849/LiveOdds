from numpy import where


def process(data, tc_data, leagues):
    """
    Processing method for returning liveodds from totalcorner request
    """
    overall_results = []
    overall_preds = []
    results_preds = {}
    league_dict = {}
    results = {}
    teams = []
    for match in tc_data:
        teams.append(match["h"])
        teams.append(match["a"])
        league_dict.update({match.get("h"):0})
        league_dict.update({match.get("a"):0})

    leagueset = set(list(leagues.keys()))
    teamset = set(teams)
    for league, coeff in leagues.items():
        league_dict[league] = coeff

    for match in tc_data:
        gol_linestr = match["p_goal_h"][0].strip("'").split(", ")
        try:
            gol_line = float(gol_linestr)
        except TypeError:
            try:
                gol_line = max([float(x) for x in gol_linestr])
            except ValueError:
                gol_line = 0
        if match["status"] == 'half':
            match["status"] = 45
        if int(data["Min"]) == int(match["status"]):
            calcs = {}
            unwanted_keys = ['h_id', 'a_id', 'hc', 'ac', 'hrc', 'arc',
                             'hyc', 'ayc', 'hf_hc', 'hf_ac', 'hf_hg', 'hf_ag', 'ish',
                             'hp', 'ap', 'asian_corner']
            calcs.update({'Minute': match["status"]})
            #results_preds.update(match)
            calcs["Nation"] = f'{match["h"]} vs {match["a"]}'
            calcs["CoNz"] = float(league_dict.get(match["h"]))
            if calcs["CoNz"] == 0:
                calcs["CoNz"] = float(league_dict.get(match["a"]))
            match["attacks_h"] = []
            match["shot_on_h"] = []
            calcs["Datk"] = round((float(match["dang_attacks"][0]) - float(match["dang_attacks"][1]))\
                / float(data["Min"]), 2)
            calcs["GttpH"] = float(match["shot_on"][0]) * float(data["Ptph"])
            calcs["GttfH"] = float(match["shot_off"][0]) * float(data["Ptfh"])
            calcs["GttpA"] = float(match["shot_on"][1]) * float(data["Ptpa"])
            calcs["GttfA"] = float(match["shot_off"][1]) * float(data["Ptfa"])
            calcs["GtapH"] = float(match["dang_attacks"][0]) * float(data["PAtpH"])
            calcs["GtapA"] = float(match["dang_attacks"][0]) * float(data["Patpa"])
            calcs["GtHm"] = int((calcs["GttpH"] + calcs["GttfH"] + calcs["GtapH"])\
                + calcs["Datk"] / 3)
            calcs["gtam"] = int((calcs["GttpH"] + calcs["GttfH"] + calcs["GtapH"])\
                - calcs["Datk"] / 3)

            calcs["SgtM"] = where((where(calcs["GtHm"] < float(data["CofMinH"]), 0,
                                  calcs["GtHm"]) + where(calcs["gtam"] <
                                  float(data["CofMinA"]), 0, calcs["gtam"])
                                  + calcs["CoNz"] < 0), 0, (where(calcs["GtHm"] < calcs["gtam"], 0, calcs["GtHm"])
                                  + where(calcs["gtam"] < float(data["CofMinA"]), 0, calcs["gtam"]) + calcs["CoNz"]))

            calcs["Sgmx"] = int(match["hg"]) + int(match["ag"])

            calcs["DeltaM"] = round(((
                float(match["hg"]) - float(calcs["GtHm"])) * (float(match["ag"]) -
                calcs["gtam"]) * (float(calcs["Sgmx"]) - float(calcs["SgtM"])
                                 )) / 3, 2)
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

            calcs["sgtft1"] = round(where(calcs["GtFh"] < 0, 5, calcs["GtFh"]) + \
                where(calcs["GtFa"] < 0, 7, calcs["GtFa"]) + \
                where(calcs["DeltaM"] > data["CoefMaxSgt"], data["ValueMax"],
                where(calcs["DeltaM"] < data["CoefMinSgt"], data["ValueMin"],
                0)) + float(calcs["CoNz"]), 2)

            calcs["sgtft"] = round(((calcs["sgtft1"] * where(float(data["Min"]) > 75,
                calcs["Sgmx"], calcs["sgtft1"]) * where((float(data["Min"]) <
                46 and float(data["Min"]) > 35), calcs["Sgmx"], (calcs["GtHm"] +
                calcs["gtam"]))) / 3) + (calcs["CoNz"] / 3), 2)

            i_goalstr = match["i_goal"][0].strip("'").split(", ")
            try:
                i_goal = float(i_goalstr)
            except TypeError:
                try:
                    i_goal = max([float(x) for x in i_goalstr])
                except ValueError:
                    i_goal = 0

            if calcs["sgtft1"] - i_goal:
                string = 'Over'
            else:
                string = 'Under'
            calcs["U/O"] = f'{string} {gol_line}'

            print(match)
            overall_preds.append(calcs)

        if match["status"] == 'full':
            calcs = {}
            unwanted_keys = ['h_id', 'a_id', 'hc', 'ac', 'hrc', 'arc',
                             'hyc', 'ayc', 'hf_hc', 'hf_ac', 'hf_hg', 'hf_ag', 'ish',
                             'hp', 'ap', 'asian_corner']

            calcs.update({'Minute': match["status"]})
            #results_preds.update(match)
            calcs["Nation"] = f'{match["h"]} vs {match["a"]}'
            calcs["CoNz"] = float(league_dict.get(match["h"]))
            if calcs["CoNz"] == 0:
                calcs["CoNz"] = float(league_dict.get(match["a"]))
            match["attacks_h"] = []
            match["shot_on_h"] = []
            calcs["Datk"] = round((float(match["dang_attacks"][0]) - float(match["dang_attacks"][1]))\
                / float(data["Min"]), 2)
            calcs["GttpH"] = float(match["shot_on"][0]) * float(data["Ptph"])
            calcs["GttfH"] = float(match["shot_off"][0]) * float(data["Ptfh"])
            calcs["GttpA"] = float(match["shot_on"][1]) * float(data["Ptpa"])
            calcs["GttfA"] = float(match["shot_off"][1]) * float(data["Ptfa"])
            calcs["GtapH"] = float(match["dang_attacks"][0]) * float(data["PAtpH"])
            calcs["GtapA"] = float(match["dang_attacks"][0]) * float(data["Patpa"])
            calcs["GtHm"] = int((calcs["GttpH"] + calcs["GttfH"] + calcs["GtapH"])\
                + calcs["Datk"] / 3)
            calcs["gtam"] = int((calcs["GttpH"] + calcs["GttfH"] + calcs["GtapH"])\
                - calcs["Datk"] / 3)

            calcs["SgtM"] = where((where(calcs["GtHm"] < float(data["CofMinH"]), 0,
                                  calcs["GtHm"]) + where(calcs["gtam"] <
                                  float(data["CofMinA"]), 0, calcs["gtam"])
                                  + calcs["CoNz"] < 0), 0, (where(calcs["GtHm"] < calcs["gtam"], 0, calcs["GtHm"])
                                  + where(calcs["gtam"] < float(data["CofMinA"]), 0, calcs["gtam"]) + calcs["CoNz"]))

            calcs["Sgmx"] = int(match["hg"]) + int(match["ag"])

            calcs["DeltaM"] = ((
                float(match["hg"]) - float(calcs["GtHm"])) * (float(match["ag"]) -
                calcs["gtam"]) * (float(calcs["Sgmx"]) - float(calcs["SgtM"])
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

            calcs["sgtft"] = ((calcs["sgtft1"] * where(float(data["Min"]) > 75,
                calcs["Sgmx"], calcs["sgtft1"]) * where((float(data["Min"]) <
                46 and float(data["Min"]) > 35), calcs["Sgmx"], (calcs["GtHm"] +
                calcs["gtam"]))) / 3) + (calcs["CoNz"] / 3)

            if calcs["sgtft1"] - gol_line:
                string = 'Over'
            else:
                string = 'Under'
            calcs["U/O"] = f'{string} {gol_line}'
            overall_results.append(calcs)

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
