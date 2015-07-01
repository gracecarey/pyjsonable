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

class StrictDictValidateTests( PyJasonTestBase ):
    def test_valid_init(self):
        cake = CakeDict(
            type="birthday",
            is_vegan=False,
            color="red",
            num_layers=5
        )
        self._test_json_dumps(cake)

    def test_missing_required_keys(self):
        with self.assertRaises( AttributeError ):
            CakeDict(
                # type="birthday", <-- missing required
                # is_vegan=False, <-- missing required
                color="red",
                num_layers=5
            )

    def test_missing_at_least_one_required_key(self):
        with self.assertRaises( AttributeError ):
            CakeDict(
                type="birthday",
                is_vegan=False,
                # color="red", <-- missing at_least_one_required
                num_layers=5,
                milk_type="2%"
            )

    def test_violate_cannot_coexist(self):
        with self.assertRaises(AttributeError):
            CakeDict(
                type="birthday",
                is_vegan=False,
                color="red",
                num_layers=5,
                milk_type="2%",  # <-- cannot coexist
                vegan_milk_type="almond"  # <-- cannot coexist
            )

    def test_violate_allowed_keys(self):
        with self.assertRaises(AttributeError):
            CakeDict(
                type="birthday",
                is_vegan=False,
                color="red",
                num_layers=5,
                milk_type="2%",
                wack_key="i am not allowed" # <-- key not among allowed
            )

    def test_cake_dict_only_required_keys(self):
        with self.assertRaises(AttributeError):
            CakeDictRequired({
                "type": "some type"
            })
        cake = CakeDictRequired({
            "type": "some type",
            "is_vegan": True
        })
        self._test_json_dumps(cake)

    def test_cake_dict_only_atleastone_keys(self):
        with self.assertRaises(AttributeError):
            CakeDictAtLeastOne()
        cake = CakeDictAtLeastOne({
            "hue": "blue",
            "color": "a color"
        })
        self._test_json_dumps(cake)

    def test_cake_dict_only_cannotcoexist_keys(self):
        with self.assertRaises(AttributeError):
            CakeDictCannotCoexist(
                type="birthday",
                is_vegan=False,
                color="red",
                num_layers=5,
                milk_type="2%", # <-- cannot coexist
                vegan_milk_type="almond" # <-- cannot coexist
            )
        cake = CakeDictCannotCoexist(
            type="birthday",
            is_vegan=False,
            color="red",
            num_layers=5,
            milk_type="2%",
        )
        self._test_json_dumps(cake)
        with self.assertRaises(AttributeError):
            cake.vegan_milk_type = "almond" # <-- cannot coexist

    def test_cake_dict_only_allowed_keys(self):
        with self.assertRaises(AttributeError):
            CakeDictAllowed(
                wack_attr="i am not allowed",
                num_layers=5,
            )
        cake = CakeDictAllowed(
            num_layers=5,
        )
        cake["cups_sugar"]=100
        self._test_json_dumps(cake)
        with self.assertRaises(AttributeError):
            cake.wack_attr = "no!"
        with self.assertRaises(AttributeError):
            cake["wack_attr"] = "no bad!"
    """
    {
       "frosting": {
          "cups_milk": 4,
          "cups_powdered_sugar": 7
       },
       "type": "birthday",
       "cups_sugar": 5,
       "decorations": [
          "sprinkles"
       ],
       "is_vegan": false
    }
    """
class StrictDictTypeMapTests( PyJasonTestBase ):
    def test_valid_typed(self):
        cake = CakedDictTyped(
            type="birthday",
            is_vegan=False,
            cups_sugar=5,
            decorations=["sprinkles"],
            frosting=FrostingDict(
                cups_milk=4,
                cups_powdered_sugar=7
            )
        )
        print json.dumps(cake, indent=3)
        self._test_json_dumps(cake)

    def test_invalid_typed(self):
        with self.assertRaises( TypeError ):
            CakedDictTyped(
                cups_sugar="FIVE", # <-- invalid
                type="birthday",
                is_vegan=False,
                frosting=FrostingDict(
                    cups_milk=4,
                    cups_powdered_sugar=7
                )
            )
        with self.assertRaises( TypeError ):
            FrostingDict(
                cups_milk="SEVEN",
                cups_powdered_sugar=10,
            )
        with self.assertRaises( TypeError ):
            CakedDictTyped(
                cups_sugar=5,
                is_vegan=False,
                type="birthday",
                frosting=FrostingDict(
                    cups_milk="SEVEN",
                    cups_powdered_sugar=10,
                )
            )
        with self.assertRaises( AttributeError ):
            CakedDictTyped(
                cups_sugar=5,
                # is_vegan=False, <-- Missing required
                # type="birthday",<-- Missing required
                frosting=None
            )

    def test_invalid_update_with_kwargs(self):
        cake = CakedDictTyped(
            type="birthday",
            is_vegan=False,
            frosting=FrostingDict(
                cups_milk=4,
                cups_powdered_sugar=7
            )
        )
        self._test_json_dumps(cake)
        with self.assertRaises( TypeError ):
            cake.update(is_vegan="not a bool!")

    def test_invalid_update_with_literal(self):
        cake = CakedDictTyped(
            type="birthday",
            is_vegan=True,
            frosting=FrostingDict(
                cups_milk=4,
                cups_powdered_sugar=7
            )
        )
        with self.assertRaises( TypeError ):
            cake.update({
                "is_vegan":"notbool!", # <-- invalid
                "decorations": "sprinkles"
            })
        cake.update({
            "is_vegan":True,
            "decorations": "sprinkles"
        })
        self._test_json_dumps(cake)

    def test_nullable_type(self):
        cake = CakedDictTyped(
            type="birthday",
            is_vegan=True,
        )
        cake.frosting = None
        self._test_json_dumps(cake)
        with self.assertRaises( TypeError ):
            cake.update(is_vegan="notbool!")
#
# Test objects
#
class CakeDictRequired( StrictDict ):
    class Meta:
        required_keys={"type", "is_vegan"}

class CakeDictAtLeastOne( StrictDict ):
    class Meta:
        at_least_one_required_keys={"color", "hue", "shade"}

class CakeDictCannotCoexist( StrictDict ):
    class Meta:
        cannot_coexist_keys={"milk_type", "vegan_milk_type"}

class CakeDictAllowed( StrictDict ):
    class Meta:
        allowed_keys={"num_layers", "cups_sugar"}

class CakeDict( StrictDict ):
    class Meta:
        required_keys={"type", "is_vegan"}
        at_least_one_required_keys={"color", "hue"}
        cannot_coexist_keys={"milk_type", "vegan_milk_type"}
        allowed_keys={"num_layers", "cups_sugar"}

class FrostingDict( StrictDict ):
    class Meta:
        required_keys={"cups_powdered_sugar"}
        type_map={
            "cups_milk": {
                "type": int
            },
        }
class CakedDictTyped( CakeDict ):
    class Meta:
        required_keys={"type", "is_vegan"}
        allowed_keys={"num_layers", "cups_sugar", "frosting", "decorations"}
        type_map={
            "cups_sugar": int,
            "is_vegan": bool,
            "num_layers": {
                "type": int,
            },
            "frosting": {
                "type":FrostingDict,
                "nullable":True,
            }
        }