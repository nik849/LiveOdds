def process(data, tc_data, leagues):
    """
    Processing method for returning liveodds from totalcorner request
    """
    results_preds = {}
    results = {}
    for league, coeff in leagues.items():
        print(coeff)

    unwanted_keys = ['h_id', 'a_id', 'hc', 'ac', 'hg', 'ag', 'hrc', 'arc',
                     'hyc', 'ayc', 'hf_hc', 'hf_ac', 'hf_hg', 'hf_ag', 'ish',
                     'hp', 'ap', 'asian_corner']

    for match in tc_data["matches"]:
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
            results.update(calcs)

        elif match["status"] == data["Min"]:
            results_preds.update({'Minute': data["Min"]})
            results_preds.update(match)
    print(results_preds.keys())

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
