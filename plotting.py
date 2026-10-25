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


os.makedirs("figures", exist_ok=True)

# PLOT 1 - robustness curves
fig = go.Figure()
for name in ["er_targeted", "er_random", "ba_targeted", "ba_random"]:
    data = read_csv(f"results/{name}.csv")
    fig.add_trace(go.Scatter(x=data["fraction_removed"], y=data["giant_component"], name=name))
    # essentially one column goes to the x axis, one column goes to the y axis, and the name is used in the legend

# Molloy-Reed threshold for random removal on the ER graph
# should think of how not to hardcode this, but for now it's ok
# maybe have file results/molloy_reed.csv
n_er, er_type, er_edges, er_adj = load_graph_txt("data/er_graph.edgelist")
er_fc = critical_fraction(molloy_reed_criterion(get_degrees(er_adj))["kappa"])
fig.add_vline(x=er_fc, line_dash="dash", annotation_text="ER f_c")

fig.update_layout(
    title="Robustness",
    xaxis_title="fraction of nodes removed",
    yaxis_title="giant component (fraction of n)"
)
fig.write_html("figures/robustness.html")

