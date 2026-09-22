from spatialhash import SpatialHash
import random

random.seed(60309)

class DummyAnima:
    def __init__(self, rangex = 100, rangey = 100):
        self.x = random.randint(0,rangex)
        self.y = random.randint(0,rangey)

def set_extreme_values(dummyList):
    dummyList[0].x = 0
    dummyList[0].y = 0
    dummyList[1].x = 1
    dummyList[1].y = 1
    dummyList[2].x = 0
    dummyList[2].y = 100
    dummyList[3].x = 0
    dummyList[3].y = 99
    dummyList[4].x = 99
    dummyList[4].y = 99
    dummyList[5].x = 99
    dummyList[5].y = 100
    dummyList[6].x = 100
    dummyList[6].y = 100


def test_spatial_hash_consistency_origin():
    #assert that animas have a single guaranteed identity* within the spatial hash
    sh = SpatialHash(20, 100, 100)
    
    dummyList = [DummyAnima(100, 100) for i in range(100)]
    set_extreme_values(dummyList)

    for dummy in dummyList:
        sh.add_element(dummy)

    for dummy in dummyList:
        assert dummy in sh.buckets[dummy.__get_hash(dummy.x, dummy.y)

    bucketNo = 0
    for bucket in sh.buckets:
        for dummy in bucket:
            assert dummy.bucket == bucketNo
        bucketNo += 1

    

def test_spatial_hash_consistency_through():
    #test consistency after updating
    sh = SpatialHash(20, 100, 100)
    
    dummyList = [DummyAnima(100, 100) for i in range(100)]
    set_extreme_values(dummyList)

    for dummy in dummyList:
        sh.add_element(dummy)
        
    for dummy in dummyList:
        dummy.x = random.randint(0,100)
        dummy.y = random.randint(0,100)
        sh.update_element(dummy)
        
    for dummy in dummyList:
        assert dummy in sh.buckets[dummy.__get_hash(dummy.x, dummy.y)

    totalAnima = 0
    for bucket in sh.buckets:
        bucketNo = 0
        for dummy in bucket:
            assert dummy.bucket == bucketNo
        bucketNo += 1

        totalAnima += len(bucket)
    assert totalAnima == 100



def test_bucket_adjacency_symmetry():
    #assert that adjacency is symmetric
    
    sh = SpatialHash(20, 100, 100)
    
    dummyList = [DummyAnima(100, 100) for i in range(100)]
    set_extreme_values(dummyList)
    for dummy in dummyList:
        sh.add_element(dummy)

    #test for visions of up to 3x cell size (arbitrary)
    for radius in range(3):
        for dummy in dummyList:
            for friend in sh.get_neighbours(dummy.x, dummy.y, radius):
                assert dummy in fsh.get_neighbours(friend.x, friend.y, radius)
            
def test_spatial_hash_emptinesss():
    #test that empty hash is truly empty
    sh = SpatialHash(20, 100, 100)

    for bucket in sh.buckets:
        assert len(buckets) == 0
    
def test_element_removal():
    #test that remove_element correctly removes only the specified element
    sh = SpatialHash(20, 100, 100)
    dummy = DummyAnima()
    sh.add_element(dummy)
    friend = DummyAnima()
    friend.x = dummy.x
    friend.y = dummy.y
    sh.add_element(friend)
    assert dummy in sh.buckets[sh.__get_hash(dummy.x, dummy.y)]
    assert friend in sh.buckets[sh.__get_hash(dummy.x, dummy.y)]
    sh.remove_element(dummy)
    assert element not in sh.buckets[sh.__get_hash(dummy.x, dummy.y)]
    assert friend in sh.buckets[sh.__get_hash(dummy.x, dummy.y)]
    

def test_radius_correctness():
    #tests for accuracy of spatial hash range check
    sh = SpatialHash(20, 100, 100)
    dummy = DummyAnima()
    sh.add_element(dummy)
    friend = DummyAnima()
    dummy.x = 0
    dummy.y = 0
    friend.x = 39
    friend.y = 39
    assert friend in sh.get_neighbours(dummy.x, dummy.y, 21)
    
    

def test_no_duplicate_entries():
    #checks that the same element only appears once in hash
    sh = SpatialHash(20, 100, 100)
    dummy = DummyAnima()
    sh.add_element(dummy)
    sh.update_element(dummy)
    sh.add_element(dummy)
    
    assert len(sh.buckets[sh.__get_hash(dummy.x, dummy.y)]) == 1
