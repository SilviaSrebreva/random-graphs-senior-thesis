class MaxHeap:
    # a max heap keeps the node with the highest degree at the top (index 0)
    # so we can always grab the most connected node quickly 
    # (to be used in the targeted attack)
    
    # the heap is a list, but we think of it as a  binarytree:
    # the parent of index i is (i - 1) // 2
    # the children of index i are 2*i + 1 (left) and 2*i + 2 (right)
    # rule: every parent has degree >= the degree of its children

    def __init__(self):
        self.heap = []    # list of [degree, node] pairs
        self.pos_map = {} # posiution map stores where the node currently is in self.heap
        # pos_map lets us find a node in the heap without searching the whole list

    def build(self, adj_list):

        self.heap = []
        self.pos_map = {}

        for node in adj_list:
            degree = len(adj_list[node])
            self.heap.append([degree, node])
            self.pos_map[node] = len(self.heap) - 1 # the index we just appended to


        start = len(self.heap) // 2 - 1 # the last parent node, all nodes after it are leaves(posiiton wise)
        for i in range(start, -1, -1):
            self.sift_down(i)

        # we know that all positions after the middle are children
        # essentially we just went backwards through the heap
        # and made sure every parent is bigger than its children
        # this takes O(n) time, not O(n log n)

    def is_empty(self):
        return len(self.heap) == 0

    def extract_max(self):
        # removes the node with the highest degree and returns it
        if self.is_empty():
            raise IndexError("extract_max from an empty heap")

        last = len(self.heap) - 1
        # move the max to the end of the list, because removing from the end is easy with pop
        self.swap(0, last)
        degree, node = self.heap.pop()
        del self.pos_map[node]

        # whatever got moved to the top is probably too small, so fix it to go down
        if not self.is_empty():
            self.sift_down(0)

        return node, degree

    def update_key(self, node, delta):
        # changes the degree of node by delta
        # called with delta = -1 when a neighbour of node is removed
        if node not in self.pos_map:
            return # node was already removed from the heap, nothing to update

        index = self.pos_map[node]
        self.heap[index][0] = self.heap[index][0] + delta # [0] is the degree, essentially we increase the degree of the node by delta
        # the degree of the node at position index in the heap = the degree of the node at position index in the heap + delta
       
        if delta > 0:
            self.sift_up(index)   # degree went up, it might be bigger than its parent
        else:
            self.sift_down(index) # degree went down, it might be smaller than its children

    def swap(self, i, j):
        # swaps two elements and updates pos_map for both,
        # otherwise pos_map would point to the wrong places
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.pos_map[self.heap[i][1]] = i # [1] is the node label, [0] is the degree
        self.pos_map[self.heap[j][1]] = j

    def sift_up(self, i):
        # while the element is bigger than its parent, swap it upwards
        while i > 0:
            parent = (i - 1) // 2
            if self.heap[i][0] > self.heap[parent][0]:
                self.swap(i, parent)
                i = parent
            else:
                break

    def sift_down(self, i):
        # while the element is smaller than one of its children, swap it with the bigger child
        n = len(self.heap)
        while True:
            left = 2 * i + 1
            right = 2 * i + 2
            largest = i

            if left < n and self.heap[left][0] > self.heap[largest][0]:
                largest = left
            if right < n and self.heap[right][0] > self.heap[largest][0]:
                largest = right

            if largest != i:
                self.swap(i, largest)
                i = largest
            else:
                break # no child is bigger (or there are no children), we are done


if __name__ == "__main__":
    # node 0 is connected to everyone, so it should come out first
    adj_list = {0: {1, 2, 3}, 1: {0, 2}, 2: {0, 1}, 3: {0}}

    heap = MaxHeap()
    heap.build(adj_list)

    node, degree = heap.extract_max()
    print("Removed node", node, "with degree", degree) # node 0, degree 3

    # node 0 is gone, so each of its neighbours loses one degree
    for neighbour in adj_list[node]:
        heap.update_key(neighbour, -1)

    while not heap.is_empty():
        print(heap.extract_max())
