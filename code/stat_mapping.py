import json
import os

def load_processed_data(file_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "..", "resources", "api_data", file_name)
    try:
        with open(data_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: {file_name} not found. Proceeding without this data.")
        return []

# Load weapon data
processed_weapon_data = load_processed_data("processed_weapon_data.json")

# Attempt to load descendant data, but don't fail if it's not there
processed_descendant_data = load_processed_data("processed_descendant_data.json")

# Collect all unique keys from the processed weapon data
all_weapon_keys = set()
for weapon in processed_weapon_data:
    all_weapon_keys.update(weapon.keys())

# Define the mappings
STAT_MAPPING = {
    "weapon_name": "Weapon Name",
    "weapon_id": "Weapon ID",
    "weapon_type": "Weapon Type",
    "weapon_tier": "Weapon Tier",
    "weapon_rounds_type": "Rounds Type",
    "image_url": "Image URL",
    "weapon_perk_ability_name": "Weapon Perk Ability Name",
    "weapon_perk_ability_description": "Weapon Perk Ability Description",
    "firearm_atk_105000026": "Normal Attack",
    "firearm_atk_105000057": "Elemental Attack",
    "105000023": "Fire Rate",
    "105000035": "Weak Point Damage",
    "105000077": "Critical Hit Damage",
    "105000054": "Range Start",
    "105000055": "Range End",
    "105000056": "ATK Drop-off Modifier",
    "105000005": "Max Range",
    "105000006": "Hip Fire Accuracy",
    "105000036": "Aimed Shot Accuracy",
    "105000007": "Effective Range",
    "105000037": "Recoil",
    "105000132": "Spread",
    "105000038": "Spread Recovery",
    "105000039": "Spread Per Shot",
    "105000040": "Min Spread",
    "105000041": "Max Spread",
    "105000021": "Magazine Capacity",
    "105000022": "Rounds per Magazine",
    "105000095": "Reload Time",
    "105000033": "Charge Time",
    "105000019": "Sprint Speed",
    "105000018": "Movement Speed",
    "105000034": "Movement Speed (Firing)",
    "105000020": "Movement Speed (Aiming)",
    "105000070": "Crush",
    "105000071": "Crush Rate",
    "105000008": "Max Ammo",
    "105000092": "Burst",
    "105000075": "Penetration",
    "105000030": "Critical Hit Rate",
    "105000031": "Critical Hit Damage Multiplier",
    "105000170": "Status Effect Trigger Rate",
    "105000051": "Charge Level",
    "105000069": "Crush/Blast/Pierce Damage",
    "105000073": "Explosive ATK Drop-off Range",
    "105000194": "Beam Rifle Charge Gain/Depletion Speed",
    "105000195": "Beam Rifle Charge Depletion Speed",
    "105000032": "Shotgun Burst",
    "105000174": "Launcher Explosion Radius",
    "105000200": "Shots Per Burst",
}

# Check if all keys from the processed data are in our mapping
for key in all_weapon_keys:
    if key not in STAT_MAPPING:
        print(f"Warning: '{key}' is not in the STAT_MAPPING dictionary")

def get_readable_name(key):
    """
    Get the human-readable name for a given key.
    If the key is not in the mapping, return the key itself.
    """
    return STAT_MAPPING.get(key, key)

def get_stat_value(weapon, stat_key):
    """
    Get the value of a stat for a given weapon.
    Returns None if the stat is not found.
    """
    return weapon.get(stat_key)

def get_readable_stat(weapon, stat_key):
    """
    Get a human-readable string representation of a stat for a given weapon.
    """
    value = get_stat_value(weapon, stat_key)
    if value is not None:
        return f"{get_readable_name(stat_key)}: {value}"
    return None

# Example usage:
if __name__ == "__main__":
    # Print all mappings
    for key, value in STAT_MAPPING.items():
        print(f"{key}: {value}")

    # Example of how to use these functions with the first weapon in the processed data
    if processed_weapon_data:
        example_weapon = processed_weapon_data[0]
        print("\nExample weapon stats:")
        for key in example_weapon.keys():
            readable_stat = get_readable_stat(example_weapon, key)
            if readable_stat:
                print(readable_stat)