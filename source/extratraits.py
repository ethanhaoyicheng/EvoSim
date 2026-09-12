import random

class ExtraTraits():
    def __init__(self, trait_set):
        self.traits = trait_set

    def __iter__(self):
        return iter(self.traits)
    
    def __contains__(self, trait):
        return trait in self.traits
    
    def __len__(self):
        return len(self.traits)
    
    def __str__(self):
        return str(self.traits)
    
    def __bool__(self):
        return bool(self.traits)

    def add(self, trait):
        self.traits.add(trait)
    
    def extend(self, traits):
        self.traits = set(list(self.traits) + list(traits)) #could also use union but this ensures works with both list and set of traits

    def correct_traits(self):
        attacks = list(self.traits & attack_set)

        while len(attacks) > 1:
            cull = random.choice(attacks)
            self.traits.remove(cull)
            attacks.remove(cull)
    
    def attack(self):
        return [attack for attack in attack_set if attack in self.traits]


attack_set = {"claws", "pincers", "venomous", "sand-attack", "mimic-attack"}

trait_costs = {
    "egg-laying" : 0,
    "claws" : 0.2,
    "flippers" : 0.2,
    "abrupt-wanderer" : 0,
    "poisonous" : 0.1,
    "venomous" : 0.2,
    "pincers" : 0.2,
    "snowycloak" : 0,
    "strong-gut" : 0.1,
    "sand-attack" : 0.2,
    "spiritful-child" : 0.1,
    "inky-shot" : 0.2,
    "berserker" : 0.05,
    "vampirism" : 0.1,
    "zombie" : 0,
    "gluttonous-child" : 0,
    "necro-mimicry" : 0,
    "absorb-victim" : 0.15,
    "mimic-attack" : 0.15,
    "leviathan" : 0,
    "play-dead" : 0,
    "plate-armour" : 0.4,
    "growth-syndrome" : 0,
}
        

