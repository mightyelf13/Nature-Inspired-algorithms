import sys
import xml.etree.ElementTree as ET
import numpy as np
# import matplotlib.pyplot as plt

# Parse XML input for VRP instance
def parse_vrp_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    name = root.find('info').find('name').text if root.find('info') is not None else file_path

    # Get node coordinates and identify depot
    nodes = root.find('network').find('nodes').findall('node')
    N = len(nodes)
    coords = [None] * N
    depot_index = None
    for node in nodes:
        node_id = int(node.get('id'))
        x = float(node.find('cx').text)
        y = float(node.find('cy').text)
        coords[node_id - 1] = (x, y)
        if node.get('type') == '0':
            depot_index = node_id - 1

    # Get customer demands
    demands = [0] * N
    for req in root.find('requests').findall('request'):
        node_id = int(req.get('node'))
        qty = float(req.find('quantity').text)
        if abs(qty - round(qty)) < 1e-9:
            qty = int(round(qty))
        demands[node_id - 1] = qty

    # Get vehicle capacity
    cap_elem = root.find('fleet').find('vehicle_profile').find('capacity')
    capacity = float(cap_elem.text)
    if abs(capacity - round(capacity)) < 1e-9:
        capacity = int(round(capacity))

    return name, coords, demands, depot_index, capacity

# Core ACO algorithm to solve VRP
def solve_vrp_aco(coords, demands, depot_index, capacity, ants=10, max_iter=100, alpha=1, beta=3, rho=0.8, Q=100):
    N = len(coords)

    # Compute distance matrix
    coord_array = np.array(coords)
    diff = coord_array[:, None, :] - coord_array[None, :, :]
    dist_matrix = np.sqrt((diff ** 2).sum(axis=2))
    dist_matrix = np.round(dist_matrix, 0)

    # Initialize pheromone matrix
    P = 0.01 * np.ones((N, N))
    best_cost = float('inf')
    best_solution = None
    best_costs_per_iter = []

    for iteration in range(max_iter):
        solutions = []
        costs = []

        # Each ant builds a solution
        for ant in range(ants):
            unvisited = set(range(N))
            if depot_index in unvisited:
                unvisited.remove(depot_index)

            current_node = depot_index
            remaining_capacity = capacity
            route_path = [depot_index]

            while True:
                if not unvisited:
                    if current_node != depot_index:
                        route_path.append(depot_index)
                    break

                if current_node == depot_index:
                    remaining_capacity = capacity

                # Select feasible next nodes
                feasible_nodes = [j for j in unvisited if demands[j] <= remaining_capacity]

                if feasible_nodes:
                    choices = np.array(feasible_nodes)
                    tau = P[current_node, choices]
                    distances = dist_matrix[current_node, choices]
                    attractiveness = np.ones_like(distances)
                    nonzero = distances > 0
                    attractiveness[nonzero] = 1.0 / distances[nonzero]
                    weights = (tau ** alpha) * (attractiveness ** beta)

                    # Normalize to probabilities
                    if weights.sum() == 0:
                        probabilities = np.ones_like(weights) / len(weights)
                    else:
                        probabilities = weights / weights.sum()

                    # Choose next node
                    next_node = int(np.random.choice(choices, p=probabilities))

                    route_path.append(next_node)
                    unvisited.remove(next_node)
                    remaining_capacity -= demands[next_node]
                    current_node = next_node
                else:
                    if current_node != depot_index:
                        route_path.append(depot_index)
                        current_node = depot_index
                    else:
                        break

            # Calculate total cost of route
            total_distance = 0.0
            for i in range(len(route_path) - 1):
                a = route_path[i]
                b = route_path[i + 1]
                total_distance += dist_matrix[int(a), int(b)]

            solutions.append(route_path)
            costs.append(total_distance)

            # Update best if needed
            if total_distance < best_cost:
                best_cost = total_distance
                best_solution = route_path.copy()

        # Evaporate pheromone
        P *= (1 - rho)

        # Add pheromone from each ant
        for path, cost in zip(solutions, costs):
            if cost <= 0:
                continue
            deposit = Q / cost
            for i in range(len(path) - 1):
                a = path[i]
                b = path[i + 1]
                P[a, b] += deposit
                P[b, a] += deposit
        best_costs_per_iter.append(best_cost)


    # Convert flat path to route list
    route_list = []
    current_route = []
    for node in best_solution:
        if node == depot_index:
            if current_route:
                route_list.append(current_route)
                current_route = []
        else:
            current_route.append(int(node))
    if current_route:
        route_list.append(current_route)

    return best_cost, route_list, best_costs_per_iter

# # Plot the routes on a map
# def visualize_routes(coords, depot_index, routes):
#     customer_coords = [coords[i] for i in range(len(coords)) if i != depot_index]
#     cx, cy = zip(*customer_coords)
#     plt.scatter(cx, cy, c='blue', s=20, label='Customer')

#     depot_coord = coords[depot_index]
#     plt.scatter(depot_coord[0], depot_coord[1], c='red', marker='*', s=100, label='Depot')

#     colors = plt.cm.get_cmap('tab10', len(routes))

#     for idx, route in enumerate(routes):
#         route_coords = [depot_coord] + [coords[node] for node in route] + [depot_coord]
#         rx, ry = zip(*route_coords)
#         plt.plot(rx, ry, color=colors(idx), linestyle='-', marker='o', markersize=4, label=f'Route {idx+1}')

#     plt.title('VRP Routes Visualization')
#     plt.xlabel('X Coordinate')
#     plt.ylabel('Y Coordinate')
#     plt.legend(loc='best')
#     plt.grid(True)

# def plot_convergence(best_costs, instance_name):
#     plt.figure(figsize=(8, 5))
#     plt.plot(range(1, len(best_costs) + 1), best_costs, marker='o')
#     plt.title(f"Convergence Plot - {instance_name}")
#     plt.xlabel("Iteration")
#     plt.ylabel("Best Cost So Far")
#     plt.grid(True)
#     plt.tight_layout()
#     plt.show()



# Top-level run function
def run_vrp_instance(file_path, max_iter=100):
    name, coords, demands, depot_index, capacity = parse_vrp_xml(file_path) 
    print(f"Vehicle capacity: {capacity}") # printing capacity

    # Run ACO
    best_cost, best_routes, best_costs_per_iter = solve_vrp_aco(coords, demands, depot_index, capacity, max_iter=max_iter)

    # Print solution
    print("Optimized routes:")
    depot_id = depot_index + 1
    for vidx, route in enumerate(best_routes, start=1):
        route_ids = [node + 1 for node in route]
        print(f" Vehicle {vidx}: {depot_id} -> " + " -> ".join(map(str, route_ids)) + f" -> {depot_id}")
    print(f"Total distance traveled: {best_cost}")

    # # Show visualization
    # plt.figure(figsize=(6, 6))
    # visualize_routes(coords, depot_index, best_routes)
    # plt.show()
    # plot_convergence(best_costs_per_iter, name)


if __name__ == "__main__":
    # Defaults
    default_file = "data_32.xml"
    default_iterations = 100

    # No arguments → use default file and iteration
    if len(sys.argv) == 1:
        file_path = default_file
        max_iter = default_iterations
    # One argument → treat as file, use default iteration
    elif len(sys.argv) == 2:
        file_path = sys.argv[1]
        max_iter = default_iterations
    # Two arguments → file and iteration
    elif len(sys.argv) == 3:
        file_path = sys.argv[1]
        try:
            max_iter = int(sys.argv[2])
        except ValueError:
            print("Iteration count must be an integer.")
            sys.exit(1)
    else:
        print("Usage: python vcp.py [data_file.xml] [max_iterations]")
        sys.exit(1)

    run_vrp_instance(file_path, max_iter)

