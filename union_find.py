class UnionFind:
    # union find keeps track of which nodes are in the same connected component
    # every component is stored as a tree, and the root of the tree is the "name" of the component
    # https://www.youtube.com/watch?v=ayW5B2W9hfo 

    def __init__(self, n):
        self.n = n
        self.parent = list(range(n)) # [0, 1, 2, ..., n-1], every node starts as its own root
        self.rank = [0] * n          # [0, 0, 0, ..., 0], rank is how tall the tree is

    def find(self, x):
        # follows parent pointers up until we reach the root
        # a node is the root when it is its own parent
        # recursion 
        if self.parent[x] != x:
            # path compression: on the way back, point x straight at the root
            # so next time we look for x it takes one step instead of many
            # studied this in class 
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        # joins the component of x and the component of y into one
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return # already in the same component, nothing to do

        # union by rank: hang the shorter tree under the taller one
        # this keeps the trees short, so find stays fast
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            # equal rank, pick either one as the new root
            # the tree gets one level taller, so its rank goes up by one
            self.parent[root_y] = root_x
            self.rank[root_x] = self.rank[root_x] + 1

    def rebuild(self, n, edge_list):
        # called after every node removal in the simulation
        # returns the size of the largest connected component
        # why rebuild from cratch? 
        # because union find merges components but doesn't split them

        # step 1: reset so every node is on its own again
        self.n = n
        self.parent = list(range(n))
        self.rank = [0] * n

        # step 2: join the two ends of every edge that is still there
        for u, v in edge_list:
            self.union(u, v)

        # step 3: count how many nodes share each root
        # each root is one component, so this gives the size of every component
        component_size = {} # in this dict we map roots to their component sizes
        for node in range(n): 
            root = self.find(node) # tells us the parent, the root of the component
            if root in component_size: # if the root is already in the dict, increase it with 1
                component_size[root] = component_size[root] + 1
            else:
                component_size[root] = 1

        # step 4: return the biggest one
        if not component_size:
            return 0 # if graph with no nodes
        return max(component_size.values())


if __name__ == "__main__":
    # small example: two components {0, 1, 2} and {3, 4}, and node 5 on its own
    n = 6
    edge_list = [(0, 1), (1, 2), (3, 4)]

    uf = UnionFind(n)
    print("Largest component:", uf.rebuild(n, edge_list)) # should be 3
    print("Are 0 and 2 connected?", uf.find(0) == uf.find(2)) # True
    print("Are 0 and 3 connected?", uf.find(0) == uf.find(3)) # False
