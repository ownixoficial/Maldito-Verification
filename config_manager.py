import json
import os

CONFIG_FILE = "guild_configs.json"

def load_all():
    if not os.path.exists(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_all(data: dict):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_guild_config(guild_id: int) -> dict:
    data = load_all()
    return data.get(str(guild_id), {})

def set_guild_config(guild_id: int, config: dict):
    data = load_all()
    data[str(guild_id)] = config
    save_all(data)

def update_guild_config(guild_id: int, key: str, value):
    config = get_guild_config(guild_id)
    config[key] = value
    set_guild_config(guild_id, config)
