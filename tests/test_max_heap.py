import random

from max_heap import MaxHeap
from BA_generator import generate_ba


def check_heap(heap):
    # helper: checks the two rules of the heap
    for i in range(len(heap.heap)):
        # rule 1: every parent has degree >= its children
        left = 2 * i + 1
        right = 2 * i + 2
        if left < len(heap.heap):
            assert heap.heap[i][0] >= heap.heap[left][0]
        if right < len(heap.heap):
            assert heap.heap[i][0] >= heap.heap[right][0]

        # rule 2: pos_map points at the right index for every node
        node = heap.heap[i][1]
        assert heap.pos_map[node] == i

    assert len(heap.pos_map) == len(heap.heap)


# PRIMARY

def test_extract_in_right_order():
    # degrees: node 0 -> 3, node 1 -> 2, node 2 -> 2, node 3 -> 1
    adj_list = {0: {1, 2, 3}, 1: {0, 2}, 2: {0, 1}, 3: {0}}
    heap = MaxHeap()
    heap.build(adj_list)

    degrees = []
    while not heap.is_empty():
        node, degree = heap.extract_max()
        degrees.append(degree)

    assert degrees == [3, 2, 2, 1] # biggest first


def test_update_key():
    adj_list = {0: {1, 2, 3}, 1: {0, 2}, 2: {0, 1}, 3: {0}}
    heap = MaxHeap()
    heap.build(adj_list)

    heap.update_key(3, 5) # node 3 goes from degree 1 to 6, so it should be on top now
    assert heap.extract_max() == (3, 6) # essentially we test sift_up

    heap.update_key(0, -2) # node 0 goes from degree 3 to 1, so it is not on top anymore
    node, degree = heap.extract_max() #essentially we test sift_down
    assert node != 0
    assert degree == 2


def test_empty_heap():
    heap = MaxHeap()
    heap.build({})
    assert heap.is_empty()


# SECONDARY

def test_extract_max_on_empty_heap_raises():
    heap = MaxHeap()
    try:
        heap.extract_max()
        assert False, "should have raised IndexError"
    except IndexError:
        pass


def test_heap_rules_after_many_operations():
    random.seed(1)
    adj_list, edge_list, history = generate_ba(200, 2)
    heap = MaxHeap()
    heap.build(adj_list)
    check_heap(heap)

    # same steps as the targeted attack: take the max, its neighbours lose one degree
    for step in range(100):
        node, degree = heap.extract_max()
        for neighbour in adj_list[node]:
            heap.update_key(neighbour, -1)
        check_heap(heap)
