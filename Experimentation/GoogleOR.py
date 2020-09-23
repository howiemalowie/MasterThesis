"""Capacited Vehicles Routing Problem (CVRP)."""

from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

import math


def create_data_model(link_mat, tour_limit, depot):
    """Stores the data for the problem."""
    data = {}
    n = len(link_mat[depot])
    matrix = [[0 for i in range(n)] for j in range(n)]

    index = dict()
    id = dict()
    cnt = 0
    for i in link_mat.keys():
        if i == depot:
            data['depot'] = cnt
        index[i] = cnt
        id[cnt] = i
        cnt += 1
    for i in link_mat.keys():
        for j in link_mat[i].keys():
            matrix[index[i]][index[j]] = int(link_mat[i][j]*1000000)
    data['distance_matrix'] = matrix
    data['num_vehicles'] = math.ceil(n/tour_limit)
    data['demands'] = [1 for x in range(n)]
    data['demands'][index[depot]] = 0
    data['vehicle_capacities'] = [tour_limit for x in range(data['num_vehicles'])]
    return data, id


def print_solution(data, manager, routing, solution, id):
    """Prints solution on console."""
    total_distance = 0
    total_load = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data['demands'][node_index]
            plan_output += ' {0} Load({1}) -> '.format(id[node_index], route_load)
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += ' {0} Load({1})\n'.format(id[manager.IndexToNode(index)],
                                                 route_load)
        plan_output += 'Distance of the route: {}m\n'.format(route_distance/1000000)
        plan_output += 'Load of the route: {}\n'.format(route_load)
        print(plan_output)
        total_distance += route_distance
        total_load += route_load
    print('Total distance of all routes: {}m'.format(total_distance/1000000))
    print('Total load of all routes: {}'.format(total_load))
    return total_distance


def OR(link_mat, tour_limit, depot):
    """Solve the CVRP problem."""
    # Instantiate the data problem.
    data, id = create_data_model(link_mat, tour_limit, depot)

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)


    # Add Capacity constraint.
    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(
        demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data['vehicle_capacities'],  # vehicle maximum capacities
        True,  # start cumul to zero
        'Capacity')

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.time_limit.seconds = 5
    search_parameters.log_search = False

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        return print_solution(data, manager, routing, solution, id)