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
    # Validate character_class first
    # Example base stats:
    # Warrior: health=120, strength=15, magic=5
    # Mage: health=80, strength=8, magic=20
    # Rogue: health=90, strength=12, magic=10
    # Cleric: health=100, strength=10, magic=15
    
    # All characters start with:
    # - level=1, experience=0, gold=100
    # - inventory=[], active_quests=[], completed_quests=[]
    
    # Raise InvalidCharacterClassError if class not in valid list
    valid_classes = ["Warrior", "Mage", "Rogue", "Cleric"]
    if character_class not in valid_classes:
        raise InvalidCharacterClassError(f"Invalid character class: {character_class}")

    # Base stats by class
    if character_class == "Warrior":
        health = 120
        strength = 15
        magic = 5
    elif character_class == "Mage":
        health = 80
        strength = 8
        magic = 20
    elif character_class == "Rogue":
        health = 90
        strength = 12
        magic = 10
    elif character_class == "Cleric":
        health = 100
        strength = 10
        magic = 15

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
    
    Filename format: {character_name}_save.txt
    
    File format:
    NAME: character_name
    CLASS: class_name
    LEVEL: 1
    HEALTH: 120
    MAX_HEALTH: 120
    STRENGTH: 15
    MAGIC: 5
    EXPERIENCE: 0
    GOLD: 100
    INVENTORY: item1,item2,item3
    ACTIVE_QUESTS: quest1,quest2
    COMPLETED_QUESTS: quest1,quest2
    
    Returns: True if successful
    Raises: PermissionError, IOError (let them propagate or handle)
    """
    # TODO: Implement save functionality
    # Create save_directory if it doesn't exist
    # Handle any file I/O errors appropriately
    # Lists should be saved as comma-separated values
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    filename = f"{character['name']}_save.txt"
    filepath = os.path.join(save_directory, filename)

    # Prepare list fields as comma-separated strings
    inventory_str = ",".join(character.get("inventory", []))
    active_quests_str = ",".join(character.get("active_quests", []))
    completed_quests_str = ",".join(character.get("completed_quests", []))

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
        f.write(f"ACTIVE_QUESTS: {active_quests_str}\n")
        f.write(f"COMPLETED_QUESTS: {completed_quests_str}\n")

    return True

def load_character(character_name, save_directory="data/save_games"):
    """
    Load character from save file
    
    Args:
        character_name: Name of character to load
        save_directory: Directory containing save files
    
    Returns: Character dictionary
    Raises: 
        CharacterNotFoundError if save file doesn't exist
        SaveFileCorruptedError if file exists but can't be read
        InvalidSaveDataError if data format is wrong
    """
    # TODO: Implement load functionality
    # Check if file exists → CharacterNotFoundError
    # Try to read file → SaveFileCorruptedError
    # Validate data format → InvalidSaveDataError
    # Parse comma-separated lists back into Python lists
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
        for raw_line in lines:
            line = raw_line.strip()
            if not line:
                continue
            # Allow both "FIELD: value" and "FIELD:" formats
            if ":" not in line:
                raise InvalidSaveDataError(f"Invalid line format in save file: {line}")
            key, value = line.split(":", 1)
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
                if value == "":
                    data["inventory"] = []
                else:
                    data["inventory"] = [item.strip() for item in value.split(",") if item.strip()]
            elif key == "ACTIVE_QUESTS":
                if value == "":
                    data["active_quests"] = []
                else:
                    data["active_quests"] = [q.strip() for q in value.split(",") if q.strip()]
            elif key == "COMPLETED_QUESTS":
                if value == "":
                    data["completed_quests"] = []
                else:
                    data["completed_quests"] = [q.strip() for q in value.split(",") if q.strip()]
            else:
                # Unknown key – ignore instead of failing
                continue

        # Validate structure and types
        validate_character_data(data)

    except ValueError as e:
        # Problems converting numbers
        raise InvalidSaveDataError(f"Invalid numeric value in save file: {e}")
    except InvalidSaveDataError:
        # Let this bubble as the specified error type
        raise

    return data

def list_saved_characters(save_directory="data/save_games"):
    """
    Get list of all saved character names
    
    Returns: List of character names (without _save.txt extension)
    """
    # TODO: Implement this function
    # Return empty list if directory doesn't exist
    # Extract character names from filenames
    if not os.path.exists(save_directory):
        return []

    names = []
    for filename in os.listdir(save_directory):
        if filename.endswith("_save.txt"):
            char_name = filename[:-9]  # remove "_save.txt"
            names.append(char_name)

    return names

def delete_character(character_name, save_directory="data/save_games"):
    """
    Delete a character's save file
    
    Returns: True if deleted successfully
    Raises: CharacterNotFoundError if character doesn't exist
    """
    # TODO: Implement character deletion
    # Verify file exists before attempting deletion
    filename = f"{character_name}_save.txt"
    filepath = os.path.join(save_directory, filename)

    if not os.path.exists(filepath):
        raise CharacterNotFoundError(f"Character not found: {character_name}")

    os.remove(filepath)
    return True

# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    """
    Add experience to character and handle level ups
    
    Level up formula: level_up_xp = current_level * 100
    Example when leveling up:
    - Increase level by 1
    - Increase max_health by 10
    - Increase strength by 2
    - Increase magic by 2
    - Restore health to max_health
    
    Raises: CharacterDeadError if character health is 0
    """
    # TODO: Implement experience gain and leveling
    # Check if character is dead first
    # Add experience
    # Check for level up (can level up multiple times)
    # Update stats on level up
    if is_character_dead(character):
        raise CharacterDeadError("Dead characters cannot gain experience")

    # Add experience
    character["experience"] += xp_amount

    # Level up as long as experience meets threshold
    while character["experience"] >= character["level"] * 100:
        required_xp = character["level"] * 100
        character["experience"] -= required_xp
        character["level"] += 1
        character["max_health"] += 10
        character["strength"] += 2
        character["magic"] += 2
        character["health"] = character["max_health"]

    # The tests don't require a specific return, but we'll return True to indicate success
    return True

def add_gold(character, amount):
    """
    Add gold to character's inventory
    
    Args:
        character: Character dictionary
        amount: Amount of gold to add (can be negative for spending)
    
    Returns: New gold total
    Raises: ValueError if result would be negative
    """
    # TODO: Implement gold management
    # Check that result won't be negative
    # Update character's gold
    new_total = character.get("gold", 0) + amount
    if new_total < 0:
        raise ValueError("Gold cannot be negative")
    character["gold"] = new_total
    return new_total

def heal_character(character, amount):
    """
    Heal character by specified amount
    
    Health cannot exceed max_health
    
    Returns: Actual amount healed
    """
    # TODO: Implement healing
    # Calculate actual healing (don't exceed max_health)
    # Update character health
    if amount <= 0:
        return 0

    max_health = character["max_health"]
    current_health = character["health"]

    missing = max_health - current_health
    if missing <= 0:
        return 0

    heal_amount = amount if amount <= missing else missing
    character["health"] = current_health + heal_amount
    return heal_amount

def is_character_dead(character):
    """
    Check if character's health is 0 or below
    
    Returns: True if dead, False if alive
    """
    # TODO: Implement death check
    return character.get("health", 0) <= 0

def revive_character(character):
    """
    Revive a dead character with 50% health
    
    Returns: True if revived
    """
    # TODO: Implement revival
    # Restore health to half of max_health
    if not is_character_dead(character):
        return False

    max_health = character.get("max_health", 0)
    half_health = max_health // 2
    if half_health <= 0:
        half_health = max_health  # fallback if something weird
    character["health"] = half_health
    return True

# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
    """
    Validate that character dictionary has all required fields
    
    Required fields: name, class, level, health, max_health, 
                    strength, magic, experience, gold, inventory,
                    active_quests, completed_quests
    
    Returns: True if valid
    Raises: InvalidSaveDataError if missing fields or invalid types
    """
    # TODO: Implement validation
    # Check all required keys exist
    # Check that numeric values are numbers
    # Check that lists are actually lists
    required_fields = [
        "name",
        "class",
        "level",
        "health",
        "max_health",
        "strength",
        "magic",
        "experience",
        "gold",
        "inventory",
        "active_quests",
        "completed_quests"
    ]

    for field in required_fields:
        if field not in character:
            raise InvalidSaveDataError(f"Missing required character field: {field}")

    # Type checks
    if not isinstance(character["name"], str):
        raise InvalidSaveDataError("Character 'name' must be a string")
    if not isinstance(character["class"], str):
        raise InvalidSaveDataError("Character 'class' must be a string")

    int_fields = [
        "level",
        "health",
        "max_health",
        "strength",
        "magic",
        "experience",
        "gold"
    ]
    for field in int_fields:
        if not isinstance(character[field], int):
            raise InvalidSaveDataError(f"Character field '{field}' must be an integer")

    list_fields = ["inventory", "active_quests", "completed_quests"]
    for field in list_fields:
        if not isinstance(character[field], list):
            raise InvalidSaveDataError(f"Character field '{field}' must be a list")

    return True

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")
    
    # Test character creation
    # try:
    #     char = create_character("TestHero", "Warrior")
    #     print(f"Created: {char['name']} the {char['class']}")
    #     print(f"Stats: HP={char['health']}, STR={char['strength']}, MAG={char['magic']}")
    # except InvalidCharacterClassError as e:
    #     print(f"Invalid class: {e}")
    
    # Test saving
    # try:
    #     save_character(char)
    #     print("Character saved successfully")
    # except Exception as e:
    #     print(f"Save error: {e}")
    
    # Test loading
    # try:
    #     loaded = load_character("TestHero")
    #     print(f"Loaded: {loaded['name']}")
    # except CharacterNotFoundError:
    #     print("Character not found")
    # except SaveFileCorruptedError:
    #     print("Save file corrupted")
