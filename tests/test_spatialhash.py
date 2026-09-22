from spatialhash import SpatialHash
import random

random.seed(60309)

class DummyAnima:
    def __init__(self, rangex = 100, rangey = 100):
        self.x = random.randint(0,rangex-1)
        self.y = random.randint(0,rangey-1)
        self.bucket = -1

def set_extreme_values(dummyList):
    dummyList[0].x = 0
    dummyList[0].y = 0
    dummyList[1].x = 1
    dummyList[1].y = 1
    dummyList[2].x = 0
    dummyList[2].y = 1
    dummyList[3].x = 0
    dummyList[3].y = 99
    dummyList[4].x = 99
    dummyList[4].y = 99
    dummyList[5].x = 1
    dummyList[5].y = 99
    dummyList[6].x = 99.9
    dummyList[6].y = 99.9


def test_spatial_hash_consistency_origin():
    #assert that animas have a single guaranteed identity* within the spatial hash
    sh = SpatialHash(20, 100, 100)
    
    dummyList = [DummyAnima(100, 100) for i in range(100)]
    set_extreme_values(dummyList)

    for dummy in dummyList:
        sh.add_element(dummy)

    for dummy in dummyList:
        ebucket = int(dummy.x // sh.unit) + int((dummy.y // sh.unit) * sh.width)
        assert dummy in sh.buckets[ebucket]

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
        dummy.x = random.randint(0,99)
        dummy.y = random.randint(0,99)
        sh.update_element(dummy)
        
    for dummy in dummyList:
        expected_bucket = int(dummy.x // sh.unit) + int((dummy.y // sh.unit) * sh.width)
        assert dummy in sh.buckets[expected_bucket]

    totalAnima = 0
    bucketNo = 0
    for bucket in sh.buckets:
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
                assert dummy in sh.get_neighbours(friend.x, friend.y, radius)
            
def test_spatial_hash_emptinesss():
    #test that empty hash is truly empty
    sh = SpatialHash(20, 100, 100)

    for bucket in sh.buckets:
        assert len(bucket) == 0
    
def test_element_removal():
    #test that remove_element correctly removes only the specified element
    sh = SpatialHash(20, 100, 100)
    dummy = DummyAnima()
    sh.add_element(dummy)
    friend = DummyAnima()
    friend.x = dummy.x
    friend.y = dummy.y
    sh.add_element(friend)
    expected_bucket = int(dummy.x // sh.unit) + int((dummy.y // sh.unit) * sh.width)
    assert dummy in sh.buckets[expected_bucket]
    assert friend in sh.buckets[expected_bucket]
    sh.remove_element(dummy)
    assert dummy not in sh.buckets[expected_bucket]
    assert friend in sh.buckets[expected_bucket]
    

def test_radius_correctness():
    #tests for accuracy of spatial hash range check
    sh = SpatialHash(20, 100, 100)
    dummy = DummyAnima()
    friend = DummyAnima()
    dummy.x = 0
    dummy.y = 0
    friend.x = 59
    friend.y = 59
    sh.add_element(dummy)
    sh.add_element(friend)
    assert friend in sh.get_neighbours(dummy.x, dummy.y, 21)
    sh.update_element(friend)
    assert not friend in sh.get_neighbours(dummy.x, dummy.y, 20)
    
    

def test_no_duplicate_entries():
    #checks that the same element only appears once in hash
    sh = SpatialHash(20, 100, 100)
    dummy = DummyAnima()
    sh.add_element(dummy)
    sh.update_element(dummy)
    sh.add_element(dummy)

    expected_bucket = int(dummy.x // sh.unit) + int((dummy.y // sh.unit) * sh.width)
    assert len(sh.buckets[expected_bucket]) == 1
