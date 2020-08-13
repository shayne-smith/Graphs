import random

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

    def __str__(self):
        return f"{self.queue}"

class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.reset()

    def reset(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.reset()

        # Add users
        for i in range(num_users):
            self.add_user(f"User {i}")

        # Create friendships
        possible_friendships = []

        for user_id in self.users:
            for friend_id in range(user_id + 1, self.last_id + 1):
                possible_friendships.append((user_id, friend_id))

        random.shuffle(possible_friendships)

        for i in range(num_users * avg_friendships // 2):
            friendships = possible_friendships[i]
            self.add_friendship(friendships[0], friendships[1])

    def get_neighbors(user_id):
        """
        Get all friends (edges) of a user.
        """
        return self.friendships[user_id]

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
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

            # Grab the last vertex from the PATH
            last = p[-1]

            # If that vertex has not been visited...
            if last not in visited:
                
                # CHECK IF IT'S THE TARGET
                # IF SO, RETURN PATH
                if last == destination_vertex:
                    return p

                # Mark it as visited...
                visited.add(last)

                # Then add A PATH TO its neighbors to the back of the queue
                for neighbor in self.get_neighbors(last):
                    # SHALLOW COPY THE PATH
                    path = copy.copy(p)

                    # APPEND THE NEIGHOR TO THE BACK
                    path.append(neighbor)

                    q.enqueue(path)

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """

        # store friend network
        # user 1 friends --- 1: {2, 5, 7}
        # connections = sg.get_all_social_paths(1)
        # friends_network = {
        #   1: [1],
        #   2: [1, 2],
        #   5: [1, 5],
        #   7: [1, 7],
        #   4: [1, 5, 4],
        #   6: [1, 7, 6],
        #   8: [1, 5, 4, 8],
        #   9: [1, 7, 6, 9]
        # }
        #

        friend_network = {}

        # store friends in queue for bfs
        q = Queue()

        # enqueue A PATH TO the starting vertex ID
        path = [user_id]
        q.enqueue(path)

        # Create a Set to store visited vertices
        visited = set()

        # While the queue is not empty...
        while q.size() > 0:

            # Dequeue the first PATH
            p = q.dequeue()

            # Grab the last vertex from the PATH
            last = p[-1]

            # If that vertex has not been visited...
            if last not in visited:

                # Mark it as visited...
                visited.add(last)

        return friend_network


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    print(connections)
