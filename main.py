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

    def __str__(self):
        # only print immediate neighbors
        if self.rec_count == 1:
            self.rec_count = 0
            return "\'" + self.name + "\'"
        else:
            return 'name: ' + "\'" + self.name + "\'" + '\n' + 'coordinates: ' + str(self.coordinates) + '\nObstacle: ' + str(self.obstacle) \
               + '\nneighbors: ' + str(self.neighbors) + '\n'

    def __repr__(self):
        self.rec_count += 1
        return str(self)


# Vertices will be nodes of interest. That is, blanks, and Vertices (' ', 'A-Z')
class Vertex(Node):
    def __init__(self, name, x_coordinate, y_coordinate, obstacle_flag):
        super(Vertex, self).__init__(name, x_coordinate, y_coordinate, obstacle_flag)
        self.g_actual_cost = None  # the actual cost when using A*
        self.h_cost = None  # the cost given by the heuristic function
        self.previous_vertex = None


class Graph(object):
    __vertices = {}  # keep a list of __vertices with their neighbors. Key is vertex coordinates, value is the vertex
    # object

    def add_vertex(self, v):
        # check if the vertex is a Vertex object and if it's not in the __vertices dict
        if isinstance(v, Vertex) and (v.coordinates not in self.__vertices):
            self.__vertices[v.coordinates] = v
            return True  # if successful return true
        print("Vertex with same coordinates exists or the object passed is not instance of Vertex class !")
        return False  # if unsuccessful return false

    def add_edge(self, v, u):
        if isinstance(v, Vertex) and isinstance(u, Vertex) and v in self.__vertices.values() and u in self.__vertices.values():
            v.neighbors[u.coordinates] = u
            return True
        print("Either vertex may be non-existent in the graph")
        return False

    def print_graph(self):
        # v = self.__vertices[(3, 7)]
        # print(v)
        for c, v in self.__vertices.items():
             print(v)

    def get_vertices(self):
        return self.__vertices


class Map:
    def __init__(self, file_name):
        self.__map = []
        self.__file_name = file_name
        self.__read_map(self.__file_name)

    def get_file_name(self):
        return self.__file_name

    def get_map(self):
        return self.__map

    def __read_map(self, file_name):
        with open(file_name, 'r') as f:
            for line in f:
                self.__map.append([el for index, el in enumerate(line.rstrip('\n'))])


def map_to_graph(graph, text_map):
    if isinstance(graph, Graph) and isinstance(text_map, Map):
        for row_index, row in enumerate(text_map.get_map()):
            for col_index, el in enumerate(row):
                vertex = Vertex(el, row_index, col_index, False)
                graph.add_vertex(vertex)

        # create edges
        for i in range(10):
            for j in range(9):
                # add left neighbor
                if j != 0:
                    graph.add_edge(graph.get_vertices()[(i, j)], graph.get_vertices()[(i, j - 1)])
                # add right neighbor
                if j != 8:
                    graph.add_edge(graph.get_vertices()[(i, j)], graph.get_vertices()[(i, j + 1)])
                # add up neighbor
                if i != 0:
                    graph.add_edge(graph.get_vertices()[(i, j)], graph.get_vertices()[(i - 1, j)])
                # add down neighbor
                if i != 9:
                    graph.add_edge(graph.get_vertices()[(i, j)], graph.get_vertices()[(i + 1, j)])
        return True
    print("Check your paramters !")
    return False


if __name__ == "__main__":
    # represent map / puzzle as 2D array
    map_obj = Map("map.txt")
    # print(map_obj.get_map())
    v1 = Vertex("a", 2, 3, False)
    v2 = Vertex("b", 0, 0, False)
    v3 = Vertex("c", 2, 5, True)

    v1.neighbors[v2.coordinates] = v2
    v1.neighbors[v3.coordinates] = v3

    my_graph = Graph()
    map_to_graph(my_graph, map_obj)
    my_graph.print_graph()
    #print(v1)
    # print(my_graph.get_vertices())
