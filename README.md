# EPLANopt #
EPLANopt allows the creation of the Marginal Abatement Cost (MAC) curve based on the EnergyPLAN software and by means of an optimization process. 

![](Chart_anim.gif)

## Requirements ##
- EnergyPLAN version >=15.1 (to download the software developed by [Aalborg University](https://www.en.plan.aau.dk/) go to [EnergyPLAN website](https://www.energyplan.eu/))

## How to reproduce the example ##
The example presented in this repository is based on the Scenario DK2020_2018edition_cost update.txt provided with the download of the EnergyPLAN software. This file is saved in the input_folder together its ANSI version. To produce the ANSI version needed by the code, you just need to follow these simple instructions: i) Open the DK2020_2018edition_cost update.txt file, ii) File, Save as..., iii) on the bottom change the encoding from Unicode to ANSI, iv) change the name of the file in order to remember that it is the ANSI version and click on Save. This is just to let you know the steps you have to go through if you want to change the EnergyPLAN input file. In the folder you can already find the ANSI version for the considered example: DK2020_2018edition_cost update_ANSI.txt
In the excel file called Input.xlsx you can find and set the following input of the model:
1) **Decision variables**. In this Sheet the decision variable are defined with labels, EPLAN label, Max potential and Additional step. The labels can be chosen by the user. The EPLAN label is the EnergyPLAN label that can be found in the DK2020_2018edition_cost update.txt regarding the related decision variable (for example for wind power in this case is 'input_RES1_capacity'). The Max potential is the maximum potential or upper bound of the decision variable for the expansion capacity opzimisation (in this example the are invented but reasonable numbers. However, a proper evaluation of this potential should be included in the analysis). The Additional step is the incremental value (in terms of installed power, capacity, additional share, etc.) of each decision variable on which is implemented the expansion capacity optimisation. 
2) **Paths and steps**. In this sheet the user has to define the path to the EnergyPLAN folder, the path to the input file (the ANSI version within the input_folder), the path to the output folder (that can also coincide with the input_folder) and the number of steps. The maximum number of steps defines the number of iterations resulting in the number of discreet elements in the MAC curve.
3) **Outputs**. In this sheet is possible to list other outputs that the user want to save from the EnergyPLAN output. These must have been defined with the key that is possible to find in the EnergyPLAN output file. For example the 'RES share of PES'. 

It is now possible to run the main.py file. in the libeplan.py file there are all the functions used to write input, execute EnergyPLAN and read output.
Once the simulation is finished (consider a number of simulations of energyPLAN equal to **Number of decision variables x Number of steps**, each simulation of EnergyPLAN can take 1-10 seconds depending on your machine). 

## Results ##
Once the simulation is finished the MAC.xlsx is produced. It has 4 sheets:
a) **MAC**. This sheet contains the winning decision variables for each step and all the info to plot the MAC curve.
b) **Cost effectiveness trends**. This sheet contains the values of the Cost effectiveness or Cost of CO2 Abatement (CCA) of each of the decision variables at each step. 
c) **CO2 trends**. This sheet contains the potential abatement of the decision variables at each step.
d) **Output trends**. This sheet contains the outputs of the solution implementing the winning decision variable. the outputs are defined in the Input.xlsx file and described in 3).

By running the MAC_plot.py file is possible to obtain the following plot (MAC.png):
<img src="MAC.png" width=70% height=70%>

It needs to be mention that this example it's just to show the results that it is possible to obtain with this methodology. The results in the above graph are consequence of the costs implemented in DK2020_2018edition_cost update.txt that have not been modified or checked. 

## How to cite EPLANoptMAC ##
If you use **EPLANoptMAC** for your research, we would appreciate it if you would cite the following paper (open access):
* Prina MG, Fornaroli FC, Moser D, Manzolini G, Sparber W. Optimization method to obtain marginal abatement cost-curve through EnergyPLAN software. Smart Energy 2021:100002. doi:10.1016/j.segy.2021.100002. https://www.sciencedirect.com/science/article/pii/S2666955221000022?via%3Dihub

To directly cite the code please refer to:

[![DOI](https://zenodo.org/badge/294351258.svg)](https://zenodo.org/badge/latestdoi/294351258)

## Video to explain the methodology ##
This video has been recorded within the [EMP-E 2020](http://www.energymodellingplatform.eu/) conference:

<a href="https://www.youtube.com/watch?v=0jXJhxtK_FY&t=3s" target="_blank">
 <img src="Video.JPG" alt="Watch the video" width=70% height=70% border="10" />
</a>
