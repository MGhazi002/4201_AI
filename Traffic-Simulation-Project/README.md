Traffic Simulation and Road Construction Recommendation

This project utilizes NetworkX, a Python library for the creation, manipulation, and study of the complex networks of roads within a city. The aim is to simulate traffic flow over a 10-hour period to identify where new roads should be constructed to reduce traffic congestion and improve journey times, within a given budget for new roads.
Project Overview

The application simulates traffic within a city's road network, represented as a graph with nodes (intersections) and edges (roads). It models traffic flow, computes the volume of traffic on each road segment, and uses this data to recommend where new roads could be built to optimize traffic conditions.
Key Features

    Graph-Based Traffic Simulation: Uses NetworkX to model the city's road network.
    Traffic Flow Simulation: Simulates traffic over a defined period, generating trips and calculating shortest paths between random start and end points.
    Traffic Volume Analysis: Analyzes the simulated traffic to determine the volume of traffic on each road segment.
    Road Construction Recommendation: Identifies and recommends new roads that, when constructed, are expected to offer the most significant improvements in traffic flow.

Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.
Prerequisites

    Python 3.x
    NetworkX
    NumPy

Installing

First, clone the repository to your local machine:

bash

git clone https://github.com/MGhazi002/4201_AI.git

Navigate to the project directory:

bash

cd traffic-simulation-project

Install the required Python packages:

bash

pip install -r requirements.txt

Running the Simulation

To run the simulation, execute the main script:

bash

python simulate_traffic.py

Usage

Modify the parameters in simulate_traffic.py to adjust the simulation settings, such as the number of nodes (intersections), the probability of road connections, and the number of trips generated per tick.
Contributing

Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests to us.
Versioning

We use SemVer for versioning. For the versions available, see the tags on this repository.
Authors

    Austin Hoffman, Muhammad Ghazi - Initial work - YourUsername

License

This project is licensed under the MIT License - see the LICENSE.md file for details.
Acknowledgments

    Hat tip to anyone whose code was used
    Inspiration
    etc.
