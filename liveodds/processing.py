def process(data, nations):
    """
    Processing method for returning liveodds from totalcorner request
    """
    results_preds = {}
    results = {}
    for nation, coeff in nations.items():
        print(coeff)

    results_preds["nation"] = nations.keys()
    results_preds["home"] = 0
    results_preds["away"] = 0
    results_preds["Minute"] = data["Min"]
    results_preds["Gol line"] = data["gol_line"]
    results_preds["U/O"] = None
    results_preds["Odd"] = None

    results["nation"] = nations.keys()
    results["home"] = 0
    results["away"] = 0
    results["Minute"] = data["Min"]
    results["Gol line"] = data["gol_line"]
    results["U/O"] = None
    results["Odd"] = None

    return results_preds, results


# Datk	Delta atk al minuto
# GttpH	Gol teorici da tiri in porta Home
# GttfH	Gol teorici da tiri fuori Home
# GttpH	Gol teorici da tiri in porta Away
# Gttfa	Gol teorici da tiri fuori Away
# GtatpH	Gol teorici da attacchi pericolosi Home
# GtapA	Gol teorici da attacchi pericolosi Away
#
# GtHm	Gol teorici home al min
# gtam	Gol teorici away al min
# SgtM	Somm Gol teorici al Min
# DeltaM	Delta gol teorici
#
# GtFh	Gol teorici home full time
# GtFa	Gol teorici away full time
# sgtft1	Sg total line 1
# sgtft	Sg total line ok
#
# U/O
