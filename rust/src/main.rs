extern crate rand;

use std::env;
use std::fs;
use rand::prelude::*;
use permutohedron::heap_recursive;
use std::time::{{Instant}};

fn main() {

    let args: Vec<String> = env::args().collect();
    let filename = &args[1];

    let start_timer = Instant::now();

    let cities_map = get_cities_from_file(filename);
    let mut cities_list = get_cities_list(&cities_map);

    // println!("{:?}", cities_list);
    // generate_random_route(&mut cities_list);
    // println!("{:?}", cities_list);
    // println!("{}", cities_map.get(0).unwrap()[0]);
    // println!("{}", cities_map.get(0).unwrap()[1]);
    // println!("{}", get_cost_between_cities(cities_list[0], cities_list[1], &cities_map));
    // println!("{}", get_cost_of_route(&cities_list, &cities_map));
    // println!("{}", get_all_route_permutations(&mut cities_list).len());
    // get_shortest_route_with_perms(&cities_map, &mut cities_list);
    // println!("{:?}", get_neighbourhood(&mut cities_list));

    get_shortest_route_with_neighbourhood(&cities_map, &mut cities_list, 1000);

     let end_timer = Instant::now();
     println!("\n\nTime: {:?}\n========================================", end_timer.duration_since(start_timer));

}

fn get_cities_from_file(filename: &str) -> Vec<[f32; 2]> {
    let contents = fs::read_to_string(filename)
        .expect("Something went wrong reading the file");

    let lines = contents.lines();
    let mut cities_map: Vec<[f32; 2]> = Vec::new();

    for line in lines {
        let coords: Vec<&str> = line.split(",").collect();
        //println!("x: {0}, y: {1}", coords[0], coords[1]);
        cities_map.push([coords[0].parse::<f32>().unwrap(), coords[1].parse::<f32>().unwrap()]);
    }
    cities_map
}

fn get_cities_list(cities_map: &Vec<[f32; 2]>) -> Vec<i32> {
    let mut city_list: Vec<i32> = Vec::new();
    let mut i: i32 = 0;
    for _city in cities_map {
        city_list.push(i);
        i = i + 1;
    }
    city_list
}

fn generate_random_route(cities_list: &mut Vec<i32>) -> &Vec<i32> {
    let mut rng = rand::thread_rng();
    cities_list.shuffle(&mut rng);
    cities_list
}

fn get_all_route_permutations(route: &mut Vec<i32>) -> Vec<Vec<i32>> {
    let mut permutations = Vec::new();
    heap_recursive(route, |permutation| {
        permutations.push(permutation.to_vec())
    });
    permutations
}

fn get_cost_between_cities(city_1: i32, city_2: i32, cities_map: &Vec<[f32; 2]>) -> f32 {
    let x1: &f32 = &cities_map.get(city_1 as usize).unwrap()[0];
    let y1: &f32 = &cities_map.get(city_1 as usize).unwrap()[1];
    let x2: &f32 = &cities_map.get(city_2 as usize).unwrap()[0];
    let y2: &f32 = &cities_map.get(city_2 as usize).unwrap()[1];
    
    ((x1 - x2).powf(2.0) + (y1 - y2).powf(2.0)).sqrt()
}

fn get_cost_of_route(route: &Vec<i32>, cities_map: &Vec<[f32; 2]>) -> f32 {
    let mut i: i32 = 0;
    let size: i32 = route.len() as i32;
    let mut total: f32 = 0.0;
    while i < size - 1 {
        total = total + get_cost_between_cities(route[i as usize], route[(i + 1) as usize], cities_map);
        i = i + 1;
    }
    total + get_cost_between_cities(route[i as usize], route[0 as usize], cities_map)
}

fn get_shortest_route_with_perms(cities_map: &Vec<[f32; 2]>, cities_list: &mut Vec<i32>) {

    let mut shortest_cost: f32 = get_cost_of_route(&cities_list, cities_map);
    let mut shortest_route: Vec<i32> = cities_list.as_slice().to_vec();

    for route in get_all_route_permutations(cities_list) {
        let new_cost: f32 = get_cost_of_route(&route, cities_map);

        if new_cost < shortest_cost {
            shortest_cost = new_cost;
            shortest_route = route.as_slice().to_vec();
        }
    }

    println!("\n===================== FINISHED =====================");
    println!("Shortest Route: {:?}\n Cost: {}", shortest_route, &shortest_cost);
}

fn get_neighbourhood(route: &mut Vec<i32>) -> Vec<Vec<i32>> {
    let mut neighbourhood: Vec<Vec<i32>> = Vec::new();
    let mut city_1: i32 = 0;
    while city_1 < route.len() as i32 {
        let mut city_2: i32 = 0;
        while city_2 < route.len() as i32 {
            let mut new_route: Vec<i32> = route.as_slice().to_vec();
            new_route[city_1 as usize] = route[city_2 as usize] + 0;
            new_route[city_2 as usize] = route[city_1 as usize] + 0;
            if !neighbourhood.contains(&new_route) {
                neighbourhood.push(new_route);
            }
            city_2 = city_2 + 1;
        }
        city_1 = city_1 + 1;
    }
    neighbourhood
}

fn get_shortest_in_neighbourhood(neighbourhood: &mut Vec<Vec<i32>>, cities_map: &Vec<[f32; 2]>) -> (Vec<i32>, f32) {
    let mut shortest_cost: f32 = get_cost_of_route(&neighbourhood[0], cities_map);
    let mut shortest_route: Vec<i32> = neighbourhood[0].as_slice().to_vec();

    for route in neighbourhood {
        let new_cost: f32 = get_cost_of_route(&route, cities_map);

        if new_cost < shortest_cost {
            shortest_cost = new_cost;
            shortest_route = route.as_slice().to_vec();
        }
    }
    (shortest_route, shortest_cost)
}

fn get_shortest_route_with_neighbourhood(cities_map: &Vec<[f32; 2]>, city_list: &mut Vec<i32>, time_limit: u128) {
    let start_time = Instant::now();

    let mut shortest_route = generate_random_route(city_list).as_slice().to_vec();
    let mut route = shortest_route.as_slice().to_vec();

    let mut elapsed_time: u128 = 0;
    let mut i: i32 = 1;

    while elapsed_time < time_limit {
        let mut neighbourhood = get_neighbourhood(&mut route);
        let new_route_and_cost = get_shortest_in_neighbourhood(&mut neighbourhood, cities_map);

        if route == new_route_and_cost.0 {  
            let new_cost = new_route_and_cost.1;

            if new_cost < get_cost_of_route(&shortest_route, cities_map) {
                shortest_route = new_route_and_cost.0.as_slice().to_vec();
                //println!("New Shortest: {:?}    [{}]", &shortest_route, &new_cost);
            }
            // else {
            //     println!("Local Best not short enough.");
            // }
            route = generate_random_route(city_list).as_slice().to_vec();
        }
        else {
            route = new_route_and_cost.0;
        }

        //println!("{}: {:?}    [{}]", i, route, new_route_and_cost.1);

        i = i + 1;

        elapsed_time = (Instant::now() - start_time).as_millis();
    }

    println!("\n=============== FINISHED ===============\nShortest Size: {}\nShortest Route: {:?}\nChecked: {} routes", get_cost_of_route(&shortest_route, cities_map), shortest_route, i);

}