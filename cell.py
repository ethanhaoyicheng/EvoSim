from math import sqrt
from angle import atan2
from world_facts import terrain_index

#anima
SEARCH_RANGE_LIMIT = 80

class Cell:
    def __init__(self, realm, spawnx, spawny):
        self.realm = realm
        self.x = spawnx
        self.y = spawny
        self.bucket = -1
    
    def distance_x(self, x):
        rw = self.realm.width

        if self.x - x > rw/2:
            sx = self.x - rw
        elif x - self.x > rw/2:
            sx = self.x + rw
        else:
            sx = self.x
        return abs(sx - x)

    def distance_y(self, y):
        rh = self.realm.height

        if self.y - y > rh/2:
            sy = self.y - rh
        elif y - self.y > rh/2:
            sy = self.y + rh
        else:
            sy = self.y

        return abs(sy-y)

    def displacement_x(self, x):
        rw = self.realm.width

        if self.x - x > rw/2:
            sx = self.x - rw
        elif x - self.x > rw/2:
            sx = self.x + rw
        else:
            sx = self.x
        return x - sx

    def displacement_y(self, y):
        rh = self.realm.height

        if self.y - y > rh/2:
            sy = self.y - rh
        elif y - self.y > rh/2:
            sy = self.y + rh
        else:
            sy = self.y

        return y - sy

    def distance_to(self, object):
        if isinstance(object, Cell):
            return self.distance_to_point(object.x, object.y)
        if isinstance(object, tuple):
            return self.distance_to_point(object[0],object[1])
        return None

    def distance_to_point(self, x, y):          #can be private
        return sqrt((self.displacement_x(x))**2 + (self.displacement_y(y))**2)

    def distance_to_nearest_a(self, element):   #fail: return the limit of the search (int)
        if isinstance(element, int):
            dist = 1
            terrain = terrain_index[element]
            while dist <= SEARCH_RANGE_LIMIT:
                for row in range((self.y - dist)%self.realm.height, (self.y + dist + 1)%self.realm.height):
                    for col in range((self.x - dist)%self.realm.width, (self.x + dist + 1)%self.realm.width):
                        if self.distance_to((col, row)) <= dist and self.realm.environment[row % self.realm.height][col % self.realm.width] == terrain:
                            return dist
                dist += 1
            return SEARCH_RANGE_LIMIT
    
    def distance_to_nearest_n(self, element):   #fail: return None
        if isinstance(element, int):
            dist = 1
            terrain = self.realm.terrain_index[element]
            while dist <= SEARCH_RANGE_LIMIT:
                for row in range((self.y - dist)%self.realm.height, (self.y + dist + 1)%self.realm.height):
                    for col in range((self.x - dist)%self.realm.width, (self.x + dist + 1)%self.realm.width):
                        if self.distance_to((col, row)) <= dist and self.realm.environment[row % self.realm.height][col % self.realm.width] == terrain:
                            return dist
                dist += 1
            return None
        
        """instead:for pos in self.cells_to_check:
            if self.realm.environment[pos[0]][pos[1]] == "water":
                dist = self.distance_to_point(pos[1], pos[0])
                if min(dist, nearest_dist, self.vision) == dist:    #vision for emergency clamping
                    nearest_dist = dist
                    nearest_water = (pos[0],pos[1])"""
            
    
    
    def is_within(self, object, radius):
        if isinstance(object, Cell):
            if self.distance_to(object) <= radius:
                return True
            return False
        if isinstance(object, tuple):
            if self.is_within_point(object[0],object[1],radius):
                return True
            return False
        return None
        
    def is_within_point(self, x, y, radius):
        if  self.distance_to_point(x, y) <= radius:
            return True
        return False
    
    def angle_to(self, object):
        if isinstance(object, Cell):
            return atan2(self.displacement_y(object.y), self.displacement_x(object.x))
        if isinstance(object, tuple):
            return atan2(self.displacement_y(object[1]), self.displacement_x(object[0]))

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    """def provide(self, _=None):
        return 0 or "ERROR"""

    def reproduce(self):
        pass

    def end(self):
        del self

    




    

