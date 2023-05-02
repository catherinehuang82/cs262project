from agent import *
import numpy as np
import sys
import agent

class Game:
    def __init__(self, num_agents=100, r_dist='uniform', num_interactions=100):
        self.num_agents = num_agents # total number of agents involved in the simulation
        self.acceptance_threshold = 0 # tau_i
        self.r_dist = r_dist
        self.agents = [None for i in range(num_agents)]
        self.r_arr = [0 for i in range(num_agents)] # storage of each agent's true reliability score
        self.num_interactions = num_interactions
        self.p_g = 2 # good encounter payoff
        self.p_b = -2 # bad encounter payoff
        self.alpha_direct = 0.1 # decay constant. how much a player weighs its existing opinion of another player vs information it gains from encounter with said player
        self.alpha_indirect = 0.1 # decay constant. how much a player weighs incoming opinions from other player it had a "good" encounter with
        self.total_payout = 0 # total payoff accumulated
        self.encounter_history = [] # list of dictionaries, each with the following keys: ['active_id', 'passive_id', 'accepted', 'result']
    def initialize_agents(self):
        for i in range(self.num_agents):
            r_i = 0
            if (self.r_dist == 'uniform'):
                r_i = np.random.uniform(0, 1)
            elif (self.r_dist == 'normal'):
                r_i = np.random.normal(0, 1)
            elif (self.r_dist == 'bernoulli'):
                r_i = np.random.randint(0,1)
            self.agents[i] = Agent(i,r_i)
            self.r_arr[i] = r_i
        print("agent array: ", self.agents)
    def run_encounter(self):
        '''
        initiate an encounter between two random agents, have the passive agent run the encounter,
        and update encounter history and total payoff according to encounter outcome
        '''
        active_id, passive_id = np.random.choice(range(100), size=2, replace=False)
        active_agent = self.agents[active_id]
        passive_agent = self.agents[passive_id]
        accepted, result = passive_agent.handle_encounter(active_id, active_agent.get_reliability(), active_agent.get_registers(), self.p_g, self.p_b)
        encounter_dict = {
            'active_id': active_id,
            'passive_id': passive_id,
            'accepted': accepted,
            'result': result
        }
        if accepted and result:
            self.total_payout += self.p_g
        elif accepted and not result:
            self.total_payout += self.p_b
        self.encounter_history.append(encounter_dict)
        return self.total_payout
    def run(self):
        self.initialize_agents()
        print("TEST: ", self.agents[0].get_reliability())
        for i in range(self.num_interactions):
            print(self.run_encounter())
    
        
def main():
    # args: num agents
    # thought: maybe allow user to input different reliability distributions

    '''
    args = sys.argv[1:]
    if len(args) != 2:
        print("Arg format: python simulation.py [# of agents] [reliability distribution] [# interactions]")
    num_agents = args[0]
    r_dist = args[1]
    num_interactions = args[2]
    '''

    num_agents = 100
    r_dist = 'uniform'
    num_interactions = 100

    game = Game(num_agents=num_agents, r_dist=r_dist, num_interactions=num_interactions)
    game.run()

if __name__ == "__main__":
    main()