import json, unittest
from pyjsonable import StrictDict

# To run:
# $ python -m unittest test_pyjsonable

class PyJasonTestBase( unittest.TestCase ):
    def _test_json_dumps(self, strict_dict):
        strict_dict_jsoned =  json.loads(json.dumps(strict_dict))
        self.assertDictEqual(strict_dict_jsoned, strict_dict)

class StrictDictTests( PyJasonTestBase ):

    def _init_with_literal(self):
        house_dict = StrictDict({
            "type": "bungalow",
            "floors": 1,
            "trees": ["birch", "maple", "oak"]
        })
        return house_dict

    def _init_with_kwargs(self):
        house_dict = StrictDict(
            type="bungalow",
            floors=1,
            trees=["birch", "maple", "oak"]
        )
        return house_dict

    def _update_with_literal(self, house_dict):
        house_dict.update({
            "floors":2,
            "windows":{
                "front": 7,
                "back": 9
            },
            "rooms": StrictDict(
                bathroom=2,
                bedroom=6,
                kitchen=2
            )
        })
        return house_dict

    def _update_with_kwargs(self, house_dict):
        house_dict.update(
            floors=2,
            windows=dict(front=7,back=9),
            rooms=StrictDict({
                "bathroom": 2,
                "bedroom": 6,
                "kitchen": 2
            })
        )
        return house_dict

    def _test_after_init(self, house_dict):
        self.assertEqual(house_dict.get("type"), "bungalow")
        self.assertEqual(house_dict.type, "bungalow")
        self.assertEqual(house_dict.get("floors"), 1)
        self.assertEqual(house_dict.floors, 1)
        expected_trees_array = ["birch", "maple", "oak"]
        self.assertItemsEqual(house_dict.get("trees"), expected_trees_array)
        self.assertItemsEqual(house_dict.trees, expected_trees_array)

    def _test_after_update(self, house_dict):
        self.assertEqual(house_dict.get("floors"), 2)
        self.assertEqual(house_dict.floors, 2)
        self.assertEqual(house_dict.get("windows").get("front"), 7)
        self.assertEqual(house_dict.get("windows").get("back"), 9)
        self.assertEqual(house_dict.get("rooms").get("bathroom"), 2)
        self.assertEqual(house_dict.get("rooms").get("bedroom"), 6)
        self.assertEqual(house_dict.get("rooms").get("kitchen"), 2)
        self.assertEqual(house_dict.get("rooms").bathroom, 2)
        self.assertEqual(house_dict.get("rooms").bedroom, 6)
        self.assertEqual(house_dict.get("rooms").kitchen, 2)

    def test_init_with_literal_update_with_literal(self):
        house_dict = self._init_with_literal()
        self._test_after_init(house_dict)
        self._update_with_literal(house_dict)
        self._test_after_update(house_dict)
        self._test_json_dumps(house_dict)

    def test_init_with_literal_update_with_kwargs(self):
        house_dict = self._init_with_literal()
        self._test_after_init(house_dict)
        self._update_with_kwargs(house_dict)
        self._test_after_update(house_dict)
        self._test_json_dumps(house_dict)

    def test_init_with_kwargs_update_with_literal(self):
        house_dict = self._init_with_kwargs()
        self._test_after_init(house_dict)
        self._update_with_literal(house_dict)
        self._test_after_update(house_dict)
        self._test_json_dumps(house_dict)

    def test_init_with_kwargs_update_with_kwargs(self):
        house_dict = self._init_with_kwargs()
        self._test_after_init(house_dict)
        self._update_with_kwargs(house_dict)
        self._test_after_update(house_dict)
        self._test_json_dumps(house_dict)

    def test_meta_no_extend(self):
        plain_dict = StrictDict(foo="bar")
        self.assertFalse(plain_dict.Meta.required_keys)
        self.assertFalse(plain_dict.Meta.at_least_one_required_keys)
        self.assertFalse(plain_dict.Meta.cannot_coexist_keys)
        self.assertFalse(plain_dict.Meta.allowed_keys)

class StrictDictExtendTests( PyJasonTestBase ):
    def test_valid_init(self):
        cake = CakeDict(
            type="birthday",
            is_vegan=False,
            color="red",
            num_layers=5
        )
        cake.validate()
        self._test_json_dumps(cake)

    def test_missing_required_keys(self):
        cake = CakeDict(
            # type="birthday",
            # is_vegan=False,
            color="red",
            num_layers=5
        )
        with self.assertRaises(AttributeError):
            cake.validate()
        cake.is_vegan = False
        with self.assertRaises(AttributeError):
            cake.validate()
        cake.type="birthday"
        cake.validate()
        self._test_json_dumps(cake)

    def test_missing_at_least_one_required_key(self):
        cake = CakeDict(
            type="birthday",
            is_vegan=False,
            # color="red",
            num_layers=5,
            milk_type="2%"
        )
        with self.assertRaises(AttributeError):
            cake.validate()
        cake.color = "red"
        cake.validate()
        self._test_json_dumps(cake)
        cake.hue = "scarlet"
        cake.validate()
        self._test_json_dumps(cake)

    def test_violate_cannot_coexist(self):
        cake = CakeDict(
            type="birthday",
            is_vegan=False,
            color="red",
            num_layers=5,
            milk_type="2%",
            vegan_milk_type="almond"
        )
        with self.assertRaises(AttributeError):
            cake.validate()
        cake.pop("vegan_milk_type")
        cake.validate()
        self._test_json_dumps(cake)

    def test_violate_allowed_keys(self):
        cake = CakeDict(
            type="birthday",
            is_vegan=False,
            color="red",
            num_layers=5,
            milk_type="2%",
            wack_key="i am not allowed"
        )
        with self.assertRaises(AttributeError):
            cake.validate()
        cake.pop("wack_key")
        cake.validate()
        self._test_json_dumps(cake)

#
# Test objects
#
class CakeDict( StrictDict ):
    class Meta:
        required_keys={"type", "is_vegan"}
        at_least_one_required_keys={"color", "hue"}
        cannot_coexist_keys={"milk_type", "vegan_milk_type"}
        allowed_keys={"num_layers", "cups_sugar"}
