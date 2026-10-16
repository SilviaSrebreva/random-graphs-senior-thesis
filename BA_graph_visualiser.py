import math
import tkinter as tk
 
from BA_generator import generate_ba

#canvas constants
CANVAS_SIZE = 600      # the drawing area is 600x600 pixels
NODE_RADIUS = 14        # how big each circle (node) is
AUTO_PLAY_DELAY = 900  #time between steps in milliseconds

def visualise_ba(n,m):
    adj_list, edge_list, history = generate_ba(n, m)

    root = tk.Tk()
    root.title("BA Graph Visualiser")

    canvas = tk.Canvas(
        root,
        width=CANVAS_SIZE,
        height=CANVAS_SIZE,
        bg="white"
    )
    canvas.pack() # to show on screen

    positions = {}

    centre = CANVAS_SIZE / 2
    radius = 200

    #we form a circle around the centre with the n nodes
    #this is how we will draw nodes
    for node in range(n):

        angle = 2 * math.pi * node / n # essentially each node gets 2pi/2 degrtees each

        x = centre + radius * math.cos(angle)
        y = centre + radius * math.sin(angle)

        positions[node] = (x, y)

    def draw_edge(u, v):

        x1, y1 = positions[u]
        x2, y2 = positions[v]

        canvas.create_line(
            x1, y1,
            x2, y2,
            fill="red",
            width=3
        )

    def draw_node(node):
        x, y = positions[node]

        canvas.create_oval(
                x - NODE_RADIUS,
                y - NODE_RADIUS,
                x + NODE_RADIUS,
                y + NODE_RADIUS,
                fill="lightgreen"
            )

        canvas.create_text(
                x,
                y,
                text=str(node)
            )

    def draw_step(step):
        for u, v in history[step]["edges"]: #get the edges value of this step
            draw_edge(u, v)
        node = history[step]["node"] #get the node value of this step in history

        if node is not None:
            draw_node(node)

        if step < len(history) - 1:
            root.after(
                AUTO_PLAY_DELAY,
                draw_step,
                step + 1
            ) #after this amount of time do the following

    #the seed nodes are 0 to m (m0 = m + 1 in the generator), we draw them before the first step
    for node in range(m + 1):
        draw_node(node)

    draw_step(0)

    root.mainloop() #to keep the window open

visualise_ba(10, 2)
        
