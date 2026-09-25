from realm import Realm
import realm_settings
from spatialhash import SpatialHash
import random


random.seed(60309)

def test_world_generation():
    realm = Realm(*realm_settings.default_realm_settings)
    assert realm.width > 0
    assert realm.height > 0
    assert realm.check_grass() > 0
    assert realm.check_water() > 0
    assert realm.check_ice() > 0
    assert any('tree' in row for row in realm.environment)
    assert len(realm.elements[0]) > 0
    assert len(realm.elements[1]) > 0
    assert type(realm.spatialhash) == SpatialHash

def test_water_generation():
    realm = Realm(*realm_settings.default_realm_settings)
    realm._Realm__generate_water()
    assert realm.check_water() > realm.wetness 

def test_ice_generation():
    realm = Realm(*realm_settings.default_realm_settings)
    realm._Realm__generate_ice()
    assert realm.check_ice() > realm.iceness

def test_flora_generation():
    default_temp = realm_settings.flora_factor
    realm_settings.default_realm_settings[6] = realm_settings.generate_flora(0, 1)
    realm = Realm(*realm_settings.default_realm_settings)
    assert len(realm.elements[0]) == realm_settings.default_tree_count
    realm_settings.default_realm_settings[6] = realm_settings.generate_flora(2, 1)
    realm = Realm(*realm_settings.default_realm_settings)
    assert len(realm.elements[0]) > realm_settings.default_tree_count
    ealm_settings.default_realm_settings[6] = realm_settings.generate_flora(default_temp, 1)
