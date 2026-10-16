from biased_coin import biased_coin_flip

# SIR model: every node is
# "S" susceptible - healthy, can catch the disease
# "I" infected - sick, can pass it to neighbours
# "R" recovered - can't get sick again and can't pass it on

def run_sir(adj_list, beta, gamma, initial_infected, max_steps):
    # adj_list - the one returned from the ER/BA generators; node: set of neighbours
    # beta - chance an infected node infects one susceptible neighbour in one step
    # gamma - chance an infected node recovers in one step
    # initial_infected - list of nodes that are sick at the start
    # max_steps - stop after this many steps even if the epidemic isn't over, so it doesnt run forever

    states = {node: "S" for node in adj_list} # everyone starts healthy; states i s a dictionary node: state
    for node in initial_infected:
        states[node] = "I"

    results = []
    record(results, states) # counts before anything happens (step 0)

    for step in range(1, max_steps + 1):

        if "I" not in states.values():
            break # nobody is infected, nothing can change anymore. simulation ends

        # we write the changes into a copy, so a node infected in this step
        # can't infect others in the same step
        next_states = states.copy()

        for node in adj_list:
            if states[node] == "I":

                # try to infect each susceptible neighbour
                for neighbour in adj_list[node]:
                    if states[neighbour] == "S":
                        if biased_coin_flip(beta):
                            next_states[neighbour] = "I"

                # try to recover
                if biased_coin_flip(gamma):
                    next_states[node] = "R"

        states = next_states
        record(results, states)

    return results
    # list of dicts, one per step, each with the fractions of S, I and R nodes out of n

def record(results, states):
    # counts how many nodes are in each state and stores them as fractions of n
    n = len(states)
    S = list(states.values()).count("S") / n
    I = list(states.values()).count("I") / n
    R = list(states.values()).count("R") / n
    results.append({"S": S, "I": I, "R": R})


if __name__ == "__main__":
    from BA_generator import generate_ba

    adj_list, edge_list, history = generate_ba(1000, 2)
    results = run_sir(adj_list, beta=0.05, gamma=0.1, initial_infected=[0], max_steps=200)

    for step, counts in enumerate(results):
        print(step, counts)
