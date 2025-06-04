import re
from bs4 import BeautifulSoup

def compute_hue(value, is_cd, best, threshold):
    """Linearly scale value to hue [0, 100]. Green = 100, Red = 0"""
    if is_cd:
        # Lower is better
        if value >= threshold:
            return 0
        return max(0, min(100, round(100 * (threshold - value) / (threshold - best))))
    else:
        # Higher is better
        if value <= threshold:
            return 0
        return max(0, min(100, round(100 * (value - threshold) / (best - threshold))))

def update_hue_in_html(html):
    soup = BeautifulSoup(html, "html.parser")

    # Identify all CD and F1 values
    data_cells = soup.find_all("td", attrs={"data-score": True})
    cd_values = []
    f1_values = []

    for td in data_cells:
        try:
            val = float(td.text.strip())
            is_cd = "CD" in td.find_previous("tr").text or "↓" in td.find_previous("tr").text
            # heuristic: even-numbered metric columns = CD, odd = F1
            col_index = td.parent.find_all("td").index(td)
            is_cd = col_index % 2 != 0
            (cd_values if is_cd else f1_values).append(val)
        except:
            pass

    # Split values by column
    cd_values_by_col = {}
    f1_values_by_col = {}
    for td in data_cells:
        try:
            val = float(td.text.strip())
            col_index = td.parent.find_all("td").index(td)
            if col_index % 2 != 0:
                cd_values_by_col.setdefault(col_index, []).append(val)
            else:
                f1_values_by_col.setdefault(col_index, []).append(val)
        except:
            pass

    cd_mins = {col: min(vals) for col, vals in cd_values_by_col.items()}
    f1_maxs = {col: max(vals) for col, vals in f1_values_by_col.items()}

    CD_THRESH = 20.0
    F1_THRESH = 0.70

    # Apply hue updates
    for td in data_cells:
        try:
            val = float(td.text.strip())
            col_index = td.parent.find_all("td").index(td)
            is_cd = col_index % 2 != 0
            hue = compute_hue(val, is_cd, cd_mins[col_index] if is_cd else f1_maxs[col_index], CD_THRESH if is_cd else F1_THRESH)
            style = td.get("style", "")
            style = re.sub(r"--hue:\s*\d+;", f"--hue: {hue};", style)
            td["style"] = style
        except:
            continue

    return str(soup)

# Example usage
with open("results.html", "r") as f:
    html = f.read()

updated_html = update_hue_in_html(html)

with open("results_updated.html", "w") as f:
    f.write(updated_html)