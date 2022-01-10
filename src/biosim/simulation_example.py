from src.biosim.landscape import Landscape, Lowland, Water
from src.biosim.animals import Animal, Herbivore, Carnivore


def simulate():
    Lowland().new_fodder()
    Lowland().eat_fodder()
    Lowland().prey()
    Lowland().newborn_herb()
    Lowland().newborn_carni()

    Lowland().aging_population()
    Lowland().weight_loss()
    Lowland().death_population()


L = Lowland()
L.herb = [Herbivore(age=5, weight=20) for i in range(50)]

for i in range(50):
    L.simulate()
    print(len(L.herb), L.fodder)

#
# L.carni = [Carnivore(age=5, weight=50) for i in range(50)]
# for i in range(50):
#     print(len(L.carni), L.fodder)
#     L.simulate()


