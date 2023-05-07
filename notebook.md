# CS 262 Final Project: Trust System Simulation

## Engineering Notebook

## Initial Game Implementation
### Setup
* Agent class in agent.py
* Game class in simulation.py

### Description

As of now, our simulation focuses on exhibiting the result of a series of encounters between learn_trust agents (as described somewhere not yet defined lol). We do this using instances of the Agent class to represent a node in the distributed system, and this abstracts away the details of the actual interconnectedness between the agents to highlight what the system tends towards, exploring the effect of fine-tuning the parameters (starting reliabilities and opinions of each agent, the distributions used, etc.)

To more accurately explore the effect of having distributed systems inconsistencies, we'd need to change the simulation to run each agent as a process, and have a way for them to discover and connect to each other, as well as decide on the encounters themselves. Some specific details of implementation would vary depending on what kind of system it is -- for example, whether the system is designed with a finite number of agents involved. [Need to add more on this]

## Systems problems to simulate
### Collaborative computation
* How many encounter attempts a passive agent needs before a successful encounter
* Implementation change: keep the passive agent around in the encounter,
and keep trying different active agents with this passive agent until we get a successful encounter for this passive agent
* Graphs: number of encounters needed per passive agent over time

### File uploading/downloading system
* The OG game can nicely simualate this
* Total payout across all agents <=> proportion of successful downloads, overall user satisfaction, etc.
