# SignalFlow
This repo serves as the core implementation of an IRL algorithm for the purposes of predicting the behavior of a arbitrary discrete space signal

### Description
The goal is to take in a action signal that is controlling a simple robotic system with arbitrary dynamics based on
a user input provided by the user. The user input device and the robot system are seperated by an imperfect network thatThis input force signal is a two dimensional vector. 
can drop data coming from the user for certain periods of time.
The actions are processed by the learning block by collecting the time series of states and calculating the state action
pairs based on the deterministic transition probability of the signal.

## Setup
The Inverse Reenforcment Learning library is dependent on several conditions
In order to meet all the conditions its recommended you install anaconda for python3
https://docs.anaconda.com/anaconda/install/index.html

Then Import the environment following the instructions: 
https://docs.anaconda.com/anaconda/navigator/tutorials/manage-environments/#importing-an-environment


## Getting Started
Start by running integrate.py 

## Notes on structure
The data for demonstrations is stored within the /data directory. 
There also lies some of the data processing functions to condition the data 
prior to ingestion by one of the MDP classes.
