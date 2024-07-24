import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def fetch_api_data(endpoint):
    api_key = os.getenv('NEXON_API_KEY')
    if not api_key:
        raise ValueError("API key not found. Please set the NEXON_API_KEY environment variable.")

    base_url = "https://open.api.nexon.com/static/tfd/meta/en"
    url = f"{base_url}/{endpoint}.json"
    headers = {"x-nxopen-api-key": api_key}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def process_weapon_data(weapons):
    processed_weapons = []
    for weapon in weapons:
        processed_weapon = {
            "weapon_name": weapon.get("weapon_name"),
            "weapon_id": weapon.get("weapon_id"),
            "weapon_type": weapon.get("weapon_type"),
            "weapon_tier": weapon.get("weapon_tier"),
            "weapon_rounds_type": weapon.get("weapon_rounds_type"),
            "image_url": weapon.get("image_url"),
            "weapon_perk_ability_name": weapon.get("weapon_perk_ability_name"),
            "weapon_perk_ability_description": weapon.get("weapon_perk_ability_description")
        }

        level_100_stats = next((level for level in weapon.get("firearm_atk", []) if level["level"] == 100), None)
        if level_100_stats:
            for stat in level_100_stats.get("firearm", []):
                processed_weapon[f"firearm_atk_{stat['firearm_atk_type']}"] = stat["firearm_atk_value"]

        for stat in weapon.get("base_stat", []):
            processed_weapon[stat["stat_id"]] = stat["stat_value"]

        processed_weapons.append(processed_weapon)

    return processed_weapons

def process_descendant_data(descendants):
    return [
        {
            "descendant_id": descendant.get("descendant_id"),
            "descendant_name": descendant.get("descendant_name"),
            "descendant_image_url": descendant.get("descendant_image_url"),
            "descendant_stat": descendant.get("descendant_stat"),
            "descendant_skill": descendant.get("descendant_skill")
        }
        for descendant in descendants
    ]

def process_module_data(modules):
    return [
        {
            "module_name": module.get("module_name"),
            "module_id": module.get("module_id"),
            "image_url": module.get("image_url"),
            "module_type": module.get("module_type"),
            "module_tier": module.get("module_tier"),
            "module_socket_type": module.get("module_socket_type"),
            "module_class": module.get("module_class"),
            "module_stat": module.get("module_stat")
        }
        for module in modules
    ]

def process_reactor_data(reactors):
    return [
        {
            "reactor_id": reactor.get("reactor_id"),
            "reactor_name": reactor.get("reactor_name"),
            "image_url": reactor.get("image_url"),
            "reactor_tier": reactor.get("reactor_tier"),
            "reactor_skill_power": reactor.get("reactor_skill_power"),
            "optimized_condition_type": reactor.get("optimized_condition_type")
        }
        for reactor in reactors
    ]

def process_external_component_data(components):
    return [
        {
            "external_component_id": component.get("external_component_id"),
            "external_component_name": component.get("external_component_name"),
            "image_url": component.get("image_url"),
            "external_component_equipment_type": component.get("external_component_equipment_type"),
            "external_component_tier": component.get("external_component_tier"),
            "base_stat": component.get("base_stat"),
            "set_option_detail": component.get("set_option_detail")
        }
        for component in components
    ]

def process_reward_data(rewards):
    return [
        {
            "map_id": reward.get("map_id"),
            "map_name": reward.get("map_name"),
            "battle_zone": reward.get("battle_zone")
        }
        for reward in rewards
    ]

def process_stat_data(stats):
    return [
        {
            "stat_id": stat.get("stat_id"),
            "stat_name": stat.get("stat_name")
        }
        for stat in stats
    ]

def process_void_battle_data(void_battles):
    return [
        {
            "void_battle_id": battle.get("void_battle_id"),
            "void_battle_name": battle.get("void_battle_name")
        }
        for battle in void_battles
    ]

def process_title_data(titles):
    return [
        {
            "title_id": title.get("title_id"),
            "title_name": title.get("title_name")
        }
        for title in titles
    ]

def save_processed_data(data, filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    save_dir = os.path.join(current_dir, "..", "resources", "api_data")
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, filename)
    
    with open(save_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Processed data saved to {save_path}")

def update_all_data():
    try:
        endpoints = [
            ("weapon", process_weapon_data),
            ("descendant", process_descendant_data),
            ("module", process_module_data),
            ("reactor", process_reactor_data),
            ("external-component", process_external_component_data),
            ("reward", process_reward_data),
            ("stat", process_stat_data),
            ("void-battle", process_void_battle_data),
            ("title", process_title_data)
        ]

        for endpoint, processor in endpoints:
            print(f"Fetching and processing {endpoint} data...")
            data = fetch_api_data(endpoint)
            if isinstance(data, list):
                processed_data = processor(data)
            elif isinstance(data, dict) and endpoint in data:
                processed_data = processor(data[endpoint])
            else:
                raise ValueError(f"Unexpected {endpoint} data format")
            save_processed_data(processed_data, f"processed_{endpoint.replace('-', '_')}_data.json")

        print("All data processing completed successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    update_all_data()