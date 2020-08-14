from room import Room
from player import Player
from world import World

import random
import copy
from ast import literal_eval
from util import Queue

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()
player = Player(world.starting_room)

# find the opposite direction
def find_opposite_direction(direction):
    if direction == "n":
        return "s"
    elif direction == "s":
        return "n"
    elif direction == "e":
        return "w"
    elif direction == "w":
        return "e"
    else:
        print("INVALID DIRECTION")
        return False

# find shortest path to a room with unexplored exits
def bfs(starting_vertex):
    """
    Return a list of room id's containing the shortest path from
    starting_vertex to a room with unexplored exits in
    breath-first order.
    """

    # Create an empty queue 
    q = Queue()
    
    # enqueue a path to the starting vertex
    q.enqueue([starting_vertex])

    # Create a Set to store visited vertices
    visited = set()

    # While the queue is not empty...
    while q.size() > 0:

        # Dequeue the first PATH
        p = q.dequeue()

        # Grab the last vertex from the path
        last = p[-1]

        # If that vertex has not been visited...
        if last.id not in visited:
            
            # check if current room has unexplored exits
            if '?' in traversal_graph[last.id].values():

                # return list of rooms if the room has unexplored exits
                return p

            # Mark current room as visited...
            visited.add(last.id)

            # Then add a path to its neighbors to the back of the queue
            for next_direction in last.get_exits():
                # shallow copy that path
                new_path = copy.copy(p)

                # append the neighbor to the end of new_path
                new_path.append(last.get_room_in_direction(next_direction))

                # add new_path to queue
                q.enqueue(new_path)

    return False

# map out the maze
def draw_traversal_graph(v, direction=None, new_room=None):

    # check if current room is already in traversal_graph
    if v.id not in traversal_graph:

        # create empty dictionary for current room
        traversal_graph[v.id] = {}

        # initialize all exits with a '?' value
        for exit in v.get_exits():
            traversal_graph[v.id][exit] = '?'

    # check if there is a direction and new_room pass into function
    if direction is not None and new_room is not None:

        # check if new_room is already in traversal_graph
        if new_room.id not in traversal_graph:

            # create empty dictionary for new_room
            traversal_graph[new_room.id] = {}

            # initialize all exits with a '?' value
            for exit in new_room.get_exits():
                traversal_graph[new_room.id][exit] = '?'

        # connect the current and new rooms with correct directions
        traversal_graph[v.id][direction] = new_room.id
        traversal_graph[new_room.id][find_opposite_direction(direction)] = v.id

# pick a random, unexplored exit
def random_step(v):

    # check for unexplored exits
    if '?' in traversal_graph[v.id].values():
        for exit in v.get_exits():
            
            # choose only unexplored exits
            if traversal_graph[v.id][exit] == '?':

                # find next room over
                new_room = v.get_room_in_direction(exit)

                # add new room to visited rooms
                player_visited_rooms.add(new_room)

                # draw traversal graph with current room, exit direction, and next room
                draw_traversal_graph(v, exit, new_room)

                # add exit direction to traversal path
                traversal_path.append(exit)

                return new_room
    
##### Main #####
traversal_path = []
player_visited_rooms = set()
traversal_graph = {}
current_room = world.starting_room

draw_traversal_graph(world.starting_room)
player_visited_rooms.add(world.starting_room)

# run simulation until player has visited all rooms
while len(player_visited_rooms) < len(room_graph):

    # check if current room has unexplored exits
    if '?' in traversal_graph[current_room.id].values():

        # take a random step into an unexplored room
        current_room = random_step(current_room)

    # otherwise, find a path back to a room with unexplored exits
    else:

        # run bfs to find shortest path back to room with unexplored exits
        backtracking_path = bfs(current_room)

        # loop through each room in backtracking_path
        for path in backtracking_path:

            # check all exits in current room
            for exit in current_room.get_exits():

                # check if the value of current room's exit direction matches next room in backtracking_path
                if traversal_graph[current_room.id][exit] == path.id:

                    # add exit direction to traversal_path
                    traversal_path.append(exit)

                    # update current room to next room in backtracking_path
                    current_room = current_room.get_room_in_direction(exit)

                    break


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
