import numpy as np

class LearnTrustAgent:
    
    def __init__(self, id, reliability, alpha_direct, alpha_indirect):
        self.id = id
        self.reliability = reliability # quantity between 0 and 1
        registers_indices = list(range(100))
        registers_indices.remove(id)
        self.registers = dict.fromkeys(registers_indices, 0.5) # reliability estimates of the other agents. dict mapping neighbor id to reliabilty opinion
        self.alpha_direct = alpha_direct
        self.alpha_indirect = alpha_indirect
        self.encounter_history = [] # this attribute is not yet used, but could be useful

    def get_reliability(self):
        return self.reliability
    
    def get_registers(self):
        return self.registers

    def handle_encounter(self, active_id, active_id_reliability, active_id_registers, p_g, p_b):
        '''
        handle encounter when this agent is asked to participate in an encounter as the passive agent.
        this handling includes choosing whether to accept the encounter request, and updating opinions
        on other agents' reliability scores based on the encounter's result.
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
        predicted_expected_payoff = opinion * p_g + (1 - opinion) * p_b
        accepted = predicted_expected_payoff >= 0
        if accepted:
            reliability_sample = np.random.random()
            result = reliability_sample < active_id_reliability
        else:
            result = 0
        # have passive agent do opinion updating
        if accepted:
            # update opinion of active agent directly
            self.registers[active_id] = (1 - self.alpha_direct) * self.registers[active_id] + self.alpha_direct * result
            if result:
                # update opinions of all other agents through active agent's opinions, since this passive agent now trusts the active agent
                for id in active_id_registers.keys():
                    if id == self.id:
                        continue
                    self.registers[id] = (1 - self.alpha_indirect) * self.registers[id] + self.alpha_indirect * active_id_registers[id]

        return [accepted, result]