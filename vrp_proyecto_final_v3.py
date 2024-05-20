import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import filedialog
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import pandas as pd

def load_csv_file():
    filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if filename:
        df = pd.read_csv(filename)
        distance_matrix = df.values.tolist()
        data = {}
        data["distance_matrix"] = distance_matrix
        data["num_vehicles"] = 4
        data["starts"] = [1, 2, 15, 16]
        data["ends"] = [0, 0, 0, 0]
        return data
    else:
        return None

def create_data_model():
    data = load_csv_file()
    if data is None:
        messagebox.showerror("Error", "No file selected or file could not be read")
    return data

def print_solution(data, manager, routing, solution, output_text):
    output_text.insert(tk.END, f"Objetivo: {solution.ObjectiveValue()}\n")
    max_route_distance = 0
    for vehicle_id in range(data["num_vehicles"]):
        index = routing.Start(vehicle_id)
        plan_output = f"Ruta del vehiculo {vehicle_id}:\n"
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output += f" {manager.IndexToNode(index)} -> "
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id
            )
        plan_output += f"{manager.IndexToNode(index)}\n"
        plan_output += f"Distancia de la ruta: {route_distance}m\n"
        output_text.insert(tk.END, plan_output + "\n")
        max_route_distance = max(route_distance, max_route_distance)
    output_text.insert(tk.END, f"Ruta más larga: {max_route_distance}m\n")

def solve_vrp(output_text):
    output_text.delete(1.0, tk.END)  # Clear previous output
    try:
        data = create_data_model()
        
        manager = pywrapcp.RoutingIndexManager(
            len(data["distance_matrix"]), data["num_vehicles"], data["starts"], data["ends"]
        )

        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return data["distance_matrix"][from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
        
        dimension_name = "Distance"
        routing.AddDimension(
            transit_callback_index,
            0,
            2000,
            True,
            dimension_name,
        )
        distance_dimension = routing.GetDimensionOrDie(dimension_name)
        distance_dimension.SetGlobalSpanCostCoefficient(100)

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        )

        solution = routing.SolveWithParameters(search_parameters)

        if solution:
            print_solution(data, manager, routing, solution, output_text)
        else:
            output_text.insert(tk.END, "No se encontró solución\n")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def main():
    # Crear la ventana principal
    root = tk.Tk()
    root.title("Solución VRP")
    root.geometry("800x600")
    root.configure(bg="#f0f0f0")

    # Crear el frame principal
    main_frame = tk.Frame(root, bg="#f0f0f0")
    main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Crear el área de texto para mostrar la solución
    output_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=80, height=20, font=("Arial", 12), bg="#ffffff")
    output_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    # Crear el botón para ejecutar el algoritmo
    solve_button = tk.Button(main_frame, text="Resolver VRP", command=lambda: solve_vrp(output_text), font=("Arial", 14, "bold"), bg="#4CAF50", fg="#ffffff", relief=tk.RAISED, padx=10, pady=5)
    solve_button.pack(pady=10)
    
    load_button = tk.Button(root, text='Load CSV', command=create_data_model, font=("Arial", 14, "bold"), bg="#4CAF50", fg="#ffffff", relief=tk.RAISED, padx=10, pady=5)
    load_button.pack(pady=10)

    # Ejecutar el bucle principal de la ventana
    root.mainloop()

if __name__ == "__main__":
    main()
