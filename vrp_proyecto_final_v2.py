import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def create_data_model():
    data = {}
    data["distance_matrix"] = [
        # fmt: off
      [0, 548, 776, 696, 582, 274, 502, 194, 308, 194, 536, 502, 388, 354, 468, 776, 662],
      [548, 0, 684, 308, 194, 502, 730, 354, 696, 742, 1084, 594, 480, 674, 1016, 868, 1210],
      [776, 684, 0, 992, 878, 502, 274, 810, 468, 742, 400, 1278, 1164, 1130, 788, 1552, 754],
      [696, 308, 992, 0, 114, 650, 878, 502, 844, 890, 1232, 514, 628, 822, 1164, 560, 1358],
      [582, 194, 878, 114, 0, 536, 764, 388, 730, 776, 1118, 400, 514, 708, 1050, 674, 1244],
      [274, 502, 502, 650, 536, 0, 228, 308, 194, 240, 582, 776, 662, 628, 514, 1050, 708],
      [502, 730, 274, 878, 764, 228, 0, 536, 194, 468, 354, 1004, 890, 856, 514, 1278, 480],
      [194, 354, 810, 502, 388, 308, 536, 0, 342, 388, 730, 468, 354, 320, 662, 742, 856],
      [308, 696, 468, 844, 730, 194, 194, 342, 0, 274, 388, 810, 696, 662, 320, 1084, 514],
      [194, 742, 742, 890, 776, 240, 468, 388, 274, 0, 342, 536, 422, 388, 274, 810, 468],  
      [536, 1084, 400, 1232, 1118, 582, 354, 730, 388, 342, 0, 878, 764, 730, 388, 1152, 354],
      [502, 594, 1278, 514, 400, 776, 1004, 468, 810, 536, 878, 0, 114, 308, 650, 274, 844],
      [388, 480, 1164, 628, 514, 662, 890, 354, 696, 422, 764, 114, 0, 194, 536, 388, 730],
      [354, 674, 1130, 822, 708, 628, 856, 320, 662, 388, 730, 308, 194, 0, 342, 422, 536],
      [468, 1016, 788, 1164, 1050, 514, 514, 662, 320, 274, 388, 650, 536, 342, 0, 764, 194],
      [776, 868, 1552, 560, 674, 1050, 1278, 742, 1084, 810, 1152, 274, 388, 422, 764, 0, 798],
      [662, 1210, 754, 1358, 1244, 708, 480, 856, 514, 468, 354, 844, 730, 536, 194, 798, 0],
    ]
    data["num_vehicles"] = 4
    data["starts"] = [1, 2, 15, 16]
    data["ends"] = [0, 0, 0, 0]
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

    # Ejecutar el bucle principal de la ventana
    root.mainloop()

if __name__ == "__main__":
    main()
