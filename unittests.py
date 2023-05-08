import unittest
import numpy as np
from agent import LearnTrustAgent
from config import TestConfig as Config

num_agents = Config.num_agents
num_encounters = Config.num_encounters

def initialize_agents(num_agents, r_dist: str = Config.r_dist, alpha_direct: float = Config.alpha_direct, alpha_indirect: float = Config.alpha_indirect):
        agents = [None] * num_agents

        for i in range(num_agents):
            r_i = 0
            exp_r_i = 0

            if (r_dist == 'uniform'):
                r_i = np.random.uniform(0, 1)
                exp_r_i = 0.5
            elif (r_dist == 'normal'):
                r_i = np.random.normal(0, 1)
                exp_r_i = 0
            elif (r_dist == 'bernoulli'):
                exp_r_i = 0.5
                r_i = np.random.randint(0, 2)
            
            agents[i] = LearnTrustAgent(
                i, r_i, alpha_direct, alpha_indirect, exp_r_i)

        return agents
            


class TestAgentClass(unittest.TestCase):
    '''
    Test the Agent class, and the following methods:
    - get_reliability()
    - get_opinion()
    - get_registers()
    - handle_encounter()
    '''

    def test_helper_methods(self):
        '''
        Test the helper methods of the Agent class
        '''
        for i in range(100):
            testAgent = LearnTrustAgent(id=i, reliability=0.5, alpha_direct=0.1, alpha_indirect=0.1)
            self.assertEqual(testAgent.get_reliability(), 0.5) # Test the get_reliability() method
            self.assertEqual(testAgent.get_reliability(), testAgent.reliability) # Test the get_reliability() method
            self.assertEqual(testAgent.get_registers(), testAgent.registers) # Test the get_registers() method

            # Test the get_opinion() method
            for id in testAgent.registers.keys():
                self.assertEqual(testAgent.registers[id], testAgent.get_opinion(id))


    def test_handle_encounter(self):
        # Initialize the agents to test encounter handling
        agents = initialize_agents(num_agents=num_agents, r_dist='uniform', alpha_direct=0.1, alpha_indirect=0.1)

        # Test the handle_encounter() method for 100 random encounters
        for i in range(100):
            active_id, passive_id = np.random.choice(
            range(num_agents), size=2, replace=False)
            active_agent = agents[active_id]
            passive_agent = agents[passive_id]

            opinion = active_agent.get_opinion(passive_id)
            predicted_expected_payoff = opinion * Config.p_g + (1 - opinion) * Config.p_b

            accepted, success = active_agent.handle_encounter(
                passive_id,
                passive_agent.get_reliability(),
                passive_agent.get_registers(),
                Config.p_g,
                Config.p_b
            )

            # Test the accepted and success data types
            self.assertTrue(accepted in [True, False])
            self.assertTrue(success in [True, False])
            
            # accepted should be True if the predicted expected payoff of the passive agent is >= active agents payoff threshold
            self.assertEqual(accepted, predicted_expected_payoff >= active_agent.payoff_threshold)


if __name__ == '__main__':
    unittest.main()
