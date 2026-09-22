import random
from anima import Anima, bleed
from extratraits import ExtraTraits


class DummyRealm:
    def __init__(self, temperature=1):
        self.temperature = temperature
        self.width = 100
        self.height = 100
        self.environment = [["grass" for _ in range(100)] for _ in range(100)]
        self.fruit_list = []
        self.creature_naming_mode = "nameless"
        self.name = "The Great Wonder..."

    def anima_id(self):
        #dummy id not required
        return 0


def make_genome():
    return [("apple", "meat"), [2, [1, 1, 1]], 0.5, 10, 5, 5, 20, 2, 10, 10, 5, ExtraTraits(set())]


def make_anima():
    return Anima(1, "nameless", make_genome(), DummyRealm(), 50, 50)


def test_anima_initialisation():
    # Asserts starting attributes of anima
    anima = make_anima()
    assert anima.id == 1
    assert anima.x == 50
    assert anima.y == 50
    assert anima.age == 0
    assert anima.status == [25, 25, 0, 0, -999]
    assert anima.target is None
    assert anima.mode == 1
    assert anima.asleep is False
    assert anima.strength == 5
    assert anima.toughness == 5
    assert anima.speed == 2
    assert anima.vision == 10


def test_size():
    anima = make_anima()
    assert anima.size() == 5


def test_diet_type_carnivore():
    # Tests meat-only diet is identified as carnivorous
    anima = make_anima()
    anima.diet = ("meat",)
    assert anima.diet_type() == "carnivore"


def test_diet_type_omnivore():
    # Tests diet containing meat and plants is identified as omnivorous
    anima = make_anima()
    anima.diet = ("meat", "apple")
    assert anima.diet_type() == "omnivore"


def test_diet_type_herbivore():
    # Tests plant-only diet is identified as herbivorous
    anima = make_anima()
    anima.diet = ("apple",)
    assert anima.diet_type() == "herbivore"


def test_is_satiated():
    # Tests the boundary at which an Anima is considered satiated
    anima = make_anima()
    anima.status[0] = 34
    assert anima.is_satiated() is True
    anima.status[0] = 35
    assert anima.is_satiated() is False


def test_is_starving():
    # Tests the boundary at which an Anima is considered starving
    anima = make_anima()
    anima.status[0] = 72.5
    assert anima.is_starving() is False
    anima.status[0] = 72.6
    assert anima.is_starving() is True


def test_is_injured():
    # Tests the injury threshold based on damage
    anima = make_anima()
    anima.status[3] = 10
    assert anima.is_injured() is False
    anima.status[3] = 10.1
    assert anima.is_injured() is True


def test_is_bleeding():
    # Tests for 'bleed' affliction in conditions
    anima = make_anima()
    assert anima.is_bleeding() is False
    anima.conditions.append(bleed)
    assert anima.is_bleeding() is True


def test_is_mature():
    # Tests the maturity boundary based on maturity age
    anima = make_anima()
    anima.age = anima.maturity_age - 1
    assert anima.is_mature() is False
    anima.age = anima.maturity_age
    assert anima.is_mature() is True


def test_is_senescent():
    # Tests the senescence boundary based on senescence age
    anima = make_anima()
    anima.age = anima.senescence_age - 1
    assert anima.is_senescent() is False
    anima.age = anima.senescence_age
    assert anima.is_senescent() is True


def test_update_increases_status():
    # Tests that update correctly increases a status value
    anima = make_anima()
    anima.status[0] = 25
    anima.update(0, 5)
    assert anima.status[0] == 30


def test_update_decreases_status():
    # Tests that update correctly decreases a status value
    anima = make_anima()
    anima.status[0] = 25
    anima.update(0, -5)
    assert anima.status[0] == 20


def test_update_clamps_status_at_zero():
    # Tests that normal status values cannot fall below zero
    anima = make_anima()
    anima.status[0] = 2
    anima.update(0, -5)
    assert anima.status[0] == 0


def test_update_mating_drive_cannot_exceed_maximum():
    # Tests that mating drive is capped at the maximum value after maturity
    anima = make_anima()
    anima.age = anima.maturity_age
    anima.status[4] = 70
    anima.update(4, 20)
    assert anima.status[4] == 75


def test_provide_enough_food():
    # Tests that 'provide' removes and returns the requested amount when enough food is available.
    anima = make_anima()
    anima.food_chunks = 10
    assert anima.provide(3) == 3
    assert anima.food_chunks == 7


def test_provide_not_enough_food():
    # Tests that provide returns all available food when the requested amount is unavailable.
    anima = make_anima()
    anima.food_chunks = 2
    assert anima.provide(5) == 2
    assert anima.food_chunks == 0


def test_provide_zero_food():
    # Tests that providing food from an empty food source returns zero.
    anima = make_anima()
    anima.food_chunks = 0
    assert anima.provide(5) == 0
    assert anima.food_chunks == 0


def test_drink():
    # Tests that drinking decreases thirst by five.
    anima = make_anima()
    anima.status[1] = 25
    anima.drink()
    assert anima.status[1] < 25


def test_sleep():
    # Tests that sleeping changes sleep-related state and clears temporary lists.
    anima = make_anima()
    anima.status[2] = 20
    anima.status[3] = 5
    anima.sleep_debt = 4
    anima.rejected = [1]
    anima.eatenList = [2]
    anima.sleep()
    assert anima.asleep is True
    assert anima.sleep_debt == 0
    assert anima.status[2] > 20
    assert anima.status[3] < 4
    assert anima.rejectedList == []
    assert anima.eatenList == []


def test_move():
    # Tests that an Anima moves according to its velocity
    anima = make_anima()
    anima.x = 50
    anima.y = 50
    anima.dx = 2
    anima.dy = 3
    anima.move()
    assert anima.x == 52
    assert anima.y == 53


def test_move_wraps_horizontal_position():
    # Tests that horizontal movement wraps around the realm boundary
    anima = make_anima()
    anima.x = 99
    anima.y = 50
    anima.dx = 2
    anima.dy = 0
    anima.move()
    assert anima.x == 1


def test_move_wraps_vertical_position():
    # Tests that vertical movement wraps around the realm boundary
    anima = make_anima()
    anima.x = 50
    anima.y = 99
    anima.dx = 0
    anima.dy = 2
    anima.move()
    assert anima.y == 1


def test_is_family_with_parent():
    # Tests that an Anima recognises its parent as family
    anima = make_anima()
    parent = make_anima()
    anima.parents = [parent]
    assert anima.is_family(parent) is True


def test_is_family_with_child():
    # Tests that an Anima recognises its child as family
    anima = make_anima()
    child = make_anima()
    child.parents = [anima]
    anima.offspring = [child]
    assert anima.is_family(child) is True


def test_is_family_with_unrelated_anima():
    # Tests that unrelated Animas are not identified as family
    anima = make_anima()
    other = make_anima()
    assert anima.is_family(other) is False


def test_is_dead_from_starvation():
    # Tests that an Anima dies when its hunger reaches the death threshold
    anima = make_anima()
    anima.status[0] = 100
    assert anima.is_dead() is True


def test_is_not_dead_from_sleepiness():
    # Tests that high sleepiness alone does not cause death
    anima = make_anima()
    anima.status[2] = 100
    assert anima.is_dead() is False


def test_autopsy_starvation():
    # Tests that starvation is correctly identified as the cause of death
    anima = make_anima()
    anima.status[0] = 100
    assert anima.autopsy() == "starvation"


def test_autopsy_thirst():
    # Tests that thirst is correctly identified as the cause of death
    anima = make_anima()
    anima.status[1] = 100
    assert anima.autopsy() == "thirst"


def test_autopsy_wounds():
    # Tests that fatal damage is correctly identified as the cause of death
    anima = make_anima()
    anima.status[3] = 100
    assert anima.autopsy() == "its wounds"
