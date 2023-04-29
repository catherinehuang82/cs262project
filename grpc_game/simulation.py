from agent import *

def main():
    # args: num agents
    # thought: maybe allow user to input different reliability distributions
    args = sys.argv[1:]
    if len(args) != 1:
        print("Arg format: python simulation.py [# of agents] [reliability distribution]")
    num_agents = args[0]
    r_dist = args[1]

    # instantiate agents
    # reliability distributions: uniform, normal, some extreme cases, etc.
    agents = []
    for i in range(num_agents):
        if (r_dist == "uniform"):
            agents.append(Agent(np.random.uniform(0, 1)))
        else if (r_dist == "normal"):
            agends.append(Agent(np.random.normal(0, 1)))
        else:
            agents.append(Agent(0))

    # begin interactions

    # output simulation statistics