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

In the first setting, multiple "active" agents are initiating encounters with other "passive" agents, who decide whether or not to accept the encounter. After each encounter, either both agents receive a "good" or "bad" payoff, with the probability of a good payoff dependent on agent reliability. This setting could simulate peer-to-peer systems like BitTorrent, where users must collaborate to upload and download large files, tending to choose more helpful peers in the long run. Here, both overall payout and the "shape" of community payout are important: the first metric measures how happy and efficient the community is overall, while the second helps us gauge fairness. Fairness can be considered from multiple perspectives, such as everyone receiving near-uniform payoff or more reliable agents receiving more payoff, etc.

In the second setting, we focus on one "passive" agent, who is trying to perform some computation. This computation is a large task and they need help from several other computers. Several "active" agents volunteer to help, and the passive agent must accept or deny their requests. This could simulate helpful researchers trying to aid in a task, along with malicious actors who are trying to ruin the computation. We are interested in observing how many encounter attempts a passive agent needs before a successful encounter.

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

### Agent reliability distributions
We initialize the population with a distribution of reliability scores.
* Uniform: uniform distribution in range [0,1]
* Normal: normal distribution with mean 1, stddev 1
* Bernoulli: everyone has either perfect reliability (1) or none (0) w/ probability 0.5 each
* Beta(2, 10): makes it more likely for agents to be unreliable

We wanted to test results under each of these distributions.

### Relative magnitudes of good and bad payoffs
Upon a successful/unsuccessful encounter, both agents receive a good/bad payoff. 

Some experiments we wanted to try:
* Good/bad payoffs are equal (e.g. good payoff = 1, bad payoff = -1)
* Skewed good payoff and different magnitudes (e.g. good payoff = 3, bad payoff = -1)
* Skewed bad payoff and different magnitudes (e.g. good payoff = 1, bad payoff = -2)
* Passive agent receives more payoffs (e.g. upon good encounter, passive/active agents receive 3/1 payoffs respectively; upon bad encounter, passive/active agents receive -1/-3 payoffs respectively)
* Active agent receives more payoffs

### Types of agents present and the proportion of each
Agent types:
* learn_trust: the agent initializes their opinion of each agent to the expected value (e.g. 0.5 for a uniform(0,1) distribution), then updates their opinions over time. Their likelihood of accepting an encounter from an agent is proportional to their opinion of them.
* know_reliability: the agent has perfect information, i.e. knows every agent's true reliability.
* always_accept: the agent accepts all interactions.
* always_deny: the agent denies all interactions. 

Some experiments we wanted to try:
* Purely learn_trust agents
* Purely know_reliability agents
* A mix of all 4 types of agents of varying proportions

Potential future agent types to try:
* Agents that are more forgiving in early encounters (e.g. lower threshold to accept an interaction) and have higher standards over time. This could be reasonable because we don't want to penalize a high-reliability neighbor who happened to mess up once.

## Conclusion
To read the final paper with more detailed descriptions of our experiments and results, please reach out to the authors at karlyhou@college.harvard.edu, catherinehuang@college.harvard.edu, and adammohamed@college.harvard.edu.