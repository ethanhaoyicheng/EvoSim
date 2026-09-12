class Biome():
    def __init__(self, facts):
        self.width_unit = facts[0][0]
        self.height_unit = facts[0][1]
        self.temperature = facts[1]
        self.wetness = facts[2][0]
        self.iceness = facts[2][1]
        self.vegetation = facts[3]
        #self.natural_elements = facts[4]
        #self.native_fauna = facts[5]

biomes = {
    "testk utopia" : Biome([[600, 400], 1, [0.2, 0.05], [["tree", 3000], ["bush", 5000], ["vine", 1250], ["reed", 1000], ["lily", 2000], ["wildgrass", 25000]]]),
    "testa apple experiment" : Biome([[600, 500], 1.25, [0.1, 0], [["tree", 600]]]),
    "grassland" : Biome([[10, 10], 1, [0.1, 0], [["tree", 100], ["lily", 100], ["wildgrass", 1500]]]),
    "forest" : Biome([[10, 10], 1, [0.1, 0], [["tree", 500], ["bush", 500], ["lily", 250]]]),
    "jungle" : Biome([[10, 10], 1.5, [0.15, 0], [["tree", 500], ["bush", 500], ["vine", 50], ["lily", 250]]]),
    "mountains" : Biome([[10, 10], 0.75, [0.15, 0.15], [["tree", 50], ["bush", 50], ["vine", 5], ["lily", 80], ["wildgrass", 50]]]),
    "desert" : Biome([[10, 10], 2, [0.02, 0], [["tree", 50], ["bush", 50], ["vine", 5], ["lily", 20], ["wildgrass", 10]]]),
    "dry tundra" : Biome([[10, 10], 0.2, [0.02, 0.5], [["tree", 50], ["bush", 50], ["vine", 5], ["wildgrass", 50]]]),
    "wet tundra" : Biome([[10, 10], 0.2, [0.2, 0.5], [["tree", 50], ["bush", 50], ["vine", 5], ["wildgrass", 50]]]),
    "volcano" : Biome([[10, 10], 2, [0.02, 0], [["tree", 50], ["bush", 50], ["vine", 5], ["lily", 20], ["wildgrass", 10]], [["volcano", 1]]]),
    "ocean" : Biome([[10, 10], 0.5, [0.9, 0.05], []]),
}

