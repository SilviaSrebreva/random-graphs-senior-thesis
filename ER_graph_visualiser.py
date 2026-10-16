import math
import tkinter as tk

from ER_generator import generate_erdos_renyi_gnp

#canvas constants
CANVAS_SIZE = 600      # the drawing area is 600x600 pixels
NODE_RADIUS = 14       # how big each circle (node) is
AUTO_PLAY_DELAY = 900  #time between steps in milliseconds


def visualise_er(n, p):
    adj_list, edge_list, history = generate_erdos_renyi_gnp(n, p)

    root = tk.Tk()
    root.title("ER Graph Visualiser")

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

        angle = 2 * math.pi * node / n # essentially each node gets 2pi/n radians each

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

    def draw_step(step):

        for u, v in history[step]["edges"]: #get the edges value of this step
            draw_edge(u, v)

        node = history[step]["node"] #get the node value in history

        if node is not None:

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

        if step < len(history) - 1:
            root.after(
                AUTO_PLAY_DELAY,
                draw_step,
                step + 1
            ) #after this amount of time do the following

    draw_step(0)

    root.mainloop() #to keep the window open


visualise_er(10, 0.3)
