def process(data, tc_data, leagues):
    """
    Processing method for returning liveodds from totalcorner request
    """
    results_preds = {}
    results = {}
    for league, coeff in leagues.items():
        print(coeff)

    for match in tc_data["matches"]:
        if match["status"] == 'full':
            results.update(match)
        elif match["status"] is not None:
            results_preds.update(match)

    return results_preds, results
