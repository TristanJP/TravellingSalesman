# Current TSP solution

import math
import random
import time

def get_cities_from_file(file_name):
    csv_file = open(file_name, "r")
    cities_map = []
    for line in csv_file:
        city = []
        for coord in line.split(","):
            coord = coord.rstrip()
            city += [float(coord)]
        cities_map += [city]

    return cities_map

def get_list_of_cities(cities_map):
    i = 0
    city_list = []
    while i < len(cities_map):
        city_list += [i]
        i += 1

    return city_list

def get_cost_of_cities_route(route, cities_map):
    total = 0
    i = 0

    while i < len(route)-1:
        total += get_cost_between_cities(cities_map, route[i],route[i+1])
        i += 1
    total += get_cost_between_cities(cities_map, route[-1], route[0])

    return total

def get_cost_between_cities(cities_map, city_1, city_2):

    return distance_between_coords(cities_map[city_1][0],
                                   cities_map[city_2][0],
                                   cities_map[city_1][1],
                                   cities_map[city_2][1])

def distance_between_coords(x1, x2, y1, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def generate_random_route(city_list):
    copy = city_list[1:]
    random.shuffle(copy)
    city_list[1:] = copy
    return city_list

def find_shortest_routes_in_map(cities_map, time_limit):
    cities_list = get_list_of_cities(cities_map)

    shortest_routes = []
    cost = get_cost_of_cities_route(generate_random_route(cities_list), cities_map)
    i = 1
    start_time = time.time()
    elapsed_time = 0
    while elapsed_time < time_limit:
        route = generate_random_route(cities_list)
        print(route)
        new_cost = get_cost_of_cities_route(route, cities_map)

        print(f"{i}: {new_cost:.14f} - {route}           [{cost:.14f}]")
        i += 1
        if cost > new_cost:
            cost = new_cost
            shortest_routes = [route]
        elif cost == new_cost:
            if route not in shortest_routes:
                shortest_routes.append(route)

        elapsed_time = time.time() - start_time
    
    print(f"\n======= FINISHED =======\nShortest Size: {cost}\nShortest Routes:")
    for route in shortest_routes:
        print(route)

    return shortest_routes[0]

def two_opt_swap(route):
    random_cities = random.sample(range(0,len(route)), 2)

    new_route = route.copy()

    new_route[random_cities[0]] = route[random_cities[1]]
    new_route[random_cities[1]] = route[random_cities[0]]
    return new_route

def two_opt_neighbourhood(route):
    neighbourhood = []

    x = len(route)
    y = (x * (((1/2) * x) - (1/2)))

    while len(neighbourhood) < y:
        new_route = two_opt_swap(route)

        if new_route not in neighbourhood:
            neighbourhood.append(new_route)
    
    return neighbourhood

def find_shortest_route_in_neighbourhood(neighbourhood, cities_map):
    shortest_route = [neighbourhood[0]]
    cost = get_cost_of_cities_route(neighbourhood[0], cities_map)
    for route in neighbourhood:
        new_cost = get_cost_of_cities_route(route, cities_map)
        if cost > new_cost:
            cost = new_cost
            shortest_route = [route]

        #print(f' {route} - {cost}')

    print(f'{cost}:\n{shortest_route}')
    return shortest_route


cities_map = get_cities_from_file("ulysses16(1).csv")

rand_shortest = find_shortest_routes_in_map(cities_map, 10)

neighbourhood = two_opt_neighbourhood(rand_shortest)
find_shortest_route_in_neighbourhood(neighbourhood, cities_map)
