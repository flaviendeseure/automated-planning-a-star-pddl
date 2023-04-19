<a name="readme-top"></a>


<br />
<div align="center">
  <h1 align="center">Automated Planning with A* Search from PDDL domain </h1>
  <p align="center">
    Python implementation of an automated planning system that solves planning problems specified in PDDL using the A* search algorithm with heuristics.
    <br />
     
    
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![MIT License][license-shield]][license-url]
    
  </p>
</div>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#authors">Authors</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>



## About The Project
Automated Planning with A* Search from PDDL domain is a Python project that aims to solve planning problems specified in the Planning Domain Definition Language (PDDL) using the A* search algorithm with heuristics. The project provides a command-line interface that allows users to specify the domain and problem files. The program then parses the input files and uses the A* search algorithm to find a plan that achieves the goal state with minimum cost.

We propose some interesting heuristics :
1. **OneHeuristic**: return always one (no heuristic)
2. **ManhattanDistanceHeuristic**: calculates the Manhattan distance between a state and the goal
3. **Pattern DB**: calculates the distance between a state and the goal using a pattern database
4. **CustomHeuristic**: calculates the number of goal predicates that are not in the current state

This project is useful for anyone interested in automated planning and solving planning problems with PDDL. It can be used as a tool for experimenting with different heuristics or search algorithms and as a learning resource for understanding how automated planning works. The project is released under the MIT license, so it can be freely used, modified, and distributed.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Getting Started
This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Installation
1. Clone the repo
   ```sh
   git clone https://github.com/flaviendeseure/automated-planning-a-star-pddl.git
   cd automated-planning-a-star-pddl
   ```
2. Install Python packages  
   a. With Poetry
   ```sh
    poetry install
    ```
   b. With a virtual environment
   ```sh
    python -m venv planning_env
    source planning_env/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Usage
To run the script, use the following command:

1. With poetry
```sh
poetry run main [--group GROUP] [--problem PROBLEM] [--domain DOMAIN]
``` 
Exemple : 
```sh
poetry run main --group 2 --problem problem1
```   

2. With a virtual environment
```sh
source planning_env/bin/activate
python -m planification_automatique  [--group GROUP] [--problem PROBLEM] [--domain DOMAIN]
```
Exemple : 
```sh
python -m planification_automatique --group 2 --problem problem1
```   

where:  
- --group: integer that specifies the group number (default: 1).
- --problem: string that specifies the name of the problem file (default: "problem0").
- --domain: string that specifies the name of the domain file (default: "domain").  
  
The script will load the PDDL domain and problem files specified by --domain and --problem, respectively, and will run the A* search algorithm with a Manhattan distance heuristic to find a solution. The output will show the cost of the solution, the number of steps in the plan, and the time it took to find the solution. It will also print the plan found by the algorithm.  
  
An example of output is:   
```bash  
=========================================================  
Domain: groupe2 - domain  
Problem: problem0
=========================================================
Solution found with cost 8 in 7 steps and 0.59 seconds
-----------------------------------------
Found Plan:
-----------
move(pos62, pos61) => move(pos61, pos51) => move(pos51, pos41) => move(pos41, pos31) => shoot(pos31, pos21) 
=> move(pos31, pos21) => move(pos21, pos11)
=========================================================  
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Authors
- [Yoan Gabison](https://github.com/YoanGab)
- [Thomas Favoli](https://github.com/tf83f)
- [Noam Benitah](https://github.com/NoamBenitah)
- [Flavien Deseure--Charron](https://github.com/flaviendeseure)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License
Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

[contributors-shield]: https://img.shields.io/github/contributors/flaviendeseure/automated-planning-a-star-pddl.svg?style=for-the-badge
[contributors-url]: https://github.com/flaviendeseure/automated-planning-a-star-pddl/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/flaviendeseure/automated-planning-a-star-pddl.svg?style=for-the-badge
[forks-url]: https://github.com/flaviendeseure/automated-planning-a-star-pddl/network/members
[stars-shield]: https://img.shields.io/github/stars/flaviendeseure/automated-planning-a-star-pddl.svg?style=for-the-badge
[stars-url]: https://github.com/flaviendeseure/automated-planning-a-star-pddl/stargazers
[license-shield]: https://img.shields.io/github/license/flaviendeseure/automated-planning-a-star-pddl.svg?style=for-the-badge
[license-url]: https://github.com/flaviendeseure/automated-planning-a-star-pddl/blob/master/LICENSE.txt
