import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

xlsx = Path(r"C:\Users\Administrator\.openclaw\workspace\Stonewater_Karjat_Quote.xlsx")
out_path = Path(r"C:\Users\Administrator\.openclaw\workspace\table_images\All_In_One.png")

df = pd.read_excel(xlsx, sheet_name="All_In_One").fillna("")

fig_h = 0.6 + 0.35*len(df) + 0.5
fig, ax = plt.subplots(figsize=(12, fig_h))
ax.axis('off')

table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='left', loc='center')
table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 1.2)

for (row, col), cell in table.get_celld().items():
    if row == 0:
        cell.set_facecolor('#1f2937')
        cell.get_text().set_color('white')
        cell.get_text().set_weight('bold')
    else:
        if row % 2 == 0:
            cell.set_facecolor('#f3f4f6')

plt.tight_layout()
fig.savefig(out_path, dpi=200, bbox_inches='tight')
plt.close(fig)
print(str(out_path))
