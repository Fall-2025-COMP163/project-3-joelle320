"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Starter Code

Name: Lauren Roberson

AI Usage: [Document any AI assistance used]

This module handles inventory management, item usage, and equipment.
"""

from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError
)

# Maximum inventory size
MAX_INVENTORY_SIZE = 20

# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================

def add_item_to_inventory(character, item_id):
    """
    Add an item to character's inventory
    
    Args:
        character: Character dictionary
        item_id: Unique item identifier
    
    Returns: True if added successfully
    Raises: InventoryFullError if inventory is at max capacity
    """
    # TODO: Implement adding items
    # Check if inventory is full (>= MAX_INVENTORY_SIZE)
    # Add item_id to character['inventory'] list
    inventory = character.setdefault('inventory', [])
    if len(inventory) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full")
    
    inventory.append(item_id)
    return True

def remove_item_from_inventory(character, item_id):
    """
    Remove an item from character's inventory
    
    Args:
        character: Character dictionary
        item_id: Item to remove
    
    Returns: True if removed successfully
    Raises: ItemNotFoundError if item not in inventory
    """
    # TODO: Implement item removal
    # Check if item exists in inventory
    # Remove item from list
    inventory = character.get('inventory', [])
    if item_id not in inventory:
        raise ItemNotFoundError(f"Item not found in inventory: {item_id}")
    
    inventory.remove(item_id)
    return True

def has_item(character, item_id):
    """
    Check if character has a specific item
    
    Returns: True if item in inventory, False otherwise
    """
    # TODO: Implement item check
    return item_id in character.get('inventory', [])

def count_item(character, item_id):
    """
    Count how many of a specific item the character has
    
    Returns: Integer count of item
    """
    # TODO: Implement item counting
    # Use list.count() method
    return character.get('inventory', []).count(item_id)

def get_inventory_space_remaining(character):
    """
    Calculate how many more items can fit in inventory
    
    Returns: Integer representing available slots
    """
    # TODO: Implement space calculation
    inventory = character.get('inventory', [])
    remaining = MAX_INVENTORY_SIZE - len(inventory)
    if remaining < 0:
        remaining = 0
    return remaining

def clear_inventory(character):
    """
    Remove all items from inventory
    
    Returns: List of removed items
    """
    # TODO: Implement inventory clearing
    # Save current inventory before clearing
    # Clear character's inventory list
    inventory = character.get('inventory', [])
    removed_items = list(inventory)
    character['inventory'] = []
    return removed_items

# ============================================================================
# ITEM USAGE
# ============================================================================

def use_item(character, item_id, item_data):
    """
    Use a consumable item from inventory
    
    Args:
        character: Character dictionary
        item_id: Item to use
        item_data: Item information dictionary from game_data
    
    Item types and effects:
    - consumable: Apply effect and remove from inventory
    - weapon/armor: Cannot be "used", only equipped
    
    Returns: String describing what happened
    Raises: 
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'consumable'
    """
    # TODO: Implement item usage
    # Check if character has the item
    # Check if item type is 'consumable'
    # Parse effect (format: "stat_name:value" e.g., "health:20")
    # Apply effect to character
    # Remove item from inventory
    if not has_item(character, item_id):
        raise ItemNotFoundError(f"Item not found in inventory: {item_id}")
    
    item_type = item_data.get('type')
    if item_type != 'consumable':
        raise InvalidItemTypeError(f"Item '{item_id}' is not a consumable")

    effect = item_data.get('effect')

    # Handle both string and dict effect formats
    if isinstance(effect, dict):
        for stat_name, value in effect.items():
            try:
                value_int = int(value)
            except (TypeError, ValueError):
                continue
            apply_stat_effect(character, stat_name, value_int)
    else:
        # Assume string like "health:20"
        stat_name, value = parse_item_effect(effect)
        apply_stat_effect(character, stat_name, value)

    remove_item_from_inventory(character, item_id)
    return f"Used {item_id}."

def equip_weapon(character, item_id, item_data):
    """
    Equip a weapon
    
    Args:
        character: Character dictionary
        item_id: Weapon to equip
        item_data: Item information dictionary
    
    Weapon effect format: "strength:5" (adds 5 to strength)
    
    If character already has weapon equipped:
    - Unequip current weapon (remove bonus)
    - Add old weapon back to inventory
    
    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'weapon'
    """
    # TODO: Implement weapon equipping
    # Check item exists and is type 'weapon'
    # Handle unequipping current weapon if exists
    # Parse effect and apply to character stats
    # Store equipped_weapon in character dictionary
    # Remove item from inventory
    if not has_item(character, item_id):
        raise ItemNotFoundError(f"Weapon not found in inventory: {item_id}")
    
    if item_data.get('type') != 'weapon':
        raise InvalidItemTypeError(f"Item '{item_id}' is not a weapon")

    # If a weapon is already equipped, unequip it first
    if 'equipped_weapon' in character:
        # Remove previous weapon bonus
        prev_bonus = character.get('_weapon_bonus')
        if prev_bonus:
            apply_stat_effect(character, prev_bonus['stat'], -prev_bonus['value'])
        # Return old weapon to inventory
        prev_weapon_id = character['equipped_weapon']
        add_item_to_inventory(character, prev_weapon_id)

    # Apply new weapon bonus
    effect = item_data.get('effect')
    if isinstance(effect, dict):
        # Use the first entry
        for stat_name, value in effect.items():
            value_int = int(value)
            apply_stat_effect(character, stat_name, value_int)
            character['_weapon_bonus'] = {'stat': stat_name, 'value': value_int}
            break
    else:
        stat_name, value = parse_item_effect(effect)
        apply_stat_effect(character, stat_name, value)
        character['_weapon_bonus'] = {'stat': stat_name, 'value': value}

    # Equip the weapon
    character['equipped_weapon'] = item_id
    remove_item_from_inventory(character, item_id)
    return f"Equipped weapon {item_id}."

def equip_armor(character, item_id, item_data):
    """
    Equip armor
    
    Args:
        character: Character dictionary
        item_id: Armor to equip
        item_data: Item information dictionary
    
    Armor effect format: "max_health:10" (adds 10 to max_health)
    
    If character already has armor equipped:
    - Unequip current armor (remove bonus)
    - Add old armor back to inventory
    
    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'armor'
    """
    # TODO: Implement armor equipping
    # Similar to equip_weapon but for armor
    if not has_item(character, item_id):
        raise ItemNotFoundError(f"Armor not found in inventory: {item_id}")
    
    if item_data.get('type') != 'armor':
        raise InvalidItemTypeError(f"Item '{item_id}' is not armor")

    # If armor is already equipped, unequip it
    if 'equipped_armor' in character:
        prev_bonus = character.get('_armor_bonus')
        if prev_bonus:
            apply_stat_effect(character, prev_bonus['stat'], -prev_bonus['value'])
        prev_armor_id = character['equipped_armor']
        add_item_to_inventory(character, prev_armor_id)

    effect = item_data.get('effect')
    if isinstance(effect, dict):
        for stat_name, value in effect.items():
            value_int = int(value)
            apply_stat_effect(character, stat_name, value_int)
            character['_armor_bonus'] = {'stat': stat_name, 'value': value_int}
            break
    else:
        stat_name, value = parse_item_effect(effect)
        apply_stat_effect(character, stat_name, value)
        character['_armor_bonus'] = {'stat': stat_name, 'value': value}

    character['equipped_armor'] = item_id
    remove_item_from_inventory(character, item_id)
    return f"Equipped armor {item_id}."

def unequip_weapon(character):
    """
    Remove equipped weapon and return it to inventory
    
    Returns: Item ID that was unequipped, or None if no weapon equipped
    Raises: InventoryFullError if inventory is full
    """
    # TODO: Implement weapon unequipping
    # Check if weapon is equipped
    # Remove stat bonuses
    # Add weapon back to inventory
    # Clear equipped_weapon from character
    if 'equipped_weapon' not in character:
        return None

    weapon_id = character['equipped_weapon']

    # Remove stat bonus
    bonus = character.get('_weapon_bonus')
    if bonus:
        apply_stat_effect(character, bonus['stat'], -bonus['value'])
        character.pop('_weapon_bonus', None)

    # Add weapon back to inventory (may raise InventoryFullError)
    add_item_to_inventory(character, weapon_id)

    # Clear equipped weapon
    character.pop('equipped_weapon', None)
    return weapon_id

def unequip_armor(character):
    """
    Remove equipped armor and return it to inventory
    
    Returns: Item ID that was unequipped, or None if no armor equipped
    Raises: InventoryFullError if inventory is full
    """
    # TODO: Implement armor unequipping
    if 'equipped_armor' not in character:
        return None

    armor_id = character['equipped_armor']

    bonus = character.get('_armor_bonus')
    if bonus:
        apply_stat_effect(character, bonus['stat'], -bonus['value'])
        character.pop('_armor_bonus', None)

    add_item_to_inventory(character, armor_id)

    character.pop('equipped_armor', None)
    return armor_id

# ============================================================================
# SHOP SYSTEM
# ============================================================================

def purchase_item(character, item_id, item_data):
    """
    Purchase an item from a shop
    
    Args:
        character: Character dictionary
        item_id: Item to purchase
        item_data: Item information with 'cost' field
    
    Returns: True if purchased successfully
    Raises:
        InsufficientResourcesError if not enough gold
        InventoryFullError if inventory is full
    """
    # TODO: Implement purchasing
    # Check if character has enough gold
    # Check if inventory has space
    # Subtract gold from character
    # Add item to inventory
    cost = item_data.get('cost', 0)
    current_gold = character.get('gold', 0)

    if current_gold < cost:
        raise InsufficientResourcesError("Not enough gold to purchase item")

    if len(character.get('inventory', [])) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full")

    character['gold'] = current_gold - cost
    add_item_to_inventory(character, item_id)
    return True

def sell_item(character, item_id, item_data):
    """
    Sell an item for half its purchase cost
    
    Args:
        character: Character dictionary
        item_id: Item to sell
        item_data: Item information with 'cost' field
    
    Returns: Amount of gold received
    Raises: ItemNotFoundError if item not in inventory
    """
    # TODO: Implement selling
    # Check if character has item
    # Calculate sell price (cost // 2)
    # Remove item from inventory
    # Add gold to character
    if not has_item(character, item_id):
        raise ItemNotFoundError(f"Item not found in inventory: {item_id}")

    cost = item_data.get('cost', 0)
    sell_price = cost // 2

    remove_item_from_inventory(character, item_id)
    character['gold'] = character.get('gold', 0) + sell_price

    return sell_price

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_item_effect(effect_string):
    """
    Parse item effect string into stat name and value
    
    Args:
        effect_string: String in format "stat_name:value"
    
    Returns: Tuple of (stat_name, value)
    Example: "health:20" → ("health", 20)
    """
    # TODO: Implement effect parsing
    # Split on ":"
    # Convert value to integer
    if effect_string is None:
        raise ValueError("Effect string cannot be None")

    parts = str(effect_string).split(":", 1)
    if len(parts) != 2:
        raise ValueError(f"Invalid effect format: {effect_string}")

    stat_name = parts[0].strip()
    value_str = parts[1].strip()
    value = int(value_str)
    return stat_name, value

def apply_stat_effect(character, stat_name, value):
    """
    Apply a stat modification to character
    
    Valid stats: health, max_health, strength, magic
    
    Note: health cannot exceed max_health
    """
    # TODO: Implement stat application
    # Add value to character[stat_name]
    # If stat is health, ensure it doesn't exceed max_health
    if stat_name not in ["health", "max_health", "strength", "magic"]:
        return  # Ignore unknown stats gracefully

    if stat_name == "health":
        current = character.get("health", 0)
        max_health = character.get("max_health", current)
        new_health = current + value
        if new_health > max_health:
            new_health = max_health
        character["health"] = new_health
    elif stat_name == "max_health":
        current_max = character.get("max_health", 0)
        new_max = current_max + value
        character["max_health"] = new_max
        # If current health is now above max, clamp it
        if character.get("health", 0) > new_max:
            character["health"] = new_max
    else:
        # strength or magic
        character[stat_name] = character.get(stat_name, 0) + value

def display_inventory(character, item_data_dict):
    """
    Display character's inventory in formatted way
    
    Args:
        character: Character dictionary
        item_data_dict: Dictionary of all item data
    
    Shows item names, types, and quantities
    """
    # TODO: Implement inventory display
    # Count items (some may appear multiple times)
    # Display with item names from item_data_dict
    inventory = character.get('inventory', [])
    counts = {}

    for item_id in inventory:
        counts[item_id] = counts.get(item_id, 0) + 1

    lines = []
    for item_id, qty in counts.items():
        item_info = item_data_dict.get(item_id, {})
        name = item_info.get('name', item_id)
        item_type = item_info.get('type', 'unknown')
        lines.append(f"{name} ({item_type}) x{qty}")

    output = "\n".join(lines)
    print(output)
    return output

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== INVENTORY SYSTEM TEST ===")
    
    # Test adding items
    # test_char = {'inventory': [], 'gold': 100, 'health': 80, 'max_health': 80}
    # 
    # try:
    #     add_item_to_inventory(test_char, "health_potion")
    #     print(f"Inventory: {test_char['inventory']}")
    # except InventoryFullError:
    #     print("Inventory is full!")
    
    # Test using items
    # test_item = {
    #     'item_id': 'health_potion',
    #     'type': 'consumable',
    #     'effect': 'health:20'
    # }
    # 
    # try:
    #     result = use_item(test_char, "health_potion", test_item)
    #     print(result)
    # except ItemNotFoundError:
    #     print("Item not found")
