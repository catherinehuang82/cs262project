import numpy as np

class LearnTrustAgent:
    '''
    This class represents a LearnTrust agent in the simulation. 
    Attributes
    ----------
    id : int
        unique identifier for this agent
    reliability : float
        reliability score of this agent, value in range (0,1)
    registers : dict
        dict mapping neighbor id to reliabilty opinion
    alpha_direct : float
        decay rate for direct opinion updates
    alpha_indirect : float
        decay rate for second-hand opinion updates
    encounter_history : list
        list of encounter results
    payoff_threshold : float
        threshold for when this agent will accept an encounter

    Methods
    -------
    get_reliability()
        returns reliability score of this agent

    get_registers()
        returns dict mapping neighbor id to reliabilty opinion
    
    handle_encounter(active_id, active_id_reliability, active_id_registers, p_g, p_b)
        handle encounter when this agent is asked to participate in an encounter as the passive agent.
    '''

    def __init__(self, id: int, reliability: float, agent_type: string, alpha_direct: float, alpha_indirect: float, expected_r_dist: int = 0.5, payoff_threshold: float = 0):
        self.id = id
        self.reliability = reliability # quantity between 0 and 1
        self.agent_type = agent_type
        registers_indices = list(range(100))
        registers_indices.remove(id)
        self.expected_r_dist = expected_r_dist
        self.registers = dict.fromkeys(registers_indices, self.expected_r_dist) # reliability estimates of the other agents. dict mapping neighbor id to reliabilty opinion
        self.alpha_direct = alpha_direct
        self.alpha_indirect = alpha_indirect
        self.encounter_history = [] # this attribute is not yet used, but could be useful
        self.payoff_threshold = payoff_threshold # tau_i in the paper

    def get_reliability(self):
        return self.reliability

    def get_agent_type(self):
        return self.agent_type
    
    def get_registers(self):
        return self.registers

    def get_opinion(self, agent_id: int) -> float:
        '''
        returns opinion of this agent on the reliability of the agent with the given id
        '''
        return self.registers[agent_id]

    def handle_encounter(self, active_id: int, active_id_reliability: int, active_id_registers: dict, p_g: float, p_b: float):
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
        # accept encounter if predicted expected payoff is above threshold
        accepted = predicted_expected_payoff >= self.payoff_threshold
        
        success = 0
        if accepted:
            reliability_sample = np.random.random()
            success = reliability_sample < active_id_reliability # result is true (1) if encounter is successful, false (0) otherwise
    
        # have passive agent do opinion updating
        if accepted:
            # update opinion of active agent directly
            self.registers[active_id] = (1 - self.alpha_direct) * self.registers[active_id] + self.alpha_direct * success
            if success:
                # update opinions of all other agents through active agent's opinions, since this passive agent now trusts the active agent
                for id in active_id_registers.keys():
                    if id == self.id:
                        continue
                    self.registers[id] = (1 - self.alpha_indirect) * self.registers[id] + self.alpha_indirect * active_id_registers[id]

        return accepted, success