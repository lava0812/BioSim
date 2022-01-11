from biosim.landscape import Landscape, Lowland, Water
from biosim.animals import Animal, Herbivore, Carnivore


# def simulate():
#     Lowland().new_fodder()
#     Lowland().eat_fodder()
#     Lowland().prey()
#     Lowland().newborn_herbivore()
#     Lowland().newborn_carnivore()
#
#     Lowland().aging_population()
#     Lowland().weight_loss()
#     Lowland().death_population()


L = Lowland()
L.herbivores = [Herbivore(age=39, weight=2000) for i in range(1000)]

#Herbivore.param["omega"] = 0
print(len(L.herbivores), L.fodder)
for i in range(5):
    L.annual_cycle()
    print(len(L.herbivores), L.fodder)


# L.carni = [Carnivore(age=5, weight=50) for i in range(50)]
# for i in range(50):
#     print(len(L.carni), L.fodder)
#     L.simulate()


