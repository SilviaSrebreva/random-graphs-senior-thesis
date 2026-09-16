"""
Biased coin simulation.
Will be used in graph generation.
"""
import random #am i allowed 

def biased_coin_flip(bias):
    random_number = random.random() 
    # generates a number betweeen 1 and 0

    if random_number < bias:
        return True
    else:
        return False
    
