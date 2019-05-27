import json

INFINITY = float("inf")

vertices_names = dict()  # dict for the Vertex-Names
vertices_count = int  # Number of Vertices
transitions = [[]]  # Transition-Matrix
shortest_paths = list()  #


def load_graph(path, directed_graph=False):
    global transitions
    global vertices_count

    graph = json.load(open(path, "r"))

    vertices_count = len(graph['nodes'])  # Number of Vertices
    transitions = [[INFINITY] * vertices_count for i in range(vertices_count)]

    # foreach Vertex
    for i in range(vertices_count):
        vertices_names.update({i: graph['nodes'][i]['label']})  # Add Name to dict
        shortest_paths.append([i, i, INFINITY])  # Adds a Path for planet i from plant i with distance infinity

    for i in range(len(graph['edges'])):
        x, y = graph['edges'][i]['source'], graph['edges'][i]['target']
        distance = graph['edges'][i]['cost']
        transitions[x][y] = distance
        if not directed_graph:
            transitions[y][x] = distance


def find_shortest_path(start: int, end: int):
    to_check = [(start, 0)]  # The Start-Node and the total distance

    while len(to_check) > 0:
        to_check.sort(key=lambda x: x[1])  # sort the list for distance
        current = to_check.pop(0)
        current_vertex, current_distance = current[0], current[1]
        trans = transitions[current_vertex]

        for i in range(vertices_count):
            if trans[i] < INFINITY:
                total_distance = current_distance + trans[i]
                if shortest_paths[i][2] > total_distance:
                    shortest_paths[i] = (i, current_vertex, total_distance)
                    to_check.append((i, total_distance))

        for x in to_check:
            if x[1] > shortest_paths[end][2]:
                to_check.remove(x)

    # Print the Solution
    current_vertex = end
    path = vertices_names[end]
    while current_vertex != start:
        current_vertex = shortest_paths[current_vertex][1]
        path = vertices_names[current_vertex] + " -> " + path

    print(path)
    print("Distance: " + str(shortest_paths[end][2]))


load_graph(path="generatedGraph.json")  # load graph from json file
find_shortest_path(start=18, end=246)  # 18=Erde & 246=b3-r7-r4
