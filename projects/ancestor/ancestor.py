from util import Stack, Queue
import copy

def add_vertex(vertices, vertex_id):
    """
    Add a vertex to the graph.
    """
    if vertices.get(vertex_id) is None:
        vertices[vertex_id] = set()

def add_edge(vertices, v1, v2):
    """
    Add a directed edge to the graph.
    """
    if v1 in vertices and v2 in vertices:
        vertices[v1].add(v2)
    else:
        raise IndexError("nonexistent vertex")

def get_neighbors(vertices, vertex_id):
    """
    Get all neighbors (edges) of a vertex.
    """
    return vertices[vertex_id]
    
# test_ancestors = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7), (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)]
def earliest_ancestor(ancestors, starting_vertex):
    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    vertices = {}

    # Build graph
    for a in ancestors:
        add_vertex(vertices, a[0])
        add_vertex(vertices, a[1])
        add_edge(vertices, a[1], a[0])
        print(vertices)
    # {1: {10}, 3: {1, 2}, 2: set(), 6: {3, 5}, 5: {4}, 7: {5}, 4: set(), 8: {11, 4}, 9: {8}, 11: set(), 10: set()}

    # Create an empty stack to store all the different paths
    s = Stack()
    
    # add A PATH TO the starting vertex ID
    path = [starting_vertex]
    s.push(path)

    # Create a Set to store visited vertices
    visited = set()

    longest_path = []

    # While the stack is not empty...
    while s.size() > 0:

        # Remove the last PATH from stack
        p = s.pop()

        if len(longest_path) < len(p):
            print(p)
            longest_path = p

        # Grab the last vertex from the PATH
        last = p[-1]

        # If that vertex has not been visited...
        if last not in visited:

            # Mark it as visited...
            visited.add(last)

            # Then add A PATH TO its neighbors to the top of the stack
            for neighbor in get_neighbors(vertices, last):
                # SHALLOW COPY THE PATH
                path = copy.copy(p)

                # APPEND THE NEIGHOR TO THE BACK
                path.append(neighbor)

                s.push(path)
    
    if len(longest_path) == 0:
        return -1
    else:
        return longest_path[-1]


test_ancestors = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7), (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)]

print(earliest_ancestor(test_ancestors, 1)) # 10
print(earliest_ancestor(test_ancestors, 6)) # 10