# EPLANopt #
EPLANopt is a energy system optimization model based on the EnergyPLAN software developed by Aalborg University. This model is specifically designed to inspect and identify the best future alternatives for the energy system by considering the challenges of the energy transition. This repository contains the EPLANopt model and its associated files. 
![](MAC.gif)

## Requirements ##
- EnergyPLAN version >=15.1 (to download the software developed by [Aalborg University](https://www.en.plan.aau.dk/) go to [EnergyPLAN website](https://www.energyplan.eu/))

## Features ##
- High temporal resolution for accurately capturing renewable energy variability.
- Sector-coupling to evaluate synergies between energy sectors.
- Multi-objective optimization approach for transparent decision-making.
- Partnering with Eurac Research for model development and application.

## Key Components ##
* Future best energy mixes
* Evaluation of costs for current and future energy systems
* Analysis of the structure of the energy system cost
* Hourly energy flows and exchanges analysis
* Must-haves and must-avoids for decarbonization measures

## Solution Advantages ##
* Integrated: Considers all energy sectors (power, heating, cooling, transport, and industry) in an integrated approach.
* High resolution: Properly evaluates the intermittency of renewable energy sources.
* Transparent: Provides the Pareto front of optimal techno-economic solutions for policy makers.
* Must-have and must-avoids: Identifies common and missing elements of optimal scenarios.
* Demonstrated: Applied to various case studies at different scales and locations.

## How to reproduce the example ##
The example presented in this repository is based on the Scenario DK2020_2018edition_cost update.txt provided with the download of the EnergyPLAN software. This file is saved in the input_folder together its ANSI version. To produce the ANSI version needed by the code, you just need to follow these simple instructions: i) Open the DK2020_2018edition_cost update.txt file, ii) File, Save as..., iii) on the bottom change the encoding from Unicode to ANSI, iv) change the name of the file in order to remember that it is the ANSI version and click on Save. This is just to let you know the steps you have to go through if you want to change the EnergyPLAN input file. In the folder you can already find the ANSI version for the considered example: DK2020_2018edition_cost update_ANSI.txt

It is now possible to run the TestGA.py file. in the libeplan.py file there are all the functions used to write input, execute EnergyPLAN and read output.

## Results ##
Once the optimization is finished the history_csv.csv is created. It reports all the simulations done by the genetic algorithm (Multi-Objective Evolutionary Algorithm) and their objective function values. It is now time to run the Pareto.py script to find the Pareto Front of optimal solutions. Once this python file has been correctly executed, the output is the Pareto.xlsx file which has the following 2 sheets:
a) **history**. This sheet contains all the simulated solutions and keep track of the process done by the genetic algorithm within the optimization process. 
b) **Pareto**. This sheet contains the the optimal solutions on the Pareto front. it is what you should analyse in order to interpret the results 

It needs to be mention that this example it's just to show the results that it is possible to obtain with this methodology. The results are consequence of the costs implemented in DK2020_2018edition_cost update.txt that have not been modified or checked. 

## How to cite EPLANopt ##
If you use **EPLANopt** for your research, we would appreciate it if you would cite the following papers:
* Prina MG, Cozzini M, Garegnani G, Manzolini G, Moser D, Filippi Oberegger U, et al. Multi- objective optimization algorithm coupled to EnergyPLAN software: The EPLANopt model. Energy 2018;149:213–21. doi:10.1016/j.energy.2018.02.050. https://www.sciencedirect.com/science/article/pii/S0360544218302780
* Prina MG, Manzolini G, Moser D, Vaccaro R, Sparber W. Multi-Objective Optimization Model EPLANopt for Energy Transition Analysis and Comparison with Climate-Change Scenarios. Energies 2020;13:3255. doi:10.3390/en13123255. https://www.mdpi.com/1996-1073/13/12/3255
* Prina MG, Moser D, Vaccaro R, Sparber W. EPLANopt optimization model based on EnergyPLAN applied at regional level: the future competition on excess electricity production from renewables. Int J Sustain Energy Plan Manag 2020;27:35–50. doi:10.5278/ijsepm.3504. https://journals.aau.dk/index.php/sepm/article/view/3504
* Groppi D, Nastasi B, Prina MG, Astiaso Garcia D. The EPLANopt model for Favignana island’s energy transition. Energy Convers Manag 2021;241:114295. doi:10.1016/j.enconman.2021.114295 https://www.sciencedirect.com/science/article/pii/S0196890421004714


## Acknowledgements ##
- Aalborg University for developing the EnergyPLAN software.


For any questions or concerns, please visit our [Eurac Research website](https://www.eurac.edu/it/people/matteo-giacomo-prina).
