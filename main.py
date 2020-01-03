#!/bin/python

from typing import Union, Tuple, List
import json


with open("conversions.json", "r") as f:
    conversion_table = json.load(f)


def unit_type(unit: str) -> Union[str, None]:
    for i in conversion_table:
        if unit in conversion_table[i]["conversions"]:
            return i

    # Return None if not found
    return None


def is_same_type(a: str, b: str) -> bool:
    return unit_type(a) == unit_type(b)


def convert(a: str, b: str, value: Union[int, float]) -> Union[int, float]:
    if not is_same_type(a, b):
        raise Exception("Cannot convert different types of units")
    if a == b:
        # Same unit, so no conversion needed
        return value

    base_unit_ratio: float = conversion_table[unit_type(a)]["conversions"][a]
    target_unit_ratio: float = conversion_table[unit_type(b)]["conversions"][b]

    # Temperature gets its own section, because it includes
    # addition/subtraction and a specific ratio for fahrenheit
    if unit_type(a) == "temperature":
        to_celsius: float
        if a == "celsius":
            to_celsius = value
        elif a == "fahrenheit":
            # [C] = ([F] Ã¢Ë†â€™ ratio) * (5/9)
            to_celsius = (value - base_unit_ratio) * (5/9)
        elif a == "kelvin":
            # [C] = [K] − ratio
            to_celsius = value - base_unit_ratio

        if b == "celsius":
            return to_celsius
        elif b == "fahrenheit":
            # [F] = [C] * (9/5) + ratio
            return to_celsius * 1.8 + target_unit_ratio
        elif b == "kelvin":
            # [K] = [C] + ratio
            return to_celsius + target_unit_ratio

    return value / base_unit_ratio * target_unit_ratio


def convertf(a: str, b: str, value: Union[int, float]) -> str:
    return f"{value} {a} is {convert(a, b, value)} {b}"


def parse_string(input: str) -> Tuple[str, str, float]:
    if "to" in input:
        split_input: str = input.split(" to ")
    if "in" in input:
        split_input: str = input.split(" in ")

    # Remove trailing whitespaces with .strip()
    split_input: List[str] = [i.strip() for i in split_input]

    # The value and base unit are in split_input[0],
    # so we need to split them into individual variables
    value: float = float(split_input[0].split(" ")[0])
    base_unit: str = " ".join(split_input[0].split(" ")[1:])
    target_unit: str = split_input[1]

    return (base_unit, target_unit, value)


if __name__ == "__main__":
    while True:
        try:
            print(convertf(*parse_string(input("> "))))
        except KeyboardInterrupt:
            break
