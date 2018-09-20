import os.path
import math
import timeit

#21282 optimal 100 cost
cities = {}


def nearest_neighbor(graph, start_city):
    route = [start_city]
    total_cost = 0
    cost = {}
    current_city = start_city
    next_city = None

    cities_left = {}
    for city in graph:
        cities_left[city] = 'x'
    cities_left.pop(start_city)
    while cities_left:
        lowest_cost = float('inf')
        for city in cities_left:
            cost[city] = int(math.sqrt(((int(graph[current_city]['x']) - int(graph[city]['x'])) ** 2) +
                                       ((int(graph[current_city]['y']) - int(graph[city]['y'])) ** 2)))
            if cost[city] < lowest_cost:
                lowest_cost = cost[city]
                next_city = city
        total_cost += lowest_cost
        route.append(next_city)
        cities_left.pop(next_city)
        current_city = next_city

    route.append(start_city)
    total_cost += int(math.sqrt(((int(graph[start_city]['x']) - int(graph[current_city]['x'])) ** 2) +
                                ((int(graph[start_city]['y']) - int(graph[current_city]['y'])) ** 2)))

    return route, total_cost


"""
while True:
    problem = str(input("how many cities? 100, 150 or 200:"))

    SourceFile = 'Krolak'
    SourceFile += str(problem)
    SourceFile += '.txt'

    if os.path.exists(SourceFile) is True:
        with open(SourceFile) as File:
            for line in File:
                city, x_coord, y_coord = line.split()
                cities[city] = {'x': x_coord, 'y': y_coord}
        Start = str(input("Please enter starting city: "))
        route, total_cost = nearest_neighbor(cities, Start)
        
        for city in route:
            print(city, end="-")
            last_city = city
        print(Start)
        print("Total Cost: {} units".format(total_cost)) 
        cities.clear()
        
    else:
        print("please select a valid option")
"""


def taboo_search(graph, start_city):

    recency_list = [0] * len(graph)
    for i in range(len(recency_list)):
        recency_list[i] = [0] * (len(graph))

    frecuency_list = [0] * len(graph)
    for i in range(len(recency_list)):
        frecuency_list[i] = [0] * (len(graph))

    sub_route = []
    best_route = []
    best_sub_route = []

    route, route_cost = nearest_neighbor(graph, start_city)

    iterations_needed = 100
    penalization = 400
    max_frecuency = 5
    taboo_time = 2

    first = 0
    second = 0
    for city in route:
        best_route.append(city)

    print(route_cost)
    print(route)
    for iterations in range(iterations_needed):
        print("iteration ", iterations+1)
        lowest_cost = float('inf')
        for first_city in range(1, len(route)-2):
            for second_city in range(first_city+1, len(route)-1):
                sub_route.clear()
                for route_city in route:
                    sub_route.append(route_city)
                temporary_city = sub_route[first_city]
                sub_route[first_city] = sub_route[second_city]
                sub_route[second_city] = temporary_city

                if recency_list[first_city][second_city] > 0:
                    pass
                else:
                    sub_route_cost = calculate_route_cost(graph, sub_route)
                    if frecuency_list[first_city][second_city] > max_frecuency:
                        sub_route_cost += penalization
                    if sub_route_cost < lowest_cost:
                        lowest_cost = sub_route_cost
                        best_sub_route.clear()
                        for sub_route_city in sub_route:
                            best_sub_route.append(sub_route_city)
                        sub_route.clear()
                        first = first_city
                        second = second_city
        recency_list[first][second] = taboo_time
        frecuency_list[first][second] += 1

        for first_city in range(1, len(route)-2):
            for second_city in range(first_city+1, len(route)-1):
                if recency_list[first_city][second_city] > 0:
                    recency_list[first_city][second_city] -= 1

        route.clear()
        for city in best_sub_route:
            route.append(city)
        if lowest_cost < route_cost:
            best_route.clear()
            for city in best_sub_route:
                best_route.append(city)
            route_cost = lowest_cost
            print(route_cost)

    print(best_route)
    print(route_cost)


def calculate_route_cost(graph, route):
    cost = 0
    last_city = None
    for city in route:
        if last_city is None:
            last_city = city
        else:
            cost += int(math.sqrt(((int(graph[last_city]['x']) - int(graph[city]['x'])) ** 2) +
                                  ((int(graph[last_city]['y']) - int(graph[city]['y'])) ** 2)))
            last_city = city

    return cost


with open('Krolak200.txt') as File:
    for line in File:
        city, x_coord, y_coord = line.split()
        cities[city] = {'x': x_coord, 'y': y_coord}
start_time = timeit.default_timer()
taboo_search(cities, '1')
print("time", timeit.default_timer()-start_time)