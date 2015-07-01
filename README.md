pyjsonable
==========

Native, validatable python objects ready for json serialization

# Example Usage

```python

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

cake = CakedDictTyped(
    type="birthday",
    is_vegan=False,
    cups_sugar=5,
    decorations=["sprinkles"]
    frosting=FrostingDict(å
        cups_milk=4,
        cups_powdered_sugar=7
    )
)

print json.dumps(cake, indent=3)
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
```