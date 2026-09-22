class SpatialHash:
    def __init__(self, cell_size, world_width, world_height):       #called world. not realm
        self.width = int((world_width-1) / cell_size) + 1
        self.height = int((world_height-1) / cell_size) + 1
        self.unit = cell_size
        self.buckets = [[] for _0 in range(self.width * self.height)]
    
    def __get_hash(self, x, y):
        return int(x//self.unit) + int((y//self.unit)*self.width)
    
    def get_neighbours(self, x, y, radius):         #WRAP AROUND REALM??
        r = int((radius-0.000001)/self.unit) + 1

        my_bucket = self.__get_hash(x, y)
        neighbour_list = []
        for i in range(-r, r+1):
            for j in range(-r, r+1):
                bucket_to_check = ((my_bucket%self.width + i)%self.width) + ((int(my_bucket/self.width)+j) % self.height) * self.width
                #if bucket_to_check >= 0 and bucket_to_check < len(self.buckets) and not (i==-1 and my_bucket % self.width == 0) and not (i==1 and (my_bucket+1) % self.width == 0):
                neighbour_list.extend(self.buckets[bucket_to_check])
        return neighbour_list

    def add_element(self, element):
        if element.bucket == -1:
            bucket = self.__get_hash(element.x, element.y)
            self.buckets[bucket].append(element)
            element.bucket = bucket
            return True
        return False
    
    def remove_element(self, element):
        bucket = element.bucket
        #print(element.bucket)
        #print([b for b in range(self.width * self.height) if element in self.buckets[b]])
        self.buckets[bucket].remove(element)

    def update_element(self, element):
        if not self.add_element(element):
            
        #skip exception for flora?
            current_b = self.__get_hash(element.x, element.y)
            prev_b = element.bucket
            if current_b != prev_b:
                if prev_b >= 0:
                    self.buckets[prev_b].remove(element)
                self.buckets[current_b].append(element)
                element.bucket = current_b
    
    #tick


    def tock(self, element_list):
        for element in element_list:
            self.update_element(element)
