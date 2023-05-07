from agent import *
import numpy as np
import pandas as pd
import sys
import os
import agent


class Game:
    def __init__(self, num_agents=100, r_dist='uniform', num_interactions=100):
        self.run_no = 0
        self.agents_per_trial = 20
        self.num_agents = num_agents  # total number of agents involved in the simulation
        self.acceptance_threshold = 0  # tau_i
        self.r_dist = r_dist
        self.agents = [None for i in range(num_agents)]
        # storage of each agent's true reliability score
        self.r_arr = [0 for i in range(num_agents)]
        self.num_interactions = num_interactions
        self.p_g = 2  # good encounter payoff
        self.p_b = -2  # bad encounter payoff
        self.alpha_direct = 0.1  # decay constant. how much a player weighs its existing opinion of another player vs information it gains from encounter with said player
        # decay constant. how much a player weighs incoming opinions from other player it had a "good" encounter with
        self.alpha_indirect = 0.1
        self.total_payout = 0  # total payoff accumulated
        # list of dictionaries, each with the following keys: ['active_id', 'passive_id', 'accepted', 'result']
        self.encounter_history = []
        # create new directory to store logs of each run of the game
        os.makedirs(os.path.dirname(f'logs_failures/game{self.run_no}/'), exist_ok=True)
        self.game_desc_df = pd.read_csv('logs_failures/game_descriptions.csv')
        self.log = open(
            f'logs_failures/game{self.run_no}/game_log_{self.run_no}.txt', 'w')
        self.log_failures = open(
            f'logs_failures/game{self.run_no}/game_log_failures_{self.run_no}.txt', 'w')
        self.df = pd.DataFrame(columns=['active_id', 'passive_id', 'active_reliability',
                               'passive_reliability', 'passive_opinion', 'accepted', 'result', 'total_payout'])
        self.df_failures = pd.DataFrame(columns=['passive_id', 'num_attempts', 'total_penalty_payout'])
        self.df_aggregate_failures = pd.DataFrame(columns=['mean_num_attempts'])
        self.csv_path = f'logs_failures/game{self.run_no}/game_log_{self.run_no}.csv'
        self.csv_path_failures = f'logs_failures/game{self.run_no}/game_log_failures_{self.run_no}.csv'
        self.csv_path_aggregate_failures = f'logs_failures/game{self.run_no}/game_log_aggregate_failures_{self.run_no}.csv'

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
            exp_r_i = 0
            payoff_threshold = 0
            if (self.r_dist == 'uniform'):
                r_i = np.random.uniform(0, 1)
                exp_r_i = 0.5
            elif (self.r_dist == 'normal'):
                r_i = np.random.normal(0, 1)
                exp_r_i = 0
            elif (self.r_dist == 'bernoulli'):
                r_i = np.random.randint(0, 1)
                exp_r_i = 0.5
            elif (self.r_dist == 'skewed'):
                r_i = np.random.beta(2,6)
                exp_r_i = 0.25
                payoff_threshold = -1.005
            self.agents[i] = LearnTrustAgent(
                i, r_i, self.alpha_direct, self.alpha_indirect, exp_r_i, payoff_threshold)
            self.r_arr[i] = r_i
        # print("agent array: ", self.agents)

    def run_encounter(self, i, active_id, passive_id):
        '''
        initiate an encounter between two random agents, have the passive agent run the encounter,
        and update encounter history and total payoff according to encounter outcome
        args:
            i: encounter number in the whole game
        '''
        active_agent = self.agents[active_id]
        passive_agent = self.agents[passive_id]
        passive_agent_opinion = passive_agent.get_registers()[active_id]
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
        encounter_print_string = f"ENCOUNTER {i}.\nActive ID: {active_id}\nPassive ID: {passive_id}\nActive agent reliability: {active_agent.get_reliability()}\nPassive agent reliability: {passive_agent.get_reliability()}\nPassive agent's opinion of active agent: {passive_agent_opinion}\nEncounter accepted: {accepted}\nEncounter result: {result}\nTotal payout: {self.total_payout}\n"
        encounter_print_string += '\n###########################\n'
        self.log.write(encounter_print_string)
        self.encounter_history.append(encounter_dict)
        self.df.loc[len(self.df.index)] = encounter_dict
        return [accepted, result, encounter_print_string]

    def run(self):
        self.initialize_agents()
        print("TEST: ", self.agents[0].get_reliability())
        for j in range(self.num_interactions):
            attempt_counts = [0] * self.agents_per_trial
            passive_ids = np.random.choice(range(self.num_agents), size=self.agents_per_trial, replace=False)
            for i in range(self.agents_per_trial):
                passive_id = passive_ids[i]
                df_failures_row = {
                    'passive_id': passive_id
                }
                active_range_pool = list(range(self.num_agents))
                active_range_pool.remove(passive_id)
                attempt_count = 0
                while True:
                    active_id = np.random.choice(active_range_pool, size=1)[0]
                    accepted, result = (self.run_encounter(i, active_id, passive_id))[:2]
                    if accepted and not result:
                            attempt_count += 1
                    if accepted and result:
                        attempt_count += 1
                        break
                    if attempt_count > self.num_agents:
                        break
                attempt_counts[i] = attempt_count
                df_failures_row['num_attempts'] = attempt_count
                df_failures_row['total_penalty_payout'] = (attempt_count - 1) * self.p_b
                log_failures_print_string = f'Run {j}: Passive agent {passive_id} took {attempt_count} attempts to get a successful encounter. Penalty this agent incurred: {(attempt_count - 1) * self.p_b}\n'
                print(log_failures_print_string)
                self.log_failures.write(log_failures_print_string)
                self.df_failures.loc[len(self.df_failures.index)] = df_failures_row
            df_agg_failures_row = {
                'mean_num_attempts': np.mean(attempt_counts)
            }
            self.df_aggregate_failures.loc[len(self.df_aggregate_failures.index)] = df_agg_failures_row
        self.df.to_csv(self.csv_path)
        self.df_failures.to_csv(self.csv_path_failures)
        self.df_aggregate_failures.to_csv(self.csv_path_aggregate_failures)
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

    num_agents = 100
    r_dist = 'skewed'
    num_interactions = 750

    game = Game(num_agents=num_agents, r_dist=r_dist,
                num_interactions=num_interactions)
    encounter_history = game.run()

    # print(encounter_history)


if __name__ == "__main__":
    main()
