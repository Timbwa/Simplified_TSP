from os import path
from collections import deque
from time import time
import heapq

# This implementation is specific for undirected graphs
# All points in the map will be nodes in my map


class Node(object):
    rec_count = 0  # to prevent infinite recursion of neighbors

    def __init__(self, name, x_coordinate, y_coordinate, obstacle_flag=False):
        self.name = name  # possible values should only be ' ', 'A-Z', '*'
        self.coordinates = (x_coordinate, y_coordinate)  # this will uniquely identify the node
        self.obstacle = obstacle_flag  # if the name is '*' the obstacle is set to True
        self.neighbors = {}  # list of neighbors of this node
        self.set_obstacle()

    def add_neighbor(self, v):
        if isinstance(v, Node) and v not in self.neighbors:
            self.neighbors[v.coordinates] = v

    def set_obstacle(self):
        if self.name == '*':
            self.obstacle = True


class Edge(object):
    def __init__(self, to_node, w):
        self.to_node = to_node
        self.weight = w

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'To Node: {self.to_node.name} Weight: {self.weight}'

    def __eq__(self, other):
        if isinstance(other, Edge):
            return self.to_node.name == other.to_node.name  # and self.weight == other.weight
        return NotImplemented

    def __lt__(self, other):
        return self.weight < other.weight


# Vertices will be nodes of interest. That is, blanks, and Vertices (' ', 'A-Z')
class Vertex(Node):
    def __init__(self, name, x_coordinate, y_coordinate, obstacle_flag):
        super(Vertex, self).__init__(name, x_coordinate, y_coordinate, obstacle_flag)
        self.g_actual_cost = 10_000  # the actual cost when using A*, start with high value representing infinity when
        # creating new vertex
        self.h_cost = 0  # the cost given by the heuristic function
        self.previous_vertex = None
        self.total_cost = self.g_actual_cost + self.h_cost
        self.edges = []

    def __str__(self):
        # only print immediate neighbors
        if self.rec_count == 1:
            self.rec_count = 0
            return "\'" + self.name + "\'" + " " + str(self.coordinates)
        else:
            return 'name: ' + "\'" + self.name + "\'" + '\n' + 'coordinates: ' + str(
                self.coordinates) + '\nObstacle: ' + str(self.obstacle) \
                   + '\nneighbors: ' + str(self.neighbors) + '\n' + f'G score: {self.g_actual_cost}\n' \
                                                                    f'H score: {self.h_cost}\n' \
                                                                    f'F score: {self.total_cost}\n'

    def __repr__(self):
        self.rec_count += 1
        return str(self)

    # override comparator functions
    def __lt__(self, other):
        return self.total_cost < other.total_cost

    def __eq__(self, other):
        if isinstance(other, Vertex):
            return self.coordinates == other.coordinates
        return NotImplemented


class Graph(object):
    def __init__(self):
        self.__vertices = {}  # keep a list of __vertices with their neighbors.

    def add_vertex(self, v):
        # check if the vertex is a Vertex object and if it's not in the __vertices dict
        if isinstance(v, Vertex) and (v.coordinates not in self.__vertices):
            self.__vertices[v.coordinates] = v
            return True  # if successful return true
        print("Vertex with same coordinates exists or the object passed is not instance of Vertex class !")
        return False  # if unsuccessful return false

    def add_edge(self, v, u):
        if isinstance(v, Vertex) and isinstance(u, Vertex) and v in self.__vertices.values() \
                and u in self.__vertices.values():
            v.neighbors[u.coordinates] = u
            return True
        print("Either vertex may be non-existent in the graph")
        return False

    def add_edge_weight(self, v, u, w):
        if isinstance(v, Vertex) and isinstance(u, Vertex) and v in self.__vertices.values() \
                and u in self.__vertices.values():
            edge = Edge(u, w)
            edge_1 = Edge(v, w)
            v.edges.append(edge)
            u.edges.append(edge_1)
            return True
        print("Either vertex may be non-existent in the graph")
        return False

    def is_empty(self):
        return not bool(self.__vertices)

    def print_graph(self):
        for c, v in self.__vertices.items():
            print(v)

    def print_graph_edges(self):
        for c, v in self.__vertices.items():
            if isinstance(v, Vertex):
                print(f'{v.name}' + str(v.edges))

    def get_vertex(self, coordinates):
        return self.__vertices.get(coordinates)

    # needed for re-evaluation of different paths
    def reset_values(self):
        for c, vertex in self.__vertices.items():
            vertex.g_actual_cost = 10_000
            vertex.h_cost = 0
            vertex.total_cost = vertex.g_actual_cost + vertex.h_cost
            vertex.previous_vertex = None


class Map(object):
    def __init__(self, file_name):
        self.__map = []
        self.__file_name = file_name
        self.__read_map(self.__file_name)

    def get_file_name(self):
        return self.__file_name

    def get_map(self):
        return self.__map

    def print_map(self):
        for index, el in enumerate(self.__map):
            print(el)

    def __read_map(self, file_name):
        if path.exists(file_name):
            with open(file_name, 'r') as f:
                for line in f:
                    self.__map.append([el for index, el in enumerate(line.rstrip('\n'))])
        else:
            print("Error:" + ' ' + file_name + ' ' + 'doesn\'t exist')


def map_to_graph(graph, text_map):
    if isinstance(graph, Graph) and isinstance(text_map, Map):
        for row_index, row in enumerate(text_map.get_map()):
            for col_index, el in enumerate(row):
                vertex = Vertex(el, row_index, col_index, False)
                graph.add_vertex(vertex)

        # create edges with right-left-down-up order for tie-breaking
        for i in range(10):
            for j in range(9):
                # add left neighbor
                if j != 0:
                    graph.add_edge(graph.get_vertex((i, j)), graph.get_vertex((i, j - 1)))
                # add right neighbor
                if j != 8:
                    graph.add_edge(graph.get_vertex((i, j)), graph.get_vertex((i, j + 1)))
                # add up neighbor
                if i != 0:
                    graph.add_edge(graph.get_vertex((i, j)), graph.get_vertex((i - 1, j)))
                # add down neighbor
                if i != 9:
                    graph.add_edge(graph.get_vertex((i, j)), graph.get_vertex((i + 1, j)))

        return True
    print("Check your parameters !")
    return False


def display_menu():
    msg = "\nWelcome, pick an option:"
    prompts = {1: "Construct a Shortest Path Graph",
               2: "Solve TSP using BFS and UCS",
               3: "Exit"}
    print(msg)
    for key, value in enumerate(prompts):
        print(str(value) + '. ' + prompts[value])
    try:
        option = int(input("Choice:"))
        return option
    except ValueError as ve:
        print('Please enter a number from 1-3')
    return 0


def manhattan_heuristic(start_vertex, end_vertex):
    if isinstance(start_vertex, Vertex) and isinstance(end_vertex, Vertex):
        man_dist = abs(end_vertex.coordinates[0] - start_vertex.coordinates[0]) + abs(end_vertex.coordinates[0] -
                                                                                      start_vertex.coordinates[0])
        return man_dist


def reconstruct_path(start_vertex, goal_vertex):
    total_path = []
    if isinstance(start_vertex, Vertex) and isinstance(goal_vertex, Vertex):
        # while a previous vertex exists
        total_path.append(goal_vertex)
        current_vertex = goal_vertex.previous_vertex
        while current_vertex.previous_vertex:
            total_path.insert(0, current_vertex)
            current_vertex = current_vertex.previous_vertex
        total_path.insert(0, current_vertex)
        return total_path


def solve_a_star(graph, start_vertex, goal_vertex, path_lists):
    if isinstance(graph, Graph) and isinstance(start_vertex, Vertex) and isinstance(goal_vertex, Vertex):
        closed_set = []  # visited vertices
        fringe = []

        # initialise start vertex parameters
        start_vertex.g_actual_cost = 0  # start vertex actual cost
        start_vertex.h_cost = manhattan_heuristic(start_vertex, goal_vertex)
        start_vertex.total_cost = start_vertex.g_actual_cost + start_vertex.h_cost

        # add start vertex to min heap priority queue
        heapq.heappush(fringe, start_vertex)
        while len(fringe):
            # get vertex with lowest total f_score(g + h)
            heapq.heapify(fringe)
            current_vertex = heapq.heappop(fringe)
            closed_set.append(current_vertex)
            # print("current vertex: ")
            # print(current_vertex)
            if isinstance(current_vertex, Vertex):
                if current_vertex.coordinates == goal_vertex.coordinates:  # if current vertex is goal vertex return
                    print(f'{start_vertex.name}, {goal_vertex.name}, {goal_vertex.g_actual_cost}')
                    path_lists.append([start_vertex.name, goal_vertex.name, goal_vertex.g_actual_cost])
                    return goal_vertex.g_actual_cost

                for key, neighbor in current_vertex.neighbors.items():
                    # tentative g cost of neighbor. Every distance from current ot neighbor is one
                    if neighbor not in closed_set:
                        temp_g_cost = current_vertex.g_actual_cost + 1
                        if not neighbor.obstacle and temp_g_cost < neighbor.g_actual_cost:
                            # best path at the moment

                            # update neighbor parameters
                            neighbor.previous_vertex = current_vertex
                            neighbor.g_actual_cost = temp_g_cost
                            neighbor.h_cost = manhattan_heuristic(neighbor, goal_vertex)
                            neighbor.total_cost = neighbor.h_cost + neighbor.g_actual_cost

                            # avoid adding visited nodes in fringe
                            if neighbor not in fringe:
                                heapq.heappush(fringe, neighbor)

        return "no solution"


def solve_tsp_bfs(graph, start_vertex, goal_vertex, path_list):
    # reset graph values
    graph.reset_values()
    # weights in bfs are not considered
    # arbitrary queue for inserting nodes
    queue = deque()
    visited_nodes = []
    total_cost = 0

    # start with start_vertex. Add edges to queue
    if isinstance(start_vertex, Vertex) and isinstance(goal_vertex, Vertex):
        path_list.append(start_vertex.name)
        for index, edge in enumerate(start_vertex.edges):
            queue.append(edge)
        visited_nodes.append(start_vertex)

        # while the queue is not empty
        while queue:
            edge = queue.popleft()
            visited_nodes.append(edge.to_node)
            path_list.append(edge.to_node.name)
            if (edge.to_node == goal_vertex and bool(total_cost)) or not queue:
                # may add weight of goal
                total_cost += edge.weight + edge.to_node.edges[0].weight
                path_list.append(start_vertex.name)
                return total_cost
            # add all the nodes in the edges in of vertex to queue if it's not visited
            q_index = 0
            for index, e in enumerate(edge.to_node.edges):
                if e not in queue and e.to_node not in visited_nodes:
                    queue.append(e)
                    visited_nodes.append(e.to_node)
                if e in queue:
                    queue[q_index].weight = e.weight
                    q_index = q_index + 1

            total_cost += edge.weight
        return total_cost, path_list


def solve_tsp_ucs(graph, start_vertex, goal_vertex, path_list):
    # reset graph values
    graph.reset_values()
    # create min heap for storing edges according to least weight
    queue = []
    visited_nodes = []
    total_cost = 0

    # start with start vertex. Add edges to queue
    if isinstance(start_vertex, Vertex) and isinstance(goal_vertex, Vertex):
        path_list.append(start_vertex.name)
        for index, edge in enumerate(start_vertex.edges):
            heapq.heappush(queue, edge)
        heapq.heapify(queue)
        visited_nodes.append(start_vertex)

        # while the queue isn't empty
        while queue:
            edge = heapq.heappop(queue)
            visited_nodes.append(edge.to_node)
            path_list.append(edge.to_node.name)

            if (edge.to_node == goal_vertex and bool(total_cost)) or not queue:
                # may add weight of goal
                total_cost += edge.weight + edge.to_node.edges[0].weight
                path_list.append(start_vertex.name)
                return total_cost

            # add all the neighboring nodes according to their weights
            queue = []
            for index, ed in enumerate(edge.to_node.edges):
                if ed.to_node not in visited_nodes:
                    heapq.heappush(queue, ed)
            heapq.heapify(queue)
            total_cost += edge.weight


if __name__ == "__main__":
    # Error messages
    graph_error_msg = "Shortest Path Graph isn't constructed yet...\n"
    prompt_error_msg = "Choose a number on the list\n"

    # print menu
    choice = display_menu()

    # create map from file
    map_obj = Map("map.txt")

    # create graph representative of the whole map/puzzle
    map_graph = Graph()
    map_ucs_graph = Graph()

    # create graph that will contain edge weights
    tsp_bfs_graph = Graph()
    tsp_ucs_graph = Graph()

    path_lists = []

    # Vertices A, B, C, D
    # A is at (8, 2)
    # B is at (1, 3)
    # C is at (3, 6)
    # D is at (8, 6)
    vertices = [(8, 2), (1, 3), (3, 6), (8, 6)]

    # keep displaying menu waiting for input
    while choice != 3:
        if choice == 1:

            # create fully connected graph from input map
            if map_graph.is_empty() or map_ucs_graph.is_empty():
                map_to_graph(map_graph, map_obj)
                map_to_graph(map_ucs_graph, map_obj)

                # add relevant vertices to graph
                for v in range(len(vertices)):
                    temp_vertex = map_graph.get_vertex(vertices[v])
                    temp_ucs_vertex = map_ucs_graph.get_vertex(vertices[v])
                    tsp_bfs_graph.add_vertex(temp_vertex)
                    tsp_ucs_graph.add_vertex(temp_ucs_vertex)
                # print(tsp_graph.print_graph())

                # for each vertex A, B, C, D find shortest path and add edge
                for i in range(len(vertices)):
                    this_vertex = map_graph.get_vertex(vertices[i])
                    this_ucs_vertex = map_ucs_graph.get_vertex(vertices[i])
                    temp_list = vertices[i + 1:]
                    if not temp_list:
                        break
                    for j in range(len(temp_list)):
                        to_vertex = map_graph.get_vertex(temp_list[j])
                        to_ucs_vertex = map_ucs_graph.get_vertex(temp_list[j])
                        weight = solve_a_star(map_graph, this_vertex, to_vertex, path_lists)
                        tsp_bfs_graph.add_edge_weight(this_vertex, to_vertex, weight)
                        tsp_ucs_graph.add_edge_weight(this_ucs_vertex, to_ucs_vertex, weight)
                        map_graph.reset_values()
                        map_ucs_graph.reset_values()
            else:
                for path in path_lists:
                    print(f'{path[0]}, {path[1]}, {path[2]}')

        elif choice == 2:
            # TO-DO
            if map_graph.is_empty():
                print("Error: " + graph_error_msg)
                choice = display_menu()
                continue
            # solve using BFS
            bfs_path = []
            bfs_time0 = time()
            bfs_cost = solve_tsp_bfs(tsp_bfs_graph, tsp_bfs_graph.get_vertex((8, 2)),
                                     tsp_bfs_graph.get_vertex((8, 2)), bfs_path)
            bfs_time1 = time()
            bfs_tot_time = round((bfs_time1 - bfs_time0), 7)

            # solve using UCS
            ucs_path = []
            ucs_time0 = time()
            ucs_cost = solve_tsp_ucs(tsp_ucs_graph, tsp_ucs_graph.get_vertex((8, 2)),
                                     tsp_ucs_graph.get_vertex((8, 2)), ucs_path)
            ucs_time1 = time()
            ucs_tot_time = round((ucs_time1 - ucs_time0), 7)
            # print results and statistics
            print(f'\nAlgorithm used: BFS')
            print(*bfs_path, sep='-')
            print(f'Total Tour Cost {bfs_cost}\n')

            print(f'\nAlgorithm used: UCS')
            print(*ucs_path, sep='-')
            print(f'Total Tour Cost {ucs_cost}\n')
            print(f'Statistics:\n'
                  f'\t\t\tNodes\t\t\t\tTime\t\t\tCost\n'
                  f'BFS\t{bfs_path}\t{bfs_tot_time} sec\t{bfs_cost}\n'
                  f'UCS\t{ucs_path}\t{ucs_tot_time} sec\t{bfs_cost}')

        elif choice == 3:
            print("Bye...")
            break
        else:
            print("Error: " + prompt_error_msg)
        choice = display_menu()
