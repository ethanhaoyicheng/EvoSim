class Fruit():
    def __init__(self, name = "apple", statusChange = [-150, 0, 0, -80, 80]):
        self.name = name
        self.statusChange = statusChange

apple = Fruit()
lily = Fruit("lily", [-150, 0, 0, -100, 100])
lavendar = Fruit("lavendar", [-50, 0, 50, -250, 10])
melon = Fruit("melon", [-1000, -100, 0, 0, 100])
berry = Fruit("berry", [-50, 0, 0, 0, 30])
wildgrass = Fruit("wildgrass", [-50, 0, 0, 0, 0])

bean = Fruit("bean", [-4000, -4000, -4000, -4000, 4000])

#capitalise fruit names??? gone :(