# COMPSCI 262 Final Project: Trust System Simulation

## Motivation
Part of the premise of distributed systems is that machines collectively rely on one another to reliably and accurately carry out tasks for collective goals. For example, in federated learning, in order to end up with a well- behaving aggregate model, each private model must handle training correctly. In peer-to-peer file sharing systems like BitTorrent, machines must reliably distribute files over the Internet. In systems of nodes that cooperatively perform a computational task, the computation requester can only receive an accurate computation result if each machine does its part correctly. Many other trust- and security-based protocols happen over networks in distributed systems, such as browser certificate signing and password authentication. Trust management protocols exist not only between a user and a system, but also within different pieces of secure distributed system pipelines. The ever-increasing importance and ubiquity of trust in distributed systems motivates our desire to explore the impact of shifting parameters.

Past work has not comprehensively formalized trust in distributed systems. Questions like where trust comes from, how it is learned, or how it should be used to guide action, are not answered by traditional trust manage- ment systems (e.g. security policies, credentials). By figuring out how to encode trust components like beliefs, opinions, and impressions into a distributed system, we can work toward algorithms that make constituent nodes learn trust over time.

## Related Work
In [A Simple Game for the Study of Trust in Distributed Systems](https://link.springer.com/article/10.1007/bf03160228), Diamadi et al. formalize trust in a controlled game context by studying an artificial community of agents that use trust to succeed in a game against nature. In the game, agents are chosen at random to participate in pairwise encounters with other agents, which probabilistically go “well" (positive payout) or “poorly" (negative payout) depending on private agent reliability scores. Agents accept or deny encounter proposals based on their opinions of other agents’ reliability scores, which change depending on observed encounter outcomes. The objective of the game is for each agent to maximize per-agent and collective payout.

This game simulates trust learning, propagation, and utility because its multi-agent setting models the multiple- machine setting of a distributed system. The encounters in the game can model interactions between two machines over a network. The GOOD vs. BAD outcome of an encounter can represent the success or failure status of a machine with which another machine interacts (e.g. Byzantine failure in the form of an incorrect or inaccurate computation response, crash failure, etc.). The payout in the game corresponds to a a “goal" for our distributed system, whether that is an accurate numerical computation, undamaged file exchange, etc.

## Problem Statement
We implement the Diamadi et al. paper and extend it to specific experimental settings, the results of which we hope can shed light on the following:
* How experimental evaluation of agent behavior in the game can directly help us understand the learning, propagation, and utility of trust in real-world distributed systems that entail such trust. We are specifically interested in two motivating systems:
  1. A file uploading and downloading system, such as BitTorrent.
  2. A collection of nodes that collaboratively perform computation over a network, such as federated learning.
* How this game-based study of trust can broadly help us design more accurate and efficient secure distributed systems in the real world.

## Full Project Writeup
To read the final paper with more detailed descriptions of our experiments and results, please reach out to the authors at karlyhou@college.harvard.edu, catherinehuang@college.harvard.edu, and adammohamed@college.harvard.edu.
