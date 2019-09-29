import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Collections;
import java.util.LinkedHashSet;
import java.io.FileReader;
import java.io.IOException;
import java.io.BufferedReader;

class Main {
    public static void main(String[] args) throws IOException {

        ArrayList<List<Double>> cityMap = getCityMapFromFile("ulysses16(3).csv");

        getShortestRoute(cityMap);
    }

    private static ArrayList<List<Double>> getCityMapFromFile(String filename) throws IOException {
        ArrayList<List<Double>> output = new ArrayList<List<Double>>();
        String row;
        BufferedReader csvReader = new BufferedReader(new FileReader(filename));
        while ((row = csvReader.readLine()) != null) {
            String[] data = row.split(",");
            Double[] coords = {Double.parseDouble(data[0]), null};
            coords[1] = Double.parseDouble(data[1]);
            output.add(Arrays.asList(coords));
        }
        csvReader.close();
        return output;
    }

    private static ArrayList<Integer> getRandomRoutePermutation(ArrayList<List<Double>> cityMap) {
        int i = 0;
        ArrayList<Integer> cityList = new ArrayList<Integer>();
        for (List<Double> city : cityMap) {
            cityList.add(i);
            i++;
        }

        Collections.shuffle(cityList);
        return cityList;
    }

    private static Double getRouteSize(ArrayList<Integer> route, ArrayList<List<Double>> cityMap) {
        Double total = (double) 0;
        int i = 0;

        while (i < route.size() - 1) {
            total += getDistanceBetweenCities(route.get(i), route.get(i + 1), cityMap);
            i++;
        }
        total += getDistanceBetweenCities(route.get(i), route.get(0), cityMap);

        return total;
    }

    private static Double getDistanceBetweenCities(int city1, int city2, ArrayList<List<Double>> cityMap) {
        return (Double) Math.sqrt(Math.pow((cityMap.get(city1).get(1) - cityMap.get(city1).get(0)), 2) +  Math.pow((cityMap.get(city2).get(1) - cityMap.get(city2).get(0)), 2));
    }

    private static void getShortestRoute(ArrayList<List<Double>> cityMap) {
        LinkedHashSet<ArrayList<Integer>> routes = new LinkedHashSet<ArrayList<Integer>>();

        for (int i = 0; i < 362880;) {
            ArrayList<Integer> route = getRandomRoutePermutation(cityMap); //= new ArrayList<Integer>(Arrays.asList(7, 4, 5, 8, 6, 0, 2, 3, 1));// = getRandomRoutePermutation(cityMap);
            int oldSize = routes.size();
            routes.add(route);
            int newSize = routes.size();
            if (oldSize != newSize) {
                i++;
            }
        }
        
        LinkedHashSet<ArrayList<Integer>> shortestRoute = new LinkedHashSet<ArrayList<Integer>>();
        Double shortestSize = (double) 1000;
        int i = 1;
        for (ArrayList<Integer> route : routes) {
            Double newSize = getRouteSize(route, cityMap);

            if (newSize < shortestSize) {
                shortestSize = newSize;
                shortestRoute.clear();
                shortestRoute.add(route);
            }

            if (newSize.equals(shortestSize)) {
                shortestRoute.add(route);
            }

            System.out.println(i + ": " + newSize + " - " + route + "       (" + shortestSize + ")");

            i++;
        }

        System.out.println("\n======= FINISHED =======");
        System.out.println("Shortest Size: " + shortestSize + "\nShortest Routes:");
        for (ArrayList<Integer> route : shortestRoute) {
            System.out.println(route);
        }
        
    }
}