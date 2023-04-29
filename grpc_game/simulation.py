from agent import *
import numpy as np

def main():
    # args: num agents
    # thought: maybe allow user to input different reliability distributions
    args = sys.argv[1:]
    if len(args) != 2:
        print("Arg format: python simulation.py [# of agents] [reliability distribution] [# interactions]")
    num_agents = args[0]
    r_dist = args[1]
    num_interactions = args[2]

    # instantiate agents
    # reliability distributions: 
    #   uniform
    #   normal
    #   binary: everyone either gets 1 or 0 w/ equal probability (maybe make this variable)
    agents = []
    for i in range(num_agents):
        if (r_dist == "uniform"):
            agents.append(Agent(np.random.uniform(0, 1)))
        else if (r_dist == "normal"):
            agents.append(Agent(np.random.normal(0, 1)))
        else if (r_dist == "binary"):
            agents.append(Agent(randint(0,1)))
        else:
            agents.append(Agent(0))

    # keep track of stats
    rewards = [0 for i in range(num_agents)]

    # begin interactions
    for i in range(num_interactions):
        continue

    # output simulation statistics
    print("Total community reward: " + sum(rewards))
    print("Individual rewards: " + rewards)
    print("Average reward: " + sum(rewards)/len(rewards))
    print("Std dev of rewards: " + np.std(rewards))