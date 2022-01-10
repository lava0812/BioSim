from src.biosim.landscape import Landscape, Lowland, Water
from src.biosim.animals import Animal, Herbivore, Carnivore


def simulate():
    Landscape().new_fodder()
    Landscape().eat_fodder()
    Landscape().prey()
    Landscape().newborn_herb()
    Landscape().newborn_carni()

    Landscape().aging_population()
    Landscape().weight_loss()
    Landscape().death_population()


L = Landscape()
L.herb = [Herbivore(age=5, weight=20) for i in range(100)]
L.carni = [Carnivore(age=5, weight=50) for i in range(100)]

for i in range(50):
    L.simulate()
    print(len(L.herb), len(L.carni), L.fodder)


# L.carni = [Carnivore(age=5, weight=50) for i in range(50)]
# for i in range(50):
#     print(len(L.carni), L.fodder)
#     L.simulate()


