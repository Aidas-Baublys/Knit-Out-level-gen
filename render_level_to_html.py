import os
from pathlib import Path


def render_level_to_html(level_data, folder="levels"):
    Path(folder).mkdir(parents=True, exist_ok=True)
    filename = os.path.join(folder, f"level_{level_data['level_id']}.html")

    color_map = {
        0: "#FF3B30",  # red
        1: "#FF9500",  # orange
        2: "#FFCC00",  # yellow
        3: "#34C759",  # green
        4: "#5AC8FA",  # light blue
        5: "#007AFF",  # blue
        6: "#5856D6",  # purple
        7: "#AF52DE",  # violet
        8: "#8E8E93",  # gray
        9: "#A3A3AF",  # silver
        10: "#000000",  # black
        -1: "#3a3a3c",  # empty slot: dark gray
    }

    def color_box(value):
        color = color_map.get(value, "#FFFFFF")
        text = str(value) if value >= 0 else ""
        return f"""
        <div style="
            width: 40px; height: 40px; 
            background-color: {color};
            color: white;
            font-weight: bold;
            text-align: center;
            line-height: 40px;
            border-radius: 6px;
            border: 1px solid #555;
            margin: 2px;
        ">{text}</div>
        """

    # Build carpet columns (flip so index 0 is bottom)
    max_height = max(len(col) for col in level_data["color_columns"])
    carpets_html = ""

    # Render from top row (max height) down to 0
    for row in reversed(range(max_height)):
        row_html = '<div style="display: flex; justify-content: center;">'
        for col in level_data["color_columns"]:
            val = col[row] if row < len(col) else -1
            row_html += color_box(val)
        row_html += "</div>"
        carpets_html += row_html

    # Build bobbin grid (bottom)
    bobbins_html = ""
    for row in level_data["bobbin_grid"]:
        row_html = '<div style="display: flex; justify-content: center;">'
        for val in row:
            row_html += color_box(val)
        row_html += "</div>"
        bobbins_html += row_html

    # Final HTML layout with dark mode styles
    html = f"""
    <html>
    <head>
      <meta charset="utf-8" />
      <title>Level {level_data['level_id']} Preview</title>
    </head>
    <body style="font-family: sans-serif; background: #1e1e1e; color: #f8f8f2; padding: 20px;">
      <h2 style="color: #ffd866;">Level {level_data['level_id']} Preview</h2>
      <h3 style="color: #50fa7b;">🧶 Color Columns (Carpets)</h3>
      <div style="margin-bottom: 40px;">{carpets_html}</div>
      <h3 style="color: #8be9fd;">🧵 Bobbin Grid</h3>
      <div>{bobbins_html}</div>
    </body>
    </html>
    """

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"🌐 HTML saved to {filename}")
