# CS 262 Final Project: Trust System Simulation

## Engineering Notebook

## Initial Game Implementation
### Setup
* Agent class in agent.py
* Game class in simulation.py

### Description

As of now, our simulation focuses on exhibiting the result of a series of encounters between learn_trust agents (as described somewhere not yet defined lol). We do this using instances of the Agent class to represent a node in the distributed system, and this abstracts away the details of the actual interconnectedness between the agents to highlight what the system tends towards, exploring the effect of fine-tuning the parameters (starting reliabilities and opinions of each agent, the distributions used, etc.)

To more accurately explore the effect of having distributed systems inconsistencies, we'd need to change the simulation to run each agent as a process, and have a way for them to discover and connect to each other, as well as decide on the encounters themselves. Some specific details of implementation would vary depending on what kind of system it is -- for example, whether the system is designed with a finite number of agents involved. [Need to add more on this]

### Settings

We ran simulations to model two different distributed settings.

In the first setting, multiple "active" agents are initiating encounters with other "passive" agents, who decide whether or not to accept the encounter. After each encounter, either both agents receive a "good" or "bad" payoff, with the probability of a good payoff dependent on agent reliability. This setting could simulate peer-to-peer systems like BitTorrent, where users must collaborate to upload and download large files, tending to choose more helpful peers in the long run.

In the second setting, we focus on one "passive" agent, who is trying to perform some computation. This computation is a large task and they need help from several other computers. Several "active" agents volunteer to help, and the passive agent must accept or deny their requests. This could simulate helpful researchers trying to aid in a task, along with malicious actors who are trying to ruin the computation.

## Experiments
We wanted to observe what would happen to:
* Total community payoff 
* The shapes of individual payoff (i.e. who is getting more rewards?)

while varying parameters like
* Number of agents
* Number of interactions
* Agent reliability distributions 
* Relative magnitudes of good and bad payoffs
* The types of agents present and the proportion of each

## Conclusion
To read the final paper with more detailed descriptions of our experiments and results, please reach out to the authors at karlyhou@college.harvard.edu, catherinehuang@college.harvard.edu, and adammohamed@college.harvard.edu.