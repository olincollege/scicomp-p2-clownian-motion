# Clownian Motion
Authored by @zbwrm (Aydin O'Leary) and @mmadanguit (Marion Madanguit).

Python script that models Brownian motion of particles and hopefully, eventually, colloidal glass transitions.

## Structure

* `particles.py` - performs all particle simulation calculations.
* `data.csv` - contains data output of simulation.
* `plot_collisions.py` - outputs animated simulation of the particles moving over time. 
* `plot_MSD.py` - outputs plot of the particles' mean square displacement over time.
* `plots` - contains example outputs of `plot_collisions.py` and `plot_MSD.py`

## Setup

1. Clone the repository.  
2. Run `python -m venv venv` and `source venv/bin/activate` to set up and activate a virtual environment. 
3. Run `pip install -r requirements.txt` to install the dependencies. 

## Run

1. Run `python particles.py` to run our simulation. 
2. Run `python particles.py > data.csv` to save the output of the simulation to a file called data.csv.
3. Run `python plot_collisions.py` to see an animated simulation of the particles moving over time.
4. Run `python plot_MSD.py` to see a plot of the particles' mean square displacement over time.

*Note: All plots open in a separate browser window.*

## Results

Animated simulation of particles moving over time:

![Animated simulation](https://github.com/olincollege/scicomp-p2-clownian-motion/blob/main/plots/plot_collisions.gif)

Plot of particles' mean square displacement over time:

![Mean square displacement over time](https://github.com/olincollege/scicomp-p2-clownian-motion/blob/main/plots/plot_MSD.png)
