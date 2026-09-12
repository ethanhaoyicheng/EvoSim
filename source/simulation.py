class Simulation: 

    def __init__(self): 
        self.realms = [] 
        self.vis_realms = []
        self.time = 0 

    def add_realm(self, newRealm): 
        self.realms.append(newRealm) 
    
    def add_vis_realm(self, newRealm): 
        self.vis_realms.append(newRealm) 

    def tick(self): 
        #increment time for all realms 

        for realm in self.realms: 
            realm.tick() 
        for vis_realm in self.vis_realms:
            vis_realm.tick()

        self.time += 1 

    def tock(self, realmName): 
        #increment time for a specific world 
        for realm in self.realms: 
            if realm.name == realmName: 
                realm.tick() 
        for v in self.vis_realms: 
            if v.realm.name == realmName: 
                v.tick()

 