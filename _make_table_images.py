import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

xlsx = Path(r"C:\Users\Administrator\.openclaw\workspace\Stonewater_Karjat_Quote.xlsx")
out_dir = Path(r"C:\Users\Administrator\.openclaw\workspace\table_images")
out_dir.mkdir(parents=True, exist_ok=True)

sheets = pd.read_excel(xlsx, sheet_name=None)

for name, df in sheets.items():
    df = df.fillna("")
    fig, ax = plt.subplots(figsize=(12, 0.6 + 0.35*len(df) + 0.5))
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
    out_path = out_dir / f"{name.replace(' ', '_')}.png"
    plt.tight_layout()
    fig.savefig(out_path, dpi=200, bbox_inches='tight')
    plt.close(fig)

print(str(out_dir))
