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
L.herb = [Herbivore(age=5, weight=20) for i in range(50)]
L.carni = [Carnivore(age=5, weight=100) for i in range(100)]
for i in range(100):
    #print(len(L.herb), len(L.carni), L.fodder)
    L.simulate()
    print(len(L.herb), len(L.carni), L.fodder)