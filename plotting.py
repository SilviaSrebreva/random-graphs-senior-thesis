import os
import csv
import plotly.graph_objects as go

from graph_io import load_graph_txt
from molloy_reed import get_degrees, molloy_reed_criterion, critical_fraction

# should run main.py first, this file reads what main.py saved

# i augmented this btw so that it can store stuff
# https://www.geeksforgeeks.org/pandas/reading-csv-files-in-python/
def read_csv(filepath):
    # reads a csv into a dict: column name - list of numbers
    columns = {}
    with open(filepath) as f:
        reader = csv.DictReader(f) # DictReader uses the header line for the column names, every subsequent line it reads becomes a Python dict
        for row in reader:
            for name in row: # this is how we store the data in a dict of lists
                if name not in columns: # this makes sure that if the column name is not already in the dict, we create a new list for it
                    columns[name] = []
                columns[name].append(float(row[name])) #columns[0] apends row[0], which has been transormed with float into a number
                                                        # clumns[0] for examle is "fraction_removed", row[0] is the value in that column for this row, which is a string, so we convert it to a float
    return columns


# PLOT 1 - robustness curves
# er_fc is the Molloy-Reed threshold for random removal on the ER graph
def plot_robustness(er_fc):
    os.makedirs("figures", exist_ok=True)

    fig = go.Figure()
    for name in ["er_targeted", "er_random", "ba_targeted", "ba_random"]:
        data = read_csv(f"results/{name}.csv")
        fig.add_trace(go.Scatter(x=data["fraction_removed"], y=data["giant_component"], name=name))
        # essentially one column goes to the x axis, one column goes to the y axis, and the name is used in the legend

    fig.add_vline(x=er_fc, line_dash="dash", annotation_text="ER f_c")

    fig.update_layout(
        title="Robustness",
        xaxis_title="fraction of nodes removed",
        yaxis_title="giant component (fraction of n)"
    )
    fig.write_html("figures/robustness.html")

# PLOT 2 - SIR time series, one figure for ER and one for BA
def plot_sir():
    os.makedirs("figures", exist_ok=True)

    for name in ["er", "ba"]:
        data = read_csv(f"results/{name}_sir.csv")
        fig = go.Figure() # makes new figure
        fig.add_trace(go.Scatter(x=data["step"], y=data["S"], name="S"))
        fig.add_trace(go.Scatter(x=data["step"], y=data["I"], name="I"))
        fig.add_trace(go.Scatter(x=data["step"], y=data["R"], name="R"))
        fig.update_layout(
            title=f"SIR on {name.upper()}",
            xaxis_title="step",
            yaxis_title="fraction of nodes"
        )
        fig.write_html(f"figures/{name}_sir.html")


if __name__ == "__main__":
    # main.py passes er_fc in directly, here we calculate it again from the saved ER graph
    # maybe have a file results/molloy_reed.csv
    n_er, er_type, er_edges, er_adj = load_graph_txt("data/er_graph.edgelist")
    er_fc = critical_fraction(molloy_reed_criterion(get_degrees(er_adj))["kappa"])

    plot_robustness(er_fc)
    plot_sir()
    print("plots saved in figures/")