import numpy as np

class Agent:
    
    def __init__(self, id, reliability):
        self.id = id
        self.reliability = reliability # quantity between 0 and 1
        registers_indices = list(range(100))
        registers_indices.remove(id)
        self.registers = dict.fromkeys(registers_indices, 0.5) # neighborhood reliability estimates. dict mapping neighbor id to reliabilty opinion
        self.encounter_history = [] # list of dictionaries with the following keys: ['']

    def get_reliability(self):
        return self.reliability
    
    def get_registers(self):
        return self.registers

    def handle_encounter(self, active_id, active_id_reliability, active_id_registers, p_g, p_b):
        '''
        handle encounter when this agent is asked to participate in an encounter as the passive agent.
        args:
            active_id: id of active agent "initiating" this encounter
            active_id_reliability: reliability score of active agent
            active_id_registers: registers (opinions) of active agent
            p_g: payout if encounter if good
            p_b: payout if encounter is bad
        returns:
            accepted: boolean for whether or not this agent accepted the encounter
            result: boolean for whether or not this encounter was good
                these two quantities are returned so that the
                game state object can log this encounter in its hitory
        '''
        opinion = self.registers[active_id]
        # print("opinion: ", opinion)
        predicted_expected_payoff = opinion * p_g + (1 - opinion) * p_b
        accepted = predicted_expected_payoff >= 0
        if accepted:
            reliability_sample = np.random.random() 
            # print("reliability sample: ", reliability_sample)
            print("active id reliability: ", active_id_reliability)
            result = reliability_sample < active_id_reliability
            print("encounter result: ", result)
        else:
            result = 0
        if result:
            # TODO: implement opinion updating
            pass
        return [accepted, result]