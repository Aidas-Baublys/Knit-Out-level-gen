import random
import uuid
from typing import List
from render_level_to_html import render_level_to_html
from save_level_to_json import save_level_to_json


def generate_level(
    level_id: uuid.UUID = uuid.uuid4(),
    num_colors: int = 4,
    min_bobbins: int = 2,
    max_bobbins: int = 5,
    bobbin_grid_size=(3, 4),
):
    # Step 1: Pick colors
    all_colors = list(range(11))  # colors 0-10
    colors = random.sample(all_colors, num_colors)

    # Step 2: Decide number of bobbins per color
    bobbins_per_color = {
        color: random.randint(min_bobbins, max_bobbins) for color in colors
    }

    # Step 3: Generate color squares (3 per bobbin)
    color_squares = []
    for color, count in bobbins_per_color.items():
        color_squares += [color] * (count * 3)

    # Step 4: Distribute into 5 color columns
    random.shuffle(color_squares)
    color_columns = [[] for _ in range(5)]
    for color in color_squares:
        chosen_col = random.choice(color_columns)
        chosen_col.append(color)  # Top is index 0

    # Step 5: Generate bobbin list and place in grid
    all_bobbins = []
    for color, count in bobbins_per_color.items():
        all_bobbins += [color] * count
    random.shuffle(all_bobbins)

    rows, cols = bobbin_grid_size
    assert len(all_bobbins) <= rows * cols, "Not enough space in bobbin grid!"

    bobbin_grid: List[List[int]] = [[-1 for _ in range(cols)] for _ in range(rows)]
    for idx, color in enumerate(all_bobbins):
        r, c = divmod(idx, cols)
        bobbin_grid[r][c] = color

    # Fill remaining spaces with null (or -1 if needed)
    for r in range(rows):
        for c in range(cols):
            if bobbin_grid[r][c] is None:
                bobbin_grid[r][c] = -1  # Represents empty

    # Step 6: Output JSON
    level_data = {
        "level_id": str(level_id),
        "color_columns": color_columns,
        "bobbin_grid": bobbin_grid,
    }

    return level_data


# Example usage
if __name__ == "__main__":
    unique_id = uuid.uuid4()

    level = generate_level(
        level_id=unique_id, min_bobbins=5, max_bobbins=5, bobbin_grid_size=(5, 5)
    )
    save_level_to_json(level)
    render_level_to_html(level)
