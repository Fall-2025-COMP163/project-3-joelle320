"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: Lauren Roberson

AI Usage: [Document any AI assistance used]

This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """
    Load quest data from file
    
    Expected format per quest (separated by blank lines):
    QUEST_ID: unique_quest_name
    TITLE: Quest Display Title
    DESCRIPTION: Quest description text
    REWARD_XP: 100
    REWARD_GOLD: 50
    REQUIRED_LEVEL: 1
    PREREQUISITE: previous_quest_id (or NONE)
    
    Returns: Dictionary of quests {quest_id: quest_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    # TODO: Implement this function
    # Must handle:
    # - FileNotFoundError → raise MissingDataFileError
    # - Invalid format → raise InvalidDataFormatError
    # - Corrupted/unreadable data → raise CorruptedDataError
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        raise MissingDataFileError(f"Quest data file not found: {filename}")
    except OSError as e:
        # Problems opening the file (permissions, etc.)
        raise CorruptedDataError(f"Error opening quest data file: {e}")

    quests = {}
    block = []

    try:
        for raw_line in lines:
            line = raw_line.strip()
            if line == "":
                if block:
                    quest_dict = parse_quest_block(block)
                    validate_quest_data(quest_dict)
                    quest_id = quest_dict["quest_id"]
                    quests[quest_id] = quest_dict
                    block = []
            else:
                block.append(line)

        # Handle last block if file doesn't end with a blank line
        if block:
            quest_dict = parse_quest_block(block)
            validate_quest_data(quest_dict)
            quest_id = quest_dict["quest_id"]
            quests[quest_id] = quest_dict

    except InvalidDataFormatError:
        # Let this bubble up as-is for invalid formatting
        raise
    except Exception as e:
        # Any unexpected parsing problems count as corrupted data
        raise CorruptedDataError(f"Error parsing quest data: {e}")

    return quests


def load_items(filename="data/items.txt"):
    """
    Load item data from file
    
    Expected format per item (separated by blank lines):
    ITEM_ID: unique_item_name
    NAME: Item Display Name
    TYPE: weapon|armor|consumable
    EFFECT: stat_name:value (e.g., strength:5 or health:20)
    COST: 100
    DESCRIPTION: Item description
    
    Returns: Dictionary of items {item_id: item_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    # TODO: Implement this function
    # Must handle same exceptions as load_quests
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        raise MissingDataFileError(f"Item data file not found: {filename}")
    except OSError as e:
        raise CorruptedDataError(f"Error opening item data file: {e}")

    items = {}
    block = []

    try:
        for raw_line in lines:
            line = raw_line.strip()
            if line == "":
                if block:
                    item_dict = parse_item_block(block)
                    validate_item_data(item_dict)
                    item_id = item_dict["item_id"]
                    items[item_id] = item_dict
                    block = []
            else:
                block.append(line)

        if block:
            item_dict = parse_item_block(block)
            validate_item_data(item_dict)
            item_id = item_dict["item_id"]
            items[item_id] = item_dict

    except InvalidDataFormatError:
        raise
    except Exception as e:
        raise CorruptedDataError(f"Error parsing item data: {e}")

    return items


def validate_quest_data(quest_dict):
    """
    Validate that quest dictionary has all required fields
    
    Required fields: quest_id, title, description, reward_xp, 
                    reward_gold, required_level, prerequisite
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields
    """
    # TODO: Implement validation
    # Check that all required keys exist
    # Check that numeric values are actually numbers
    required_fields = [
        "quest_id",
        "title",
        "description",
        "reward_xp",
        "reward_gold",
        "required_level",
        "prerequisite"
    ]

    for field in required_fields:
        if field not in quest_dict:
            raise InvalidDataFormatError(f"Missing required quest field: {field}")

    # Check numeric types
    for numeric_field in ["reward_xp", "reward_gold", "required_level"]:
        if not isinstance(quest_dict[numeric_field], int):
            raise InvalidDataFormatError(
                f"Quest field '{numeric_field}' must be an integer"
            )

    return True


def validate_item_data(item_dict):
    """
    Validate that item dictionary has all required fields
    
    Required fields: item_id, name, type, effect, cost, description
    Valid types: weapon, armor, consumable
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields or invalid type
    """
    # TODO: Implement validation
    required_fields = [
        "item_id",
        "name",
        "type",
        "effect",
        "cost",
        "description"
    ]

    for field in required_fields:
        if field not in item_dict:
            raise InvalidDataFormatError(f"Missing required item field: {field}")

    valid_types = ["weapon", "armor", "consumable"]
    item_type = item_dict["type"]
    if item_type not in valid_types:
        raise InvalidDataFormatError(f"Invalid item type: {item_type}")

    if not isinstance(item_dict["cost"], int):
        raise InvalidDataFormatError("Item field 'cost' must be an integer")

    return True


def create_default_data_files():
    """
    Create default data files if they don't exist
    This helps with initial setup and testing
    """
    # TODO: Implement this function
    # Create data/ directory if it doesn't exist
    # Create default quests.txt and items.txt files
    # Handle any file permission errors appropriately
    data_dir = "data"
    quests_path = os.path.join(data_dir, "quests.txt")
    items_path = os.path.join(data_dir, "items.txt")

    try:
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        # Only create defaults if they don't already exist
        if not os.path.exists(quests_path):
            with open(quests_path, "w") as qfile:
                qfile.write(
                    "QUEST_ID: intro_quest\n"
                    "TITLE: First Steps\n"
                    "DESCRIPTION: Your journey begins in a quiet village.\n"
                    "REWARD_XP: 50\n"
                    "REWARD_GOLD: 10\n"
                    "REQUIRED_LEVEL: 1\n"
                    "PREREQUISITE: NONE\n"
                    "\n"
                    "QUEST_ID: goblin_menace\n"
                    "TITLE: Goblin Menace\n"
                    "DESCRIPTION: Clear the nearby woods of goblins.\n"
                    "REWARD_XP: 100\n"
                    "REWARD_GOLD: 25\n"
                    "REQUIRED_LEVEL: 2\n"
                    "PREREQUISITE: intro_quest\n"
                )

        if not os.path.exists(items_path):
            with open(items_path, "w") as ifile:
                ifile.write(
                    "ITEM_ID: rusty_sword\n"
                    "NAME: Rusty Sword\n"
                    "TYPE: weapon\n"
                    "EFFECT: strength:2\n"
                    "COST: 15\n"
                    "DESCRIPTION: A worn blade, but better than nothing.\n"
                    "\n"
                    "ITEM_ID: leather_armor\n"
                    "NAME: Leather Armor\n"
                    "TYPE: armor\n"
                    "EFFECT: health:10\n"
                    "COST: 30\n"
                    "DESCRIPTION: Basic protection for new adventurers.\n"
                    "\n"
                    "ITEM_ID: minor_potion\n"
                    "NAME: Minor Healing Potion\n"
                    "TYPE: consumable\n"
                    "EFFECT: health:20\n"
                    "COST: 10\n"
                    "DESCRIPTION: Restores a small amount of health.\n"
                )
    except OSError as e:
        # Any file creation issues count as corruption/setup problems
        raise CorruptedDataError(f"Error creating default data files: {e}")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """
    Parse a block of lines into a quest dictionary
    
    Args:
        lines: List of strings representing one quest
    
    Returns: Dictionary with quest data
    Raises: InvalidDataFormatError if parsing fails
    """
    # TODO: Implement parsing logic
    # Split each line on ": " to get key-value pairs
    # Convert numeric strings to integers
    # Handle parsing errors gracefully
    quest = {}

    for line in lines:
        if ": " not in line:
            raise InvalidDataFormatError(f"Invalid quest line format: {line}")
        key, value = line.split(": ", 1)
        key = key.strip().upper()
        value = value.strip()

        if key == "QUEST_ID":
            quest["quest_id"] = value
        elif key == "TITLE":
            quest["title"] = value
        elif key == "DESCRIPTION":
            quest["description"] = value
        elif key == "REWARD_XP":
            try:
                quest["reward_xp"] = int(value)
            except ValueError:
                raise InvalidDataFormatError("REWARD_XP must be an integer")
        elif key == "REWARD_GOLD":
            try:
                quest["reward_gold"] = int(value)
            except ValueError:
                raise InvalidDataFormatError("REWARD_GOLD must be an integer")
        elif key == "REQUIRED_LEVEL":
            try:
                quest["required_level"] = int(value)
            except ValueError:
                raise InvalidDataFormatError("REQUIRED_LEVEL must be an integer")
        elif key == "PREREQUISITE":
            if value.upper() == "NONE":
                quest["prerequisite"] = None
            else:
                quest["prerequisite"] = value
        else:
            # Unknown key – ignore or treat as invalid. We'll be strict:
            raise InvalidDataFormatError(f"Unknown quest field: {key}")

    return quest


def parse_item_block(lines):
    """
    Parse a block of lines into an item dictionary
    
    Args:
        lines: List of strings representing one item
    
    Returns: Dictionary with item data
    Raises: InvalidDataFormatError if parsing fails
    """
    # TODO: Implement parsing logic
    item = {}

    for line in lines:
        if ": " not in line:
            raise InvalidDataFormatError(f"Invalid item line format: {line}")
        key, value = line.split(": ", 1)
        key = key.strip().upper()
        value = value.strip()

        if key == "ITEM_ID":
            item["item_id"] = value
        elif key == "NAME":
            item["name"] = value
        elif key == "TYPE":
            item["type"] = value.lower()
        elif key == "EFFECT":
            # EFFECT: stat_name:value
            effect_str = value
            if ":" in effect_str:
                stat_name, stat_value = effect_str.split(":", 1)
                stat_name = stat_name.strip()
                stat_value_str = stat_value.strip()
                # Try to convert numeric portion to int
                try:
                    stat_value_int = int(stat_value_str)
                    item["effect"] = {stat_name: stat_value_int}
                except ValueError:
                    # If not numeric, just store as string
                    item["effect"] = {stat_name: stat_value_str}
            else:
                # If format is unexpected, treat whole thing as a raw effect string
                item["effect"] = {"raw": effect_str}
        elif key == "COST":
            try:
                item["cost"] = int(value)
            except ValueError:
                raise InvalidDataFormatError("COST must be an integer")
        elif key == "DESCRIPTION":
            item["description"] = value
        else:
            raise InvalidDataFormatError(f"Unknown item field: {key}")

    return item

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")
    
    # Test creating default files
    # create_default_data_files()
    
    # Test loading quests
    # try:
    #     quests = load_quests()
    #     print(f"Loaded {len(quests)} quests")
    # except MissingDataFileError:
    #     print("Quest file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid quest format: {e}")
    
    # Test loading items
    # try:
    #     items = load_items()
    #     print(f"Loaded {len(items)} items")
    # except MissingDataFileError:
    #     print("Item file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid item format: {e}")
