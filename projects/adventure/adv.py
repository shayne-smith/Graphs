from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

traversal_graph = {}

def bfs(self, starting_vertex):
    """
    Return a list containing the shortest path from
    starting_vertex to vertex with unexplored rooms adjacent to it in
    breadth-first order.
    """
    # Create an empty queue 
    q = Queue()
    
    # enqueue A PATH TO the starting vertex ID
    path = [starting_vertex]
    q.enqueue(path)

    # Create a Set to store visited vertices
    visited = set()

    # While the queue is not empty...
    while q.size() > 0:

        # Dequeue the first PATH
        p = q.dequeue()

        # Grab the last_room vertex from the PATH
        last_room = p[-1]

        # If that vertex has not been visited...
        if last_room not in visited:
            
            # CHECK IF IT'S THE TARGET
            # IF SO, RETURN PATH
            if last_room == destination_vertex:
                return p

            # Mark it as visited...
            visited.add(last_room)

            # Then add A PATH TO its neighbors to the back of the queue
            for neighbor in self.get_neighbors(last_room):
                # SHALLOW COPY THE PATH
                path = copy.copy(p)

                # APPEND THE NEIGHOR TO THE BACK
                path.append(neighbor)

                q.enqueue(path)

def find_traversal_path(traversal_path):

    while len(traversal_graph) != len(room_graph):

        # find current room and its exits
        current_room = player.current_room.id
        current_room_exits = player.current_room.get_exits()

        # if not already in traversal graph, record having visited current room and create exit dictionary for it
        if traversal_graph.get(current_room) is None:
            traversal_graph[current_room] = {}

            # fill exit dictionary with possible exits for current room
            for exit in current_room_exits:
                traversal_graph[current_room][exit] = '?'

        next_direction = 'p'

        while len(current_room_exits) != 1 and :
            


        # find a random new direction to go into
        next_direction = player.current_room.get_exits()[random.randint(0, len(player.current_room.get_exits()) - 1)]
        print(next_direction)

        # move player into next room
        player.travel(next_direction)

        current_room_exits = player.current_room.get_exits()
        print(current_room_exits)
    
    print(traversal_graph)






    # 1. pick an unexplored direction from current room
    # 2. travel in that direction and log move
    # 3. loop through this until you reach a room with no unexplored paths
    # 4. use bfs to find shortest path back to an unexplored room
    # 5. convert path returned from bfs to a list of n/s/e/w directions
    # 6. add that converted path of directions to traversal path
    
find_traversal_path(traversal_path)


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
