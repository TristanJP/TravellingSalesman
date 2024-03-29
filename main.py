###################################
# FIrst Iteration, testing script

import random
from itertools import permutations
import math
import time

travel_map = {
    'a': {'a': 0, 'b': 20, 'c': 42, 'd': 35},
    'b': {'a': 20, 'b': 0, 'c': 30, 'd': 34},
    'c': {'a': 42, 'b': 30, 'c': 0, 'd': 12},
    'd': {'a': 35, 'b': 34, 'c': 12, 'd': 0}
}

# travel_map = {
#     'a': {'a': 0, 'b': 20, 'c': 42, 'd': 35, 'e': 5},
#     'b': {'a': 20, 'b': 0, 'c': 30, 'd': 34, 'e': 10},
#     'c': {'a': 42, 'b': 30, 'c': 0, 'd': 12, 'e': 15},
#     'd': {'a': 35, 'b': 34, 'c': 12, 'd': 0, 'e': 20},
#     'e': {'a': 5, 'b': 10, 'c': 15, 'd': 20, 'e': 0}
# }

def get_list_of_cities(cities_map):
    i = 0
    city_list = []
    for city in cities_map:
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

def distance_between_coords(x1, x2, y1, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def get_cost_of_route(route):
    total = 0
    i = 0

    while i < len(route)-1:
        total += travel_map[route[i]][route[i+1]]
        i += 1
    total += travel_map[route[-1]][route[0]]

    return total

def generate_random_route():
    cities = travel_map['a']
    random.shuffle(cities)
    return cities

def random_find_shortest():
    i = 1
    route_value = 200
    shortest_routes = []
    while i <= 1000:
        new_route = generate_random_route()
        #print(f" {i} + ': ' +  {new_route} + ' - ' + {get_cost_of_route(new_route)}")

        if route_value > get_cost_of_route(new_route):
            shortest_routes = [new_route]
            route_value = get_cost_of_route(new_route)
        elif route_value == get_cost_of_route(new_route):
            if new_route not in shortest_routes:
                shortest_routes += [new_route]

        i += 1
    print(route_value)
    print(shortest_routes)

def get_all_permutations():
    cities = travel_map['a']
    cities[1:] = permutations(cities[1:])
    return cities

def brute_force_shortest():
    all_routes = get_all_permutations()
    print(all_routes)
    shortest_routes = []
    cost = 200
    for route in all_routes:
        new_cost = get_cost_of_route(route)
        if cost > new_cost:
            cost = new_cost
            shortest_routes = [route]
        elif cost == new_cost:
            shortest_routes.append(route)

        #print(f' {route} - {cost}')

    print(f'{cost}:\n{shortest_routes}')

def get_all_city_perms(city_list):
    return list(permutations(city_list))

def get_limited_routes(city_list, limit):
    output = []

    while len(output) < limit:
        copy = city_list[1:]
        random.shuffle(copy)
        city_list[1:] = copy
        if city_list not in output:
            output.append(city_list.copy())
    
    return output

def find_shortest_routes(file_name, route_limit, all_randomly):
    cities_map = get_cities_from_file(file_name)

    cities_list = get_list_of_cities(cities_map)

    if route_limit == None:
        all_routes = get_all_city_perms(cities_list)
        if all_randomly:
            random.shuffle(all_routes)
    else:
        all_routes = get_limited_routes(cities_list, route_limit)    

    shortest_routes = []
    cost = 1000
    i = 1

    for route in all_routes:
        new_cost = get_cost_of_cities_route(route, cities_map)

        #print(f"{i}: {new_cost:.14f} - {route}           [{cost:.14f}]")
        i += 1
        if cost > new_cost:
            cost = new_cost
            shortest_routes = [route]
        # elif cost == new_cost:
        #     shortest_routes.append(route)
    
    print("\n======= FINISHED =======")
    print(f'Shortest Size: {cost}\nShortest Routes:\n{shortest_routes}')

start_time = time.time()

find_shortest_routes("../ulysses16(3).csv", None, False)

end_time = time.time()
print(f"Time: {end_time - start_time}")

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
