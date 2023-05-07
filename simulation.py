from agent import *
import numpy as np
import pandas as pd
import sys
import os
import agent
from config import Config 


class Game:
    def __init__(self, num_agents=100, r_dist='uniform', num_interactions=100, p_g=2, p_b=-2, alpha_direct=0.1, alpha_indirect=0.1):
        self.run_no = 2
        self.num_agents = num_agents  # total number of agents involved in the simulation
        self.acceptance_threshold = 0  # tau_i
        self.r_dist = r_dist
        self.agents = [None for i in range(num_agents)]
        # storage of each agent's true reliability score
        self.r_arr = [0 for i in range(num_agents)]
        self.num_interactions = num_interactions
        self.p_g = p_g  # good encounter payoff
        self.p_b = p_b  # bad encounter payoff
        self.alpha_direct = alpha_direct  # decay constant. how much a player weighs its existing opinion of another player vs information it gains from encounter with said player
        # decay constant. how much a player weighs incoming opinions from other player it had a "good" encounter with
        self.alpha_indirect = alpha_indirect
        self.total_payout = 0  # total payoff accumulated
        # list of encounters, encoded as dictionaries with the following keys: ['active_id', 'passive_id', 'accepted', 'result']
        self.encounter_history = []
        # create new directory to store logs of each run of the game
        os.makedirs(os.path.dirname(f'logs/game{self.run_no}/'), exist_ok=True)
        self.game_desc_df = pd.read_csv('logs/game_descriptions.csv')
        self.log = open(
            f'logs/game{self.run_no}/game_log_{self.run_no}.txt', 'w')
        self.df = pd.DataFrame(columns=['active_id', 'passive_id', 'active_reliability',
                               'passive_reliability', 'passive_opinion', 'accepted', 'result', 'total_payout'])
        self.csv_path = f'logs/game{self.run_no}/game_log_{self.run_no}.csv'

    def initialize_agents(self):
        game_desc_df_row = {
            'run_no': self.run_no,
            'num_agents': self.num_agents,
            'r_dist': self.r_dist,
            'agent_type': 'learn_trust',
            'num_interactions': self.num_interactions,
            'p_g': self.p_g,
            'p_b': self.p_b
        }
        self.game_desc_df.loc[self.run_no] = game_desc_df_row
        self.game_desc_df.to_csv('logs/game_descriptions.csv', index=False)
        for i in range(self.num_agents):
            r_i = 0
            if (self.r_dist == 'uniform'):
                r_i = np.random.uniform(0, 1)
            elif (self.r_dist == 'normal'):
                r_i = np.random.normal(0, 1)
            elif (self.r_dist == 'bernoulli'):
                r_i = np.random.randint(0, 1)
            self.agents[i] = LearnTrustAgent(
                i, r_i, self.alpha_direct, self.alpha_indirect)
            self.r_arr[i] = r_i
        print("agent array: ", self.agents)

    def run_encounter(self, i):
        '''
        initiate an encounter between two random agents, have the passive agent run the encounter,
        and update encounter history and total payoff according to encounter outcome
        args:
            i: encounter number in the whole game
        '''
        active_id, passive_id = np.random.choice(
            range(self.num_agents), size=2, replace=False)
        active_agent = self.agents[active_id]
        passive_agent = self.agents[passive_id]
        passive_agent_opinion = passive_agent.get_opinion(active_id)
        accepted, result = passive_agent.handle_encounter(
            active_id,
            active_agent.get_reliability(),
            active_agent.get_registers(),
            self.p_g,
            self.p_b
        )
        if accepted and result:
            self.total_payout += self.p_g
        elif accepted and not result:
            self.total_payout += self.p_b
        encounter_dict = {
            'active_id': active_id,
            'passive_id': passive_id,
            'active_reliability': active_agent.get_reliability(),
            'passive_reliability': passive_agent.get_reliability(),
            'passive_opinion': passive_agent.get_registers()[active_id],
            'accepted': accepted,
            'result': result,
            'total_payout': self.total_payout
        }
        encounter_print_string = f"""ENCOUNTER {i}.
Active ID: {active_id}
Passive ID: {passive_id}
Active agent reliability: {active_agent.get_reliability()}
Passive agent reliability: {passive_agent.get_reliability()}
Passive agent's opinion of active agent: {passive_agent_opinion}
Encounter accepted: {accepted}
Encounter result: {result}
Total payout: {self.total_payout}
"""
        encounter_print_string += '\n###########################\n'
        self.log.write(encounter_print_string)
        self.encounter_history.append(encounter_dict)
        self.df.loc[len(self.df.index)] = encounter_dict
        return encounter_print_string

    def run(self):
        self.initialize_agents()
        print("TEST: ", self.agents[0].get_reliability())
        for i in range(self.num_interactions):
            print(self.run_encounter(i))
        self.df.to_csv(self.csv_path)
        return self.encounter_history


def main():
    # TODO: maybe allow user to input different reliability distributions
    # TODO: implement the other agents: play_always, play_never, and know_reliability
    '''
    args = sys.argv[1:]
    if len(args) != 2:
        print("Arg format: python simulation.py [# of agents] [reliability distribution] [# interactions]")
    num_agents = args[0]
    r_dist = args[1]
    num_interactions = args[2]
    '''

    game = Game(num_agents=Config.num_agents, r_dist=Config.r_dist,
                num_interactions=Config.num_encounters, p_g=Config.p_g, p_b=Config.p_b, 
                alpha_direct=Config.alpha_direct, alpha_indirect=Config.alpha_indirect)
    
    game.run()


if __name__ == "__main__":
    main()
