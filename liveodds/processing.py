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
                     'hp', 'ap']
    for match in tc_data["matches"]:
        if match["status"] == 'full':
            results.update(match)
        elif match["status"] is not None:
            results_preds.update(match)
    print(results_preds.keys())

    if len(results) > 0:
        for key in unwanted_keys:
            del results[key]
    if len(results_preds) > 0:
        for key in unwanted_keys:
            del results_preds[key]

    return results_preds, results
