import re
from bs4 import BeautifulSoup

# Color map for top-3
HUE_MAP = {0: 120, 1: 30, 2: 0}  # green, orange, red

def update_top3_hues(html):
    soup = BeautifulSoup(html, "html.parser")

    # Extract all metric columns (indexed across all rows)
    td_matrix = []
    for tr in soup.find_all("tr"):
        tds = tr.find_all("td", attrs={"data-score": True})
        if tds:
            td_matrix.append(tds)

    # Transpose to get columns
    num_cols = max(len(row) for row in td_matrix)
    columns = [[] for _ in range(num_cols)]

    for row in td_matrix:
        for j, td in enumerate(row):
            try:
                val = float(td.text.strip())
                columns[j].append((val, td))
            except:
                continue

    for j, col in enumerate(columns):
        is_cd = (j % 2 == 0)

        # Sort by value: CD = ascending, F1 = descending
        sorted_vals = sorted(col, key=lambda x: x[0], reverse=not is_cd)

        for rank, (val, td) in enumerate(sorted_vals[:3]):
            hue = HUE_MAP[rank]
            style = td.get("style", "")
            style = re.sub(r"--hue:\s*\d+;", f"--hue: {hue};", style) if "--hue:" in style else f"{style}; --hue: {hue};"
            td["style"] = style

        # Clear other cells' hues
        for _, td in sorted_vals[3:]:
            style = td.get("style", "")
            style = re.sub(r"--hue:\s*\d+;?", "", style)
            td["style"] = style.strip("; ")

    return str(soup)

# Example usage
with open("results.html", "r") as f:
    html = f.read()

updated_html = update_top3_hues(html)

with open("results_updated.html", "w") as f:
    f.write(updated_html)