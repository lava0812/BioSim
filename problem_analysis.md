#Problem analysis - A41 Sathuriyan Lavanyan 

##Key questions 
### - What are the key components of the "world" to simulate?
We will mainly have 5 files that we will be working with. These are animals.py, landscape.py, island.py, 
visualization.py and simulation.py. Each file will build upon classes. 
###Landscape
This part of the script will provide us with information about the landscape; how they function and how the interaction 
is between one another

    - Superclass Landscape that contains common characteristics of the different environment.
    - Four subclasses (Highland, Lowland, Desert and Water)
    - Methods for age, death, fodder, migration and population count


###Island
This part will focus on building the island, and implement the annual cycle to the code.
 
    - Implement the Annual Cycle on Rossumøya.
    - Feeding, procreation, migration, aging, loss of weight and death
    - Design methods for migration rules.
    - The landscape affect the island build.
###Animal
This part focus on the animals on the island, and their way of acting.

    - Superclass Animal that contains common characteristics of the herbivores and carnivores.
    - Two subclasses (herbivores and carnivores)
    - Methods for aging, eating, procreation, fitness and death 
    - A method that allows you to change the given parameters


## Key aspects of running and visualising a simulation

###Simulation
    - Good code structure and documentation.
    - Not a time consuming simulation.
    - Users can adjust the simulation setting for their preferences.
    - Make a versatile code that can be used with different parameters.
    - Able to stop the simulation mid way

###Visualising
    - Informative graphs.
    - Total number of animals on the island.
    - Histogram.

## Representation of code

    - Complete tests for all functions.
    - Document while coding, and not after.
    - Follow the PEP8 guidelines.
    - Sphinx standard. 







