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
    
def earliest_ancestor(ancestors, starting_vertex):
    """Find the earliest ancestor for a given person"""

    # Represent a graph as a dictionary of vertices mapping labels to edges
    vertices = {}

    # Build graph
    for a in ancestors:
        add_vertex(vertices, a[0])
        add_vertex(vertices, a[1])
        add_edge(vertices, a[1], a[0])

    # Create an empty stack to store all the different paths
    s = Stack()
    
    # add A PATH TO the starting vertex ID
    path = [starting_vertex]
    s.push(path)

    # Create a set to store visited vertices
    visited = set()

    # Create a list to store the path to earliest ancestor
    longest_path = []

    # While the stack is not empty...
    while s.size() > 0:

        # Remove the last path from stack
        p = s.pop()

        # Grab the last vertex from the path
        last = p[-1]

        # If two ancestors are from same generation, set longest_path to ancestor with smaller value
        if len(longest_path) == len(p) and last < longest_path[-1]:
            longest_path = p

        # Find longest path
        if len(longest_path) < len(p):
            longest_path = p

        # If that vertex has not been visited...
        if last not in visited:

            # Mark it as visited...
            visited.add(last)

            # Then add A PATH TO its neighbors to the top of the stack
            for neighbor in get_neighbors(vertices, last):
                # Shallow copy the path
                path = copy.copy(p)

                # Append the neighbor to the back
                path.append(neighbor)
                
                # Add updated path to stack
                s.push(path)
    
    # return -1 if no ancestors were found
    if len(longest_path) == 1:
        return -1

    # otherwise, return the earliest ancestor
    else:
        return longest_path[-1]


test_ancestors = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7), (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)]

print(earliest_ancestor(test_ancestors, 1)) # 10
print(earliest_ancestor(test_ancestors, 6)) # 10
print(earliest_ancestor(test_ancestors, 2)) # -1