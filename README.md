# SignalFlow
This repo serves as the core implementation of an IRL algorithm for the purposes of predicting the behavior of a arbitrary discrete space signal

### Description
The goal is to take in a action signal that is controlling a simple robotic system with arbitrary dynamics based on
a user input provided by the user. The user input device and the robot system are seperated by an imperfect network thatThis input force signal is a two dimensional vector. 
can drop data coming from the user for certain periods of time.
The actions are processed by the learning block by collecting the time series of states and calculating the state action
pairs based on the deterministic transition probability of the signal.

## Getting Started
Start by running integrate.py 