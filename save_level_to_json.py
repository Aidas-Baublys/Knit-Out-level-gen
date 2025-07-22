import os
import json
from pathlib import Path


def save_level_to_json(level_data, folder="levels"):
    Path(folder).mkdir(parents=True, exist_ok=True)
    filename = os.path.join(folder, f"level_{level_data['level_id']}.json")
    with open(filename, "w") as f:
        json.dump(level_data, f, indent=2)
    print(f"📄 Level JSON saved to {filename}")
