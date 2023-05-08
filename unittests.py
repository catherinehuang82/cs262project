import unittest
from agent import LearnTrustAgent
from config import Config


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
            for j in range(100):
                self.assertEqual(testAgent.get_opinion(j), testAgent.registers[j])


    def test_handle_encounter(self):
        # Initialize the agents to test encounter handling
        for i in range(100):
            pass


if __name__ == '__main__':
    unittest.main()
