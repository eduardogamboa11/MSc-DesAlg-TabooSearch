import random

cities = {'La Paz': {'Mexicali': 1357},
          'Mexicali': {'La Paz': 1357, 'Hermosillo': 702},
          'Hermosillo': {'Mexicali': 702, 'Chihuahua': 696, 'Culiacan': 693},
          'Chihuahua': {'Hermosillo': 696, 'Durango': 685, 'Saltillo': 728},
          'Saltillo': {'Chihuahua': 728, 'Durango': 506, 'Monterrey': 87, 'Zacatecas': 382},
          'Monterrey': {'Saltillo': 87, 'Ciudad Victoria': 284, 'San Luis Potosi': 514},
          'Ciudad Victoria': {'Monterrey': 284, 'San Luis Potosi': 332},
          'Culiacan': {'Hermosillo': 693, 'Durango': 463, 'Tepic': 482},
          'Durango': {'Culiacan': 463, 'Tepic': 468, 'Chihuahua': 685, 'Saltillo': 506, 'Zacatecas': 289},
          'Zacatecas': {'Durango': 289, 'Saltillo': 382, 'San Luis Potosi': 195, 'Aguascalientes': 124},
          'San Luis Potosi': {'Monterrey': 514, 'Ciudad Victoria': 332, 'Zacatecas': 195, 'Guadalajara': 336,
                              'Aguascalientes': 177, 'Guanajuato': 206, 'Queretaro': 213},
          'Tepic': {'Guadalajara': 209, 'Culiacan': 482, 'Durango': 468, 'Colima': 371},
          'Guadalajara': {'Tepic': 209, 'San Luis Potosi': 336, 'Aguascalientes': 221, 'Colima': 198, 'Morelia': 288,
                          'Guanajuato': 292},
          'Aguascalientes': {'Guadalajara': 221, 'San Luis Potosi': 177, 'Zacatecas': 124, 'Guanajuato': 196},
          'Guanajuato':{'Aguascalientes': 196, 'Guadalajara': 292, 'San Luis Potosi': 206, 'Queretaro': 124,
                        'Morelia': 178},
          'Queretaro':{'Guanajuato': 124, 'San Luis Potosi': 213, 'Morelia': 190, 'Pachuca': 225, 'Toluca': 199},
          'Colima': {'Guadalajara': 198, 'Tepic': 371, 'Morelia': 478},
          'Morelia': {'Queretaro': 190, 'Guanajuato': 178, 'Guadalajara': 288, 'Colima': 478, 'Toluca': 236,
                      'Pachuca': 320},
          'Toluca': {'Pachuca': 176, 'Morelia': 236, 'Queretaro': 199},
          'Pachuca': {'Toluca': 176, 'Queretaro': 225, 'Morelia': 320}
          }


def get_shortest_path(weighted_graph, start, end):
    nodes_to_visit = {start}
    visited_nodes = set()
    # Distance from start to start is 0
    distance_from_start = {start: 0}
    tentative_parents = {}

    while nodes_to_visit:
        # The next node should be the one with the smallest weight
        current = min([(distance_from_start[node], node) for node in nodes_to_visit])[1]
        # The end was reached
        if current == end:
            break

        nodes_to_visit.discard(current)
        visited_nodes.add(current)

        edges = weighted_graph[current]
        unvisited_neighbours = set(edges).difference(visited_nodes)
        for neighbour in unvisited_neighbours:
            neighbour_distance = distance_from_start[current] + edges[neighbour]

            if neighbour_distance < distance_from_start.get(neighbour, float('inf')):
                distance_from_start[neighbour] = neighbour_distance
                tentative_parents[neighbour] = current
                nodes_to_visit.add(neighbour)

    print("Distance from {} to {} is {} km".format(start, end, distance_from_start[end]))
    print("You should follow the route:", end=" ")

    return _deconstruct_path(tentative_parents, end)


def _deconstruct_path(tentative_parents, end):
    if end not in tentative_parents:
        return None
    cursor = end
    path = []
    while cursor:
        path.append(cursor)
        cursor = tentative_parents.get(cursor)
    actual_path = list(reversed(path))
    route = ""
    index = 0
    for city in actual_path:
        if index is len(actual_path)-1:
            route += city
        else:
            route += city + " - "
        index += 1

    return route


def prim_algorithm(graph, start=None):
    if start is None:
        Start = random.choice(list(graph.keys()))
    else:
        Start = start
    predecessor = {}  # pair {vertex: predecesor in MST}
    key = {}  # keep track of minimum weight for each vertex
    priority_queue = {}  # priority queue implemented as dictionary

    for city in graph:
        predecessor[city] = -1
        key[city] = float('inf')
    key[Start] = 0
    for city in graph:
        priority_queue[city] = key[city]

    while priority_queue:
        neighbour = pop_min(priority_queue)
        for city in graph[neighbour]:  # all neighbors of v
            if city in priority_queue and graph[neighbour][city] < key[city]:
                predecessor[city] = neighbour
                key[city] = graph[neighbour][city]
                priority_queue[city] = graph[neighbour][city]

    return predecessor, key


def tsp_route(graph, predecessor_list, start):
    route = [start]
    current = start
    children = []
    costs = []
    next_city = start
    while len(route) != len(predecessor_list):
        children += (graph[current].keys())
        costs += (graph[current].values())
        min_distance = 99999
        for i in range(0, len(children)):
            if predecessor_list[children[i]] == current:
                if children[i] in route:
                    pass
                else:
                    if costs[i] < min_distance:
                        min_distance = costs[i]
                        next_city = children[i]
            else:
                pass
        if min_distance == 99999:
            next_city = predecessor_list[current]
        else:
            route.append(next_city)
        current = next_city
        children.clear()
        costs.clear()

    for city in route:
            print(city, end = "-")
    print(start)


def pop_min(priority_queue):
    lowest = float('inf')
    key_lowest = None
    for key in priority_queue:
        if priority_queue[key] < lowest:
            lowest = priority_queue[key]
            key_lowest = key
    del priority_queue[key_lowest]
    return key_lowest


mst,distance = prim_algorithm(cities)

print("Minimum Spanning Tree Connections")
total_distance = 0
for city in mst:
    if mst[city] is -1:
        start_city = city
        total_distance += distance[city]
    else:
        print(city, "-", mst[city])
        total_distance += distance[city]

print("Total Distance:", total_distance)

while True:
    print("Please enter what do you want to do: ")
    Option = str(input("1 for SPA, 2 for TSP:"))
    if Option is '1':
        Start = str(input("Please enter starting city: "))
        Destination = str(input("Please enter destination: "))
        print(get_shortest_path(cities, Start, Destination))
    elif Option is '2':
        Start = str(input("Please enter starting city: "))
        mst, distance = prim_algorithm(cities, Start)
        tsp_route(cities, mst, Start)
