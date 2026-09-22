from flora import Flora, flora_species
import fruit
import random



def plant_patch():
    patch = []

class DummyRealm():
    def __init__(self, temperature = 1):
        self.temperature = temperature
        self.name = "WastelandQ"
        

def test_flora_initialisation():
    realm = DummyRealm(temperature=2)
    genotype = [10, 3, 0.5]

    flora = Flora(1, genotype, realm, 20, 30)

    assert flora.id == 1
    assert flora.x == 20
    assert flora.y == 30
    assert flora.capacity == 10
    assert flora.batch_size == 3
    assert flora.rate == 1
    assert flora.fruitNo == 0
    assert flora.fruit == fruit.apple

def test_bear():
    flora = Flora(1, [10, 2, 1], DummyRealm(), 0, 0)

    flora.bear(3)

    assert flora.fruitNo == 3


def test_bear_default():
    flora = Flora(1, [10, 2, 1], DummyRealm(), 0, 0)

def test_tick_bears_fruit():
    random.seed(1)

    flora = Flora(
        1,
        [10, 3, 0.5],
        DummyRealm(temperature=1),
        0,
        0
    )

    flora.tick()

    assert flora.fruitNo == 3

    flora.bear()

    assert flora.fruitNo == 1


def test_provide():
    flora = Flora(1, [10, 2, 1], DummyRealm(), 0, 0, fruitNo=5)

    provided = flora.provide(3)

    assert provided == 3
    assert flora.fruitNo == 2


def test_provide_more_than_available():
    flora = Flora(1, [10, 2, 1], DummyRealm(), 0, 0, fruitNo=2)

    provided = flora.provide(10)

    assert provided == 2
    assert flora.fruitNo == 0

def test_provide_zero():
    flora = Flora(1, [10, 2, 1], DummyRealm(), 0, 0, fruitNo=5)

    provided = flora.provide(0)

def test_tick_bears_fruit():
    random.seed(603094)
    flora = Flora(1, [10, 3, 0.5], DummyRealm(temperature=1),0,0)
    flora.tick()
    
    assert flora.fruitNo == 3

def test_tick_does_not_bear_fruit():
    random.seed(6030942)
    flora = Flora(1, [10, 3, 0.5], DummyRealm(temperature=1),0,0)
    flora.tick()
    assert flora.fruitNo == 0




