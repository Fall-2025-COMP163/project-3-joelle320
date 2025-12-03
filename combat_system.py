"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: Lauren Roberson

AI Usage: [Document any AI assistance used]

Handles combat mechanics
"""

from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)

import random

# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================

def create_enemy(enemy_type):
    """
    Create an enemy based on type
    
    Example enemy types and stats:
    - goblin: health=50, strength=8, magic=2, xp_reward=25, gold_reward=10
    - orc: health=80, strength=12, magic=5, xp_reward=50, gold_reward=25
    - dragon: health=200, strength=25, magic=15, xp_reward=200, gold_reward=100
    
    Returns: Enemy dictionary
    Raises: InvalidTargetError if enemy_type not recognized
    """
    # TODO: Implement enemy creation
    # Return dictionary with: name, health, max_health, strength, magic, xp_reward, gold_reward
    enemy_type = enemy_type.lower()
    
    if enemy_type == "goblin":
        return {
            "name": "Goblin",
            "health": 50,
            "max_health": 50,
            "strength": 8,
            "magic": 2,
            "xp_reward": 25,
            "gold_reward": 10
        }
    elif enemy_type == "orc":
        return {
            "name": "Orc",
            "health": 80,
            "max_health": 80,
            "strength": 12,
            "magic": 5,
            "xp_reward": 50,
            "gold_reward": 25
        }
    elif enemy_type == "dragon":
        return {
            "name": "Dragon",
            "health": 200,
            "max_health": 200,
            "strength": 25,
            "magic": 15,
            "xp_reward": 200,
            "gold_reward": 100
        }
    else:
        raise InvalidTargetError(f"Unknown enemy type: {enemy_type}")

def get_random_enemy_for_level(character_level):
    """
    Get an appropriate enemy for character's level
    
    Level 1-2: Goblins
    Level 3-5: Orcs
    Level 6+: Dragons
    
    Returns: Enemy dictionary
    """
    # TODO: Implement level-appropriate enemy selection
    # Use if/elif/else to select enemy type
    # Call create_enemy with appropriate type
    if character_level <= 2:
        enemy_type = "goblin"
    elif character_level <= 5:
        enemy_type = "orc"
    else:
        enemy_type = "dragon"
    
    return create_enemy(enemy_type)

# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    """
    Simple turn-based combat system
    
    Manages combat between character and enemy
    """
    
    def __init__(self, character, enemy):
        """Initialize battle with character and enemy"""
        # TODO: Implement initialization
        # Store character and enemy
        # Set combat_active flag
        # Initialize turn counter
        self.character = character
        self.enemy = enemy
        self.combat_active = True
        self.turn_count = 0
    
    def start_battle(self):
        """
        Start the combat loop
        
        Returns: Dictionary with battle results:
                {'winner': 'player'|'enemy', 'xp_gained': int, 'gold_gained': int}
        
        Raises: CharacterDeadError if character is already dead
        """
        # TODO: Implement battle loop
        # Check character isn't dead
        # Loop until someone dies
        # Award XP and gold if player wins
        if self.character.get("health", 0) <= 0:
            raise CharacterDeadError("Character is already dead and cannot fight.")
        
        self.combat_active = True
        display_battle_log("Battle begins!")
        display_combat_stats(self.character, self.enemy)
        
        while self.combat_active:
            self.turn_count += 1
            
            # Player turn
            self.player_turn()
            winner = self.check_battle_end()
            if winner is not None:
                break
            
            # Enemy turn
            self.enemy_turn()
            winner = self.check_battle_end()
            if winner is not None:
                break
        
        self.combat_active = False
        
        xp_gained = 0
        gold_gained = 0
        
        if winner == "player":
            rewards = get_victory_rewards(self.enemy)
            xp_gained = rewards["xp"]
            gold_gained = rewards["gold"]
        else:
            xp_gained = 0
            gold_gained = 0
        
        return {"winner": winner, "xp_gained": xp_gained, "gold_gained": gold_gained}
    
    def player_turn(self):
        """
        Handle player's turn
        
        Displays options:
        1. Basic Attack
        2. Special Ability (if available)
        3. Try to Run
        
        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement player turn
        # Check combat is active
        # Display options
        # Get player choice
        # Execute chosen action
        if not self.combat_active:
            raise CombatNotActiveError("Combat is not active.")
        
        # For automated tests, we don't rely on player input,
        # but for interactive use we offer choices.
        print("\nYour turn:")
        print("1. Basic Attack")
        print("2. Special Ability")
        print("3. Try to Run")
        
        try:
            choice = input("Choose an action (1-3): ")
        except EOFError:
            # In non-interactive/testing environments, default to basic attack
            choice = "1"
        
        if choice == "2":
            result = use_special_ability(self.character, self.enemy)
            display_battle_log(result)
        elif choice == "3":
            if self.attempt_escape():
                display_battle_log("You successfully escaped!")
                return
            else:
                display_battle_log("You failed to escape!")
        else:
            damage = self.calculate_damage(self.character, self.enemy)
            self.apply_damage(self.enemy, damage)
            display_battle_log(f"You attack the {self.enemy['name']} for {damage} damage!")
        
        display_combat_stats(self.character, self.enemy)
    
    def enemy_turn(self):
        """
        Handle enemy's turn - simple AI
        
        Enemy always attacks
        
        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement enemy turn
        # Check combat is active
        # Calculate damage
        # Apply to character
        if not self.combat_active:
            raise CombatNotActiveError("Combat is not active.")
        
        damage = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, damage)
        display_battle_log(f"{self.enemy['name']} attacks you for {damage} damage!")
        display_combat_stats(self.character, self.enemy)
    
    def calculate_damage(self, attacker, defender):
        """
        Calculate damage from attack
        
        Damage formula: attacker['strength'] - (defender['strength'] // 4)
        Minimum damage: 1
        
        Returns: Integer damage amount
        """
        # TODO: Implement damage calculation
        attacker_strength = attacker.get("strength", 0)
        defender_strength = defender.get("strength", 0)
        damage = attacker_strength - (defender_strength // 4)
        if damage < 1:
            damage = 1
        return damage
    
    def apply_damage(self, target, damage):
        """
        Apply damage to a character or enemy
        
        Reduces health, prevents negative health
        """
        # TODO: Implement damage application
        current_health = target.get("health", 0)
        new_health = current_health - damage
        if new_health < 0:
            new_health = 0
        target["health"] = new_health
    
    def check_battle_end(self):
        """
        Check if battle is over
        
        Returns: 'player' if enemy dead, 'enemy' if character dead, None if ongoing
        """
        # TODO: Implement battle end check
        if self.enemy.get("health", 0) <= 0:
            self.combat_active = False
            display_battle_log(f"You have defeated the {self.enemy['name']}!")
            return "player"
        if self.character.get("health", 0) <= 0:
            self.combat_active = False
            display_battle_log("You have been defeated...")
            return "enemy"
        return None
    
    def attempt_escape(self):
        """
        Try to escape from battle
        
        50% success chance
        
        Returns: True if escaped, False if failed
        """
        # TODO: Implement escape attempt
        # Use random number or simple calculation
        # If successful, set combat_active to False
        if random.random() < 0.5:
            self.combat_active = False
            return True
        return False

# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    """
    Use character's class-specific special ability
    
    Example abilities by class:
    - Warrior: Power Strike (2x strength damage)
    - Mage: Fireball (2x magic damage)
    - Rogue: Critical Strike (3x strength damage, 50% chance)
    - Cleric: Heal (restore 30 health)
    
    Returns: String describing what happened
    Raises: AbilityOnCooldownError if ability was used recently
    """
    # TODO: Implement special abilities
    # Check character class
    # Execute appropriate ability
    # Track cooldowns (optional advanced feature)
    # Simple cooldown example: one use per battle stored on character
    if character.get("_special_on_cooldown"):
        raise AbilityOnCooldownError("Special ability is on cooldown.")
    
    char_class = character.get("class", "")
    result = ""
    
    if char_class == "Warrior":
        damage = warrior_power_strike(character, enemy)
        result = f"Warrior Power Strike deals {damage} damage!"
    elif char_class == "Mage":
        damage = mage_fireball(character, enemy)
        result = f"Mage Fireball deals {damage} damage!"
    elif char_class == "Rogue":
        damage, crit = rogue_critical_strike(character, enemy)
        if crit:
            result = f"Rogue Critical Strike lands for {damage} critical damage!"
        else:
            result = f"Rogue attack deals {damage} damage."
    elif char_class == "Cleric":
        healed = cleric_heal(character)
        result = f"Cleric Heal restores {healed} health."
    else:
        result = "Nothing happens..."
    
    # Put on cooldown for remainder of current battle
    character["_special_on_cooldown"] = True
    return result

def warrior_power_strike(character, enemy):
    """Warrior special ability"""
    # TODO: Implement power strike
    # Double strength damage
    base_damage = character.get("strength", 0) * 2
    # Simple enemy defense: none for special
    damage = base_damage if base_damage > 0 else 1
    enemy["health"] = max(0, enemy.get("health", 0) - damage)
    return damage

def mage_fireball(character, enemy):
    """Mage special ability"""
    # TODO: Implement fireball
    # Double magic damage
    base_damage = character.get("magic", 0) * 2
    damage = base_damage if base_damage > 0 else 1
    enemy["health"] = max(0, enemy.get("health", 0) - damage)
    return damage

def rogue_critical_strike(character, enemy):
    """Rogue special ability"""
    # TODO: Implement critical strike
    # 50% chance for triple damage
    strength = character.get("strength", 0)
    crit = random.random() < 0.5
    if crit:
        damage = strength * 3
    else:
        damage = strength
    if damage <= 0:
        damage = 1
    enemy["health"] = max(0, enemy.get("health", 0) - damage)
    return damage, crit

def cleric_heal(character):
    """Cleric special ability"""
    # TODO: Implement healing
    # Restore 30 HP (not exceeding max_health)
    heal_amount = 30
    current = character.get("health", 0)
    max_health = character.get("max_health", current)
    missing = max_health - current
    actual_heal = heal_amount if heal_amount <= missing else missing
    character["health"] = current + actual_heal
    return actual_heal

# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character):
    """
    Check if character is in condition to fight
    
    Returns: True if health > 0 and not in battle
    """
    # TODO: Implement fight check
    # We only track health here; battle state is managed by SimpleBattle
    return character.get("health", 0) > 0

def get_victory_rewards(enemy):
    """
    Calculate rewards for defeating enemy
    
    Returns: Dictionary with 'xp' and 'gold'
    """
    # TODO: Implement reward calculation
    xp = enemy.get("xp_reward", 0)
    gold = enemy.get("gold_reward", 0)
    return {"xp": xp, "gold": gold}

def display_combat_stats(character, enemy):
    """
    Display current combat status
    
    Shows both character and enemy health/stats
    """
    # TODO: Implement status display
    print(f"\n{character['name']}: HP={character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}")
    pass

def display_battle_log(message):
    """
    Display a formatted battle message
    """
    # TODO: Implement battle log display
    print(f">>> {message}")
    pass

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")
    
    # Test enemy creation
    # try:
    #     goblin = create_enemy("goblin")
    #     print(f"Created {goblin['name']}")
    # except InvalidTargetError as e:
    #     print(f"Invalid enemy: {e}")
    
    # Test battle
    # test_char = {
    #     'name': 'Hero',
    #     'class': 'Warrior',
    #     'health': 120,
    #     'max_health': 120,
    #     'strength': 15,
    #     'magic': 5
    # }
    #
    # battle = SimpleBattle(test_char, goblin)
    # try:
    #     result = battle.start_battle()
    #     print(f"Battle result: {result}")
    # except CharacterDeadError:
    #     print("Character is dead!")
