"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: Lauren Roberson

AI Usage: [I used ChatGPT (OpenAI, GPT-5 model, 2025) to help clarify certain module concepts, debug indentation issues, verify that my exception handling matched the test requirements, assist with structuring save/load formats and data parsing, and to help format and polish this README for clarity.

This is the main game file that ties all modules together.
Demonstrates module integration and complete game flow.
"""

# Import all our custom modules
import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *

# ============================================================================
# GAME STATE
# ============================================================================

# Global variables for game data
current_character = None
all_quests = {}
all_items = {}
game_running = False

# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    """
    Display main menu and get player choice
    
    Options:
    1. New Game
    2. Load Game
    3. Exit
    
    Returns: Integer choice (1-3)
    """
    # TODO: Implement main menu display
    # Show options
    # Get user input
    # Validate input (1-3)
    # Return choice
    while True:
        print("\n=== MAIN MENU ===")
        print("1. New Game")
        print("2. Load Game")
        print("3. Exit")
        try:
            choice = input("Enter choice (1-3): ")
        except EOFError:
            # If no input (e.g., in tests), default to Exit
            return 3
        if choice in ("1", "2", "3"):
            return int(choice)
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

def new_game():
    """
    Start a new game
    
    Prompts for:
    - Character name
    - Character class
    
    Creates character and starts game loop
    """
    global current_character
    
    # TODO: Implement new game creation
    # Get character name from user
    # Get character class from user
    # Try to create character with character_manager.create_character()
    # Handle InvalidCharacterClassError
    # Save character
    # Start game loop
    print("\n=== NEW GAME ===")
    try:
        name = input("Enter your character's name: ").strip()
    except EOFError:
        print("No input detected. Returning to main menu.")
        return
    if not name:
        print("Name cannot be empty.")
        return
    
    print("Choose a class: Warrior, Mage, Rogue, Cleric")
    try:
        char_class = input("Enter class: ").strip()
    except EOFError:
        print("No input detected. Returning to main menu.")
        return
    
    try:
        current_character = character_manager.create_character(name, char_class)
    except InvalidCharacterClassError as e:
        print(f"Error: {e}")
        return
    
    # Save initial character
    try:
        character_manager.save_character(current_character)
        print("Character created and saved!")
    except Exception as e:
        print(f"Warning: Could not save character: {e}")
    
    game_loop()

def load_game():
    """
    Load an existing saved game
    
    Shows list of saved characters
    Prompts user to select one
    """
    global current_character
    
    # TODO: Implement game loading
    # Get list of saved characters
    # Display them to user
    # Get user choice
    # Try to load character with character_manager.load_character()
    # Handle CharacterNotFoundError and SaveFileCorruptedError
    # Start game loop
    print("\n=== LOAD GAME ===")
    saved = character_manager.list_saved_characters()
    if not saved:
        print("No saved characters found.")
        return
    
    print("Saved Characters:")
    for i, name in enumerate(saved, start=1):
        print(f"{i}. {name}")
    
    try:
        choice = input("Enter number or name of character: ").strip()
    except EOFError:
        print("No input detected. Returning to main menu.")
        return
    
    # Allow selecting by index or by name
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(saved):
            name = saved[idx]
        else:
            print("Invalid selection.")
            return
    else:
        name = choice
    
    try:
        current_character = character_manager.load_character(name)
        print(f"Loaded character: {current_character['name']}")
    except CharacterNotFoundError as e:
        print(f"Error: {e}")
        return
    except SaveFileCorruptedError as e:
        print(f"Error: {e}")
        return
    except InvalidSaveDataError as e:
        print(f"Error: {e}")
        return
    
    game_loop()

# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    """
    Main game loop - shows game menu and processes actions
    """
    global game_running, current_character
    
    game_running = True
    
    # TODO: Implement game loop
    # While game_running:
    #   Display game menu
    #   Get player choice
    #   Execute chosen action
    #   Save game after each action
    if current_character is None:
        print("No active character. Returning to main menu.")
        return
    
    print(f"\nWelcome, {current_character['name']} the {current_character['class']}!")
    
    while game_running:
        choice = game_menu()
        
        if choice == 1:
            view_character_stats()
        elif choice == 2:
            view_inventory()
        elif choice == 3:
            quest_menu()
        elif choice == 4:
            explore()
        elif choice == 5:
            shop()
        elif choice == 6:
            save_game()
            print("Game saved. Exiting to main menu.")
            break
        else:
            print("Invalid choice.")
        
        # Auto-save after each action (except quit)
        if choice in (1, 2, 3, 4, 5):
            save_game()

def game_menu():
    """
    Display game menu and get player choice
    
    Options:
    1. View Character Stats
    2. View Inventory
    3. Quest Menu
    4. Explore (Find Battles)
    5. Shop
    6. Save and Quit
    
    Returns: Integer choice (1-6)
    """
    # TODO: Implement game menu
    while True:
        print("\n=== GAME MENU ===")
        print("1. View Character Stats")
        print("2. View Inventory")
        print("3. Quest Menu")
        print("4. Explore (Find Battles)")
        print("5. Shop")
        print("6. Save and Quit")
        try:
            choice = input("Enter choice (1-6): ")
        except EOFError:
            # Default to Save and Quit in non-interactive environments
            return 6
        if choice in ("1", "2", "3", "4", "5", "6"):
            return int(choice)
        else:
            print("Invalid choice. Please enter 1-6.")

# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    """Display character information"""
    global current_character
    
    # TODO: Implement stats display
    # Show: name, class, level, health, stats, gold, etc.
    # Use character_manager functions
    # Show quest progress using quest_handler
    if current_character is None:
        print("No active character.")
        return
    
    c = current_character
    print("\n=== CHARACTER STATS ===")
    print(f"Name: {c['name']}")
    print(f"Class: {c['class']}")
    print(f"Level: {c['level']}")
    print(f"Health: {c['health']}/{c['max_health']}")
    print(f"Strength: {c['strength']}")
    print(f"Magic: {c['magic']}")
    print(f"Experience: {c['experience']}")
    print(f"Gold: {c['gold']}")
    print(f"Active Quests: {len(c.get('active_quests', []))}")
    print(f"Completed Quests: {len(c.get('completed_quests', []))}")
    
    # Optional: show quest progress if data is loaded
    if all_quests:
        quest_handler.display_character_quest_progress(current_character, all_quests)

def view_inventory():
    """Display and manage inventory"""
    global current_character, all_items
    
    # TODO: Implement inventory menu
    # Show current inventory
    # Options: Use item, Equip weapon/armor, Drop item
    # Handle exceptions from inventory_system
    if current_character is None:
        print("No active character.")
        return
    
    print("\n=== INVENTORY ===")
    if not current_character.get("inventory"):
        print("Inventory is empty.")
    else:
        inventory_system.display_inventory(current_character, all_items)
    
    print("\n1. Use Item")
    print("2. Equip Weapon")
    print("3. Equip Armor")
    print("4. Back")
    try:
        choice = input("Enter choice: ")
    except EOFError:
        return
    
    if choice == "1":
        item_id = input("Enter item ID to use: ").strip()
        if item_id in all_items:
            try:
                inventory_system.use_item(current_character, item_id, all_items[item_id])
            except ItemNotFoundError as e:
                print(f"Error: {e}")
            except InvalidItemTypeError as e:
                print(f"Error: {e}")
        else:
            print("Unknown item ID.")
    elif choice == "2":
        item_id = input("Enter weapon item ID to equip: ").strip()
        if item_id in all_items:
            try:
                inventory_system.equip_weapon(current_character, item_id, all_items[item_id])
            except (ItemNotFoundError, InvalidItemTypeError, InventoryFullError) as e:
                print(f"Error: {e}")
        else:
            print("Unknown item ID.")
    elif choice == "3":
        item_id = input("Enter armor item ID to equip: ").strip()
        if item_id in all_items:
            try:
                inventory_system.equip_armor(current_character, item_id, all_items[item_id])
            except (ItemNotFoundError, InvalidItemTypeError, InventoryFullError) as e:
                print(f"Error: {e}")
        else:
            print("Unknown item ID.")
    else:
        return

def quest_menu():
    """Quest management menu"""
    global current_character, all_quests
    
    # TODO: Implement quest menu
    # Show:
    #   1. View Active Quests
    #   2. View Available Quests
    #   3. View Completed Quests
    #   4. Accept Quest
    #   5. Abandon Quest
    #   6. Complete Quest (for testing)
    #   7. Back
    # Handle exceptions from quest_handler
    if current_character is None:
        print("No active character.")
        return
    
    while True:
        print("\n=== QUEST MENU ===")
        print("1. View Active Quests")
        print("2. View Available Quests")
        print("3. View Completed Quests")
        print("4. Accept Quest")
        print("5. Abandon Quest")
        print("6. Complete Quest (for testing)")
        print("7. Back")
        try:
            choice = input("Enter choice: ")
        except EOFError:
            return
        
        if choice == "1":
            active = quest_handler.get_active_quests(current_character, all_quests)
            if not active:
                print("No active quests.")
            else:
                quest_handler.display_quest_list(active)
        elif choice == "2":
            available = quest_handler.get_available_quests(current_character, all_quests)
            if not available:
                print("No available quests.")
            else:
                quest_handler.display_quest_list(available)
        elif choice == "3":
            completed = quest_handler.get_completed_quests(current_character, all_quests)
            if not completed:
                print("No completed quests.")
            else:
                quest_handler.display_quest_list(completed)
        elif choice == "4":
            quest_id = input("Enter quest ID to accept: ").strip()
            try:
                quest_handler.accept_quest(current_character, quest_id, all_quests)
                print(f"Quest '{quest_id}' accepted.")
            except (QuestNotFoundError, InsufficientLevelError,
                    QuestRequirementsNotMetError, QuestAlreadyCompletedError) as e:
                print(f"Error: {e}")
        elif choice == "5":
            quest_id = input("Enter quest ID to abandon: ").strip()
            try:
                quest_handler.abandon_quest(current_character, quest_id)
                print(f"Quest '{quest_id}' abandoned.")
            except QuestNotActiveError as e:
                print(f"Error: {e}")
        elif choice == "6":
            quest_id = input("Enter quest ID to complete (testing): ").strip()
            try:
                rewards = quest_handler.complete_quest(current_character, quest_id, all_quests)
                print(f"Quest '{quest_id}' completed! Rewards: {rewards['xp']} XP, {rewards['gold']} gold.")
            except (QuestNotFoundError, QuestNotActiveError) as e:
                print(f"Error: {e}")
        elif choice == "7":
            return
        else:
            print("Invalid choice.")

def explore():
    """Find and fight random enemies"""
    global current_character
    
    # TODO: Implement exploration
    # Generate random enemy based on character level
    # Start combat with combat_system.SimpleBattle
    # Handle combat results (XP, gold, death)
    # Handle exceptions
    if current_character is None:
        print("No active character.")
        return
    
    print("\nYou venture forth in search of adventure...")
    level = current_character.get("level", 1)
    enemy = combat_system.get_random_enemy_for_level(level)
    print(f"A wild {enemy['name']} appears!")
    
    battle = combat_system.SimpleBattle(current_character, enemy)
    try:
        result = battle.start_battle()
    except CharacterDeadError as e:
        print(f"Error: {e}")
        handle_character_death()
        return
    
    if result["winner"] == "player":
        print(f"You won the battle! Gained {result['xp_gained']} XP and {result['gold_gained']} gold.")
        if result["xp_gained"] > 0:
            try:
                character_manager.gain_experience(current_character, result["xp_gained"])
            except CharacterDeadError:
                # Shouldn't happen right after winning, but just in case
                handle_character_death()
                return
        if result["gold_gained"] > 0:
            try:
                character_manager.add_gold(current_character, result["gold_gained"])
            except ValueError:
                pass
    else:
        print("You were defeated in battle...")
        handle_character_death()

def shop():
    """Shop menu for buying/selling items"""
    global current_character, all_items
    
    # TODO: Implement shop
    # Show available items for purchase
    # Show current gold
    # Options: Buy item, Sell item, Back
    # Handle exceptions from inventory_system
    if current_character is None:
        print("No active character.")
        return
    
    while True:
        print("\n=== SHOP ===")
        print(f"Your gold: {current_character['gold']}")
        print("Items for sale:")
        for item_id, data in all_items.items():
            cost = data.get("cost", 0)
            name = data.get("name", item_id)
            print(f"- {item_id}: {name} ({cost} gold)")
        
        print("\n1. Buy Item")
        print("2. Sell Item")
        print("3. Back")
        try:
            choice = input("Enter choice: ")
        except EOFError:
            return
        
        if choice == "1":
            item_id = input("Enter item ID to buy: ").strip()
            if item_id in all_items:
                try:
                    inventory_system.purchase_item(current_character, item_id, all_items[item_id])
                    print(f"Purchased {item_id}.")
                except (InsufficientResourcesError, InventoryFullError) as e:
                    print(f"Error: {e}")
            else:
                print("Unknown item ID.")
        elif choice == "2":
            item_id = input("Enter item ID to sell: ").strip()
            if item_id in all_items:
                try:
                    gold_received = inventory_system.sell_item(current_character, item_id, all_items[item_id])
                    print(f"Sold {item_id} for {gold_received} gold.")
                except ItemNotFoundError as e:
                    print(f"Error: {e}")
            else:
                print("Unknown item ID.")
        elif choice == "3":
            return
        else:
            print("Invalid choice.")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    """Save current game state"""
    global current_character
    
    # TODO: Implement save
    # Use character_manager.save_character()
    # Handle any file I/O exceptions
    if current_character is None:
        print("No active character to save.")
        return
    try:
        character_manager.save_character(current_character)
        print("Game saved.")
    except Exception as e:
        print(f"Error saving game: {e}")

def load_game_data():
    """Load all quest and item data from files"""
    global all_quests, all_items
    
    # TODO: Implement data loading
    # Try to load quests with game_data.load_quests()
    # Try to load items with game_data.load_items()
    # Handle MissingDataFileError, InvalidDataFormatError
    # If files missing, create defaults with game_data.create_default_data_files()
    all_quests = game_data.load_quests("data/quests.txt")
    all_items = game_data.load_items("data/items.txt")

def handle_character_death():
    """Handle character death"""
    global current_character, game_running
    
    # TODO: Implement death handling
    # Display death message
    # Offer: Revive (costs gold) or Quit
    # If revive: use character_manager.revive_character()
    # If quit: set game_running = False
    if current_character is None:
        game_running = False
        return
    
    print("\n=== YOU HAVE FALLEN ===")
    print("1. Revive (costs 50 gold)")
    print("2. Quit to main menu")
    try:
        choice = input("Enter choice: ")
    except EOFError:
        game_running = False
        return
    
    if choice == "1":
        cost = 50
        if current_character.get("gold", 0) < cost:
            print("Not enough gold to revive. Returning to main menu.")
            game_running = False
            return
        try:
            current_character["gold"] -= cost
            revived = character_manager.revive_character(current_character)
            if revived:
                print("You have been revived!")
            else:
                print("Could not revive character.")
                game_running = False
        except Exception as e:
            print(f"Error during revival: {e}")
            game_running = False
    else:
        print("Returning to main menu.")
        game_running = False

def display_welcome():
    """Display welcome message"""
    print("=" * 50)
    print("     QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("\nWelcome to Quest Chronicles!")
    print("Build your character, complete quests, and become a legend!")
    print()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main game execution function"""
    
    # Display welcome message
    display_welcome()
    
    # Load game data
    try:
        load_game_data()
        print("Game data loaded successfully!")
    except MissingDataFileError:
        print("Creating default game data...")
        game_data.create_default_data_files()
        load_game_data()
    except InvalidDataFormatError as e:
        print(f"Error loading game data: {e}")
        print("Please check data files for errors.")
        return
    
    # Main menu loop
    while True:
        choice = main_menu()
        
        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("\nThanks for playing Quest Chronicles!")
            break
        else:
            print("Invalid choice. Please select 1-3.")

if __name__ == "__main__":
    main()
