import json
import heapq
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

# ---------------- GRAPH LOADING ----------------
def load_graph(filename):
    """
    Loads graph data from a JSON file.
    JSON format:
    {
        "nodes": {
            "NodeName": [longitude, latitude],
            ...
        },
        "edges": {
            "NodeName": [["NeighborNode", distance_km], ...],
            ...
        }
    }
    """
    with open(filename, 'r') as f:
        return json.load(f)

# ---------------- DIJKSTRA ALGORITHM ----------------
def dijkstra(graph, start, end):
    """
    Custom Dijkstra's Algorithm using heapq for priority queues.
    Finds shortest path and total distance.
    """
    distances = {node: float('inf') for node in graph['nodes']}
    previous = {node: None for node in graph['nodes']}
    distances[start] = 0
    pq = [(0, start)]  # (distance, node)

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph['edges'][current_node]:
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))

    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()
    return path, distances[end]

# ---------------- VISUALIZATION ----------------
def visualize_route(graph, path):
    """
    Plots the full graph and the shortest route using Matplotlib.
    """
    plt.figure(figsize=(7, 7))
    
    # Plot all nodes and edges
    for node, coords in graph['nodes'].items():
        plt.plot(coords[0], coords[1], 'bo', markersize=6)  # Blue points for all nodes
        plt.text(coords[0], coords[1], node, fontsize=8, ha='right')

    for start_node, connections in graph['edges'].items():
        for neighbor, _ in connections:
            x_values = [graph['nodes'][start_node][0], graph['nodes'][neighbor][0]]
            y_values = [graph['nodes'][start_node][1], graph['nodes'][neighbor][1]]
            plt.plot(x_values, y_values, 'gray', linewidth=0.8)  # Light gray for general edges

    # Highlight shortest path
    for i in range(len(path) - 1):
        x_values = [graph['nodes'][path[i]][0], graph['nodes'][path[i+1]][0]]
        y_values = [graph['nodes'][path[i]][1], graph['nodes'][path[i+1]][1]]
        plt.plot(x_values, y_values, 'r', linewidth=2.5)  # Red for path

    plt.title("Optimal Route in Chennai", fontsize=14)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(True)
    plt.show()

# ---------------- TRIP PLANNING ----------------
def plan_trip():
    source = source_entry.get().strip()
    destination = dest_entry.get().strip()

    if source not in graph['nodes'] or destination not in graph['nodes']:
        messagebox.showerror("Error", "Source or Destination not found in graph-data.json.")
        return

    # Get shortest path & distance
    path, distance = dijkstra(graph, source, destination)

    # Speed mapping in km/h
    transport_speeds = {"Bike": 40, "Car": 60, "Bus": 50}
    transport = transport_var.get()
    avg_speed = transport_speeds.get(transport, 50)

    # Calculate travel time in minutes
    duration = (distance / avg_speed) * 60

    # Display in UI
    result_text.set(
        f"Path: {' → '.join(path)}\n"
        f"Distance: {distance:.2f} km\n"
        f"Estimated Time: {int(duration)} minutes ({transport})"
    )

    # Plot route in Matplotlib
    visualize_route(graph, path)

# ---------------- MAIN PROGRAM ----------------
# Load Chennai graph data
graph = load_graph("graph-data.json")  # <-- Should contain Chennai locations

# Create Tkinter window
root = tk.Tk()
root.title("Smart Route Planner - Chennai")
root.geometry("650x450")
root.configure(bg="lightblue")

frame = tk.Frame(root, bg="lightblue")
frame.pack(padx=20, pady=20, fill="both", expand=True)

# Source
tk.Label(frame, text="Source:", font=("Helvetica", 14), bg="lightblue").grid(row=0, column=0, sticky="w")
source_entry = tk.Entry(frame, font=("Helvetica", 14), width=25)
source_entry.grid(row=0, column=1, padx=10, pady=5)

# Destination
tk.Label(frame, text="Destination:", font=("Helvetica", 14), bg="lightblue").grid(row=1, column=0, sticky="w")
dest_entry = tk.Entry(frame, font=("Helvetica", 14), width=25)
dest_entry.grid(row=1, column=1, padx=10, pady=5)

# Transport dropdown
tk.Label(frame, text="Transport:", font=("Helvetica", 14), bg="lightblue").grid(row=2, column=0, sticky="w")
options = ["Car", "Bike", "Bus"]
transport_var = tk.StringVar(value=options[0])
tk.OptionMenu(frame, transport_var, *options).grid(row=2, column=1, pady=10, sticky="ew")

# Plan trip button
tk.Button(frame, text="Plan Trip", font=("Helvetica", 14), command=plan_trip).grid(row=3, column=0, columnspan=2, pady=20)

# Result label
result_text = tk.StringVar()
tk.Label(frame, textvariable=result_text, font=("Helvetica", 14), bg="lightblue", justify="left").grid(row=4, column=0, columnspan=2)

root.mainloop()
