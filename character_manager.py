"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: Lauren Roberson

AI Usage: [Document any AI assistance used]

This module handles character creation, loading, and saving.
"""

import os
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError
)

# ============================================================================
# CHARACTER MANAGEMENT FUNCTIONS
# ============================================================================

def create_character(name, character_class):
    """
    Create a new character with stats based on class
    
    Valid classes: Warrior, Mage, Rogue, Cleric
    
    Returns: Dictionary with character data including:
            - name, class, level, health, max_health, strength, magic
            - experience, gold, inventory, active_quests, completed_quests
    
    Raises: InvalidCharacterClassError if class is not valid
    """
    valid_classes = ["Warrior", "Mage", "Rogue", "Cleric"]
    if character_class not in valid_classes:
        raise InvalidCharacterClassError(f"Invalid character class: {character_class}")

    # Base stats
    if character_class == "Warrior":
        health = 120; strength = 15; magic = 5
    elif character_class == "Mage":
        health = 80; strength = 8; magic = 20
    elif character_class == "Rogue":
        health = 90; strength = 12; magic = 10
    elif character_class == "Cleric":
        health = 100; strength = 10; magic = 15

    character = {
        "name": name,
        "class": character_class,
        "level": 1,
        "health": health,
        "max_health": health,
        "strength": strength,
        "magic": magic,
        "experience": 0,
        "gold": 100,
        "inventory": [],
        "active_quests": [],
        "completed_quests": []
    }

    return character


def save_character(character, save_directory="data/save_games"):
    """
    Save character to file
    """
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    filename = f"{character['name']}_save.txt"
    filepath = os.path.join(save_directory, filename)

    inventory_str = ",".join(character.get("inventory", []))
    active_str = ",".join(character.get("active_quests", []))
    completed_str = ",".join(character.get("completed_quests", []))

    with open(filepath, "w") as f:
        f.write(f"NAME: {character['name']}\n")
        f.write(f"CLASS: {character['class']}\n")
        f.write(f"LEVEL: {character['level']}\n")
        f.write(f"HEALTH: {character['health']}\n")
        f.write(f"MAX_HEALTH: {character['max_health']}\n")
        f.write(f"STRENGTH: {character['strength']}\n")
        f.write(f"MAGIC: {character['magic']}\n")
        f.write(f"EXPERIENCE: {character['experience']}\n")
        f.write(f"GOLD: {character['gold']}\n")
        f.write(f"INVENTORY: {inventory_str}\n")
        f.write(f"ACTIVE_QUESTS: {active_str}\n")
        f.write(f"COMPLETED_QUESTS: {completed_str}\n")

    return True


def load_character(character_name, save_directory="data/save_games"):
    """
    Load character from save file
    """
    filename = f"{character_name}_save.txt"
    filepath = os.path.join(save_directory, filename)

    if not os.path.exists(filepath):
        raise CharacterNotFoundError(f"Character save file not found: {character_name}")

    try:
        with open(filepath, "r") as f:
            lines = f.readlines()
    except OSError as e:
        raise SaveFileCorruptedError(f"Error reading save file: {e}")

    data = {}

    try:
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if ": " not in line:
                raise InvalidSaveDataError(f"Invalid line format: {line}")

            key, value = line.split(": ", 1)
            key = key.strip().upper()
            value = value.strip()

            if key == "NAME":
                data["name"] = value
            elif key == "CLASS":
                data["class"] = value
            elif key == "LEVEL":
                data["level"] = int(value)
            elif key == "HEALTH":
                data["health"] = int(value)
            elif key == "MAX_HEALTH":
                data["max_health"] = int(value)
            elif key == "STRENGTH":
                data["strength"] = int(value)
            elif key == "MAGIC":
                data["magic"] = int(value)
            elif key == "EXPERIENCE":
                data["experience"] = int(value)
            elif key == "GOLD":
                data["gold"] = int(value)
            elif key == "INVENTORY":
                data["inventory"] = [x for x in value.split(",") if x] if value else []
            elif key == "ACTIVE_QUESTS":
                data["active_quests"] = [x for x in value.split(",") if x] if value else []
            elif key == "COMPLETED_QUESTS":
                data["completed_quests"] = [x for x in value.split(",") if x] if value else []
            else:
                # Unknown fields are ignored to avoid breaking tests
                continue

        validate_character_data(data)

    except ValueError as e:
        raise InvalidSaveDataError(f"Invalid numeric value: {e}")
    except InvalidSaveDataError:
        raise

    return data


def list_saved_characters(save_directory="data/save_games"):
    """
    Return list of saved character names
    """
    if not os.path.exists(save_directory):
        return []

    result = []
    for file in os.listdir(save_directory):
        if file.endswith("_save.txt"):
            result.append(file[:-9])

    return result


def delete_character(character_name, save_directory="data/save_games"):
    """
    Delete a saved character
    """
    filepath = os.path.join(save_directory, f"{character_name}_save.txt")

    if not os.path.exists(filepath):
        raise CharacterNotFoundError(f"Character not found: {character_name}")

    os.remove(filepath)
    return True

# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    """
    Add experience and handle level-ups
    """
    if is_character_dead(character):
        raise CharacterDeadError("Dead characters cannot gain experience")

    character["experience"] += xp_amount

    leveled_up = False
    while character["experience"] >= character["level"] * 100:
        requirement = character["level"] * 100
        character["experience"] -= requirement
        character["level"] += 1
        character["max_health"] += 10
        character["strength"] += 2
        character["magic"] += 2
        character["health"] = character["max_health"]
        leveled_up = True

    return leveled_up


def add_gold(character, amount):
    """
    Add or subtract gold
    """
    new_total = character["gold"] + amount
    if new_total < 0:
        raise ValueError("Gold cannot be negative")

    character["gold"] = new_total
    return new_total


def heal_character(character, amount):
    """
    Heal character
    """
    if amount <= 0:
        return 0

    missing = character["max_health"] - character["health"]
    if missing <= 0:
        return 0

    heal_amount = min(amount, missing)
    character["health"] += heal_amount
    return heal_amount


def is_character_dead(character):
    """Check if character is dead"""
    return character.get("health", 0) <= 0


def revive_character(character):
    """Revive character to 50% HP"""
    if not is_character_dead(character):
        return False

    half = max(1, character["max_health"] // 2)
    character["health"] = half
    return True

# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
    """
    Validate character save data
    """
    required = [
        "name", "class", "level", "health", "max_health",
        "strength", "magic", "experience", "gold",
        "inventory", "active_quests", "completed_quests"
    ]

    for field in required:
        if field not in character:
            raise InvalidSaveDataError(f"Missing field: {field}")

    int_fields = [
        "level", "health", "max_health", "strength",
        "magic", "experience", "gold"
    ]

    for field in int_fields:
        if not isinstance(character[field], int):
            raise InvalidSaveDataError(f"Field '{field}' must be an integer")

    list_fields = ["inventory", "active_quests", "completed_quests"]
    for field in list_fields:
        if not isinstance(character[field], list):
            raise InvalidSaveDataError(f"Field '{field}' must be a list")

    return True

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")
