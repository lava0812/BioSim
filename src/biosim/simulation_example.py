from src.biosim.landscape import Landscape, Lowland, Water
from src.biosim.animals import Animal, Herbivore, Carnivore


def simulate(self):
    self.new_fodder()
    self.eat_fodder()
    self.prey()
    self.death_population()
    self.newborn_herb()
    self.newborn_carni()
    self.weight_loss()
    self.aging_population()


L = Landscape()
L.herb = [Animal(5, 20) for i in range(50)]
L.carni = [Animal(5, 20) for i in range(50)]
for i in range(500):
    L.simulate()
    print(len(L.herb), len(L.carni), L.fodder)
