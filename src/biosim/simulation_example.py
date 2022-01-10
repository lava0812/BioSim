from src.biosim.landscape import Landscape, Lowland, Water
from src.biosim.animals import Animal, Herbivore, Carnivore


def simulate():
    Landscape().new_fodder()
    Landscape().eat_fodder()
    Landscape().prey()
    Landscape().death_population()
    Landscape().newborn_herb()
    Landscape().newborn_carni()
    Landscape().weight_loss()
    Landscape().aging_population()


L = Landscape()
L.herb = [Herbivore(age=5, weight=20) for i in range(50)]

for i in range(500):
    print(len(L.herb), L.fodder)
    L.simulate()

# L.carni = [Carnivore(age=5, weight=50) for i in range(50)]
# for i in range(50):
#     print(len(L.carni), L.fodder)
#     L.simulate()


