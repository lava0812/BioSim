from src.biosim.landscape import Landscape, Lowland, Water




def simulate(self):
    self.new_fodder()
    self.eat_fodder()
    self.death_population()
    self.newborn_herb()
    self.weight_loss()
    self.aging_population()

    L = Landscape()
    L.herb = [Animal(5, 20) for i in range(50)]
    for i in range(1000):
        L.simulate()
        print(len(L.herb), L.fodder)
