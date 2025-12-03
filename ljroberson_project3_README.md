# Project 3 – Quest Chronicles (Modular RPG System)
# Author
- Lauren Roberson – COMP 163, Fall 2025

# Description

- This project implements a complete modular RPG game using Python modules and exception handling.
Each system—character creation, combat, quests, inventory, data loading, and saving—is separated into its own module to demonstrate organization, modularity, and proper use of custom exceptions.

- The project includes custom mechanics such as equipment handling, special abilities, quest progression, and structured combat flow.

## Module Architecture (Required Features)

# game_data.py

- Loads all quest and item files.

- Parses and validates data.

- Raises exceptions for missing, corrupted, or incorrectly formatted files.

# character_manager.py

- Creates characters for the four required classes (Warrior, Mage, Rogue, Cleric).

- Handles leveling, gold, healing, death checks, saving, and loading.

# inventory_system.py

- Manages adding/removing items.

- Supports consumables, equippable weapons/armor, and shop purchases/sales.

- Enforces inventory limits and item type rules.

# quest_handler.py

- Handles accepting, completing, and abandoning quests.

- Enforces requirements (level, prerequisites, active/completed status).

- Tracks progression and provides quest data retrieval.

# combat_system.py

- Implements enemy types (goblin, orc, dragon).

- Provides turn-based combat (attacks + class abilities).

- Handles victory rewards and battle state tracking.

# main.py

- Connects all modules into a working game with menus, saving, exploration, and quest systems.

# Exception Strategy

- Data Errors: MissingDataFileError, InvalidDataFormatError

- Character Errors: InvalidCharacterClassError, CharacterNotFoundError, InvalidSaveDataError, CharacterDeadError

- Inventory Errors: InventoryFullError, ItemNotFoundError, InvalidItemTypeError, InsufficientResourcesError

- Quest Errors: QuestNotFoundError, InsufficientLevelError, QuestRequirementsNotMetError, QuestAlreadyCompletedError, QuestNotActiveError

- Combat Errors: InvalidTargetError, CombatNotActiveError

# Design Choices

- I designed the game so that each system works independently but still connects smoothly, making the overall flow easy to follow, easy to debug, and organized in a way that keeps gameplay consistent while still leaving room for creativity and expansion.

# AI Help

I used ChatGPT (OpenAI, GPT-5 model, 2025) to:

- Clarify module concepts

- Debug identenation errors

- Verify exception handling matched test expectations

- Assist with structuring save/load formats and data parsing

- Help format and polish this README

MLA Citation:
OpenAI. “ChatGPT (GPT-5 Model).” OpenAI, 2025, https://chat.openai.com/
.

# How to Play
Open the Project3 folder to access the python main.py file.
Run the game.

Choose from:

New Game – Create a character

Load Game – Resume your progress

Explore – Fight enemies and gain rewards

Quest Menu – Accept or complete quests

Inventory – Use or equip items

Shop – Buy or sell items

Save and Quit – Store progress in /data/save_games/