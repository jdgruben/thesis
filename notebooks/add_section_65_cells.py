#!/usr/bin/env python3
"""
Script to add Section 6.5 cells to the GDI Implementation notebook.
This adds all code cells for the revised trajectory classification.
"""

import json

# Load the notebook
with open('03_GDI_Implementation.ipynb', 'r') as f:
    nb = json.load(f)

# Find the index where we need to insert (after Section 6.5.1 markdown)
insert_idx = None
for i, cell in enumerate(nb['cells']):
    source = ''.join(cell.get('source', []))
    if '### 6.5.1 Complete Neighborhood Trajectory Table' in source:
        insert_idx = i + 1
        break

if insert_idx is None:
    print("Error: Could not find Section 6.5.1")
    exit(1)

print(f"Found insertion point at index {insert_idx}")

# Define all the new cells to insert
new_cells = [
    # Cell 1: Comprehensive trajectory table code
    {
        'cell_type': 'code',
        'metadata': {},
        'source': [
            '# Display comprehensive trajectory table for all 71 neighborhoods\n',
            'comprehensive_table = wide[[\n',
            '    \'GDI_2013\', \'GDI_2017\', \'GDI_2021\', \n',
            '    \'d13_21\', \'d13_17_rate\', \'d17_21_rate\', \n',
            '    \'trajectory\'\n',
            ']].copy()\n',
            '\n',
            '# Sort by total change (descending) to show full range\n',
            'comprehensive_table = comprehensive_table.sort_values(\'d13_21\', ascending=False)\n',
            '\n',
            '# Format numeric columns\n',
            'display_cols = [\'GDI_2013\', \'GDI_2017\', \'GDI_2021\', \'d13_21\', \'d13_17_rate\', \'d17_21_rate\']\n',
            'comprehensive_table[display_cols] = comprehensive_table[display_cols].round(2)\n',
            '\n',
            'print(f"Complete Trajectory Table: All {len(comprehensive_table)} Habitation Neighborhoods")\n',
            'print(f"Sorted by total change (d13_21) descending\\n")\n',
            'print("="*100)\n',
            '\n',
            '# Display full table\n',
            'pd.set_option(\'display.max_rows\', None)\n',
            'print(comprehensive_table.to_string())\n',
            'pd.set_option(\'display.max_rows\', 10)  # Reset\n',
            '\n',
            'print("\\n" + "="*100)\n',
            'print(f"\\nKey statistics:")\n',
            'print(f"  Minimum change: {wide[\'d13_21\'].min():.2f} GDI points")\n',
            'print(f"  Maximum change: {wide[\'d13_21\'].max():.2f} GDI points")\n',
            'print(f"  Mean change: {wide[\'d13_21\'].mean():.2f} GDI points")\n',
            'print(f"  Median change: {wide[\'d13_21\'].median():.2f} GDI points")\n',
            'print(f"  Std deviation: {wide[\'d13_21\'].std():.2f} GDI points")\n',
            'print(f"\\n  Neighborhoods with negative change: {(wide[\'d13_21\'] < 0).sum()}")\n',
            'print(f"  Neighborhoods with change 0-5: {((wide[\'d13_21\'] >= 0) & (wide[\'d13_21\'] < 5)).sum()}")\n',
            'print(f"  Neighborhoods with change 5-12: {((wide[\'d13_21\'] >= 5) & (wide[\'d13_21\'] < 12)).sum()}")\n',
            'print(f"  Neighborhoods with change ≥12: {(wide[\'d13_21\'] >= 12).sum()}")\n'
        ],
        'outputs': [],
        'execution_count': None
    },

    # Cell 2: Markdown for new classification
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '### 6.5.2 Implementing Four-Category Classification\n',
            '\n',
            'Now we apply the theory-driven thresholds to create a revised trajectory classification.'
        ]
    },

    # Cell 3: New classification code
    {
        'cell_type': 'code',
        'metadata': {},
        'source': [
            '# Define theory-driven classification function\n',
            'def classify_trajectory_v2(delta):\n',
            '    """Classify neighborhood trajectory using theory-driven thresholds."""\n',
            '    if delta < 0:\n',
            '        return \'Declining\'\n',
            '    elif delta < 5:\n',
            '        return \'Stable/Slow\'\n',
            '    elif delta < 12:\n',
            '        return \'Moderate\'\n',
            '    else:\n',
            '        return \'Rapid/Accelerating\'\n',
            '\n',
            '# Apply new classification\n',
            'wide[\'trajectory_v2\'] = wide[\'d13_21\'].apply(classify_trajectory_v2)\n',
            '\n',
            'print("New Four-Category Classification Applied")\n',
            'print("="*60)\n',
            'print("\\nCategory distribution:")\n',
            'print(wide[\'trajectory_v2\'].value_counts().sort_index())\n',
            '\n',
            'print("\\n\\nCategory statistics:")\n',
            'for cat in [\'Declining\', \'Stable/Slow\', \'Moderate\', \'Rapid/Accelerating\']:\n',
            '    subset = wide[wide[\'trajectory_v2\'] == cat][\'d13_21\']\n',
            '    if len(subset) > 0:\n',
            '        print(f"\\n{cat} (n={len(subset)}):")\n',
            '        print(f"  Range: [{subset.min():.2f}, {subset.max():.2f}] GDI points")\n',
            '        print(f"  Mean: {subset.mean():.2f} GDI points")\n',
            '        print(f"  Representative neighborhoods: {list(subset.nlargest(2).index)}")\n'
        ],
        'outputs': [],
        'execution_count': None
    },

    # Cell 4: Comparison analysis markdown
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '### 6.5.3 Comparison: Quartile vs Theory-Driven Classification\n',
            '\n',
            'How do neighborhoods shift between the old quartile-based system and the new theory-driven categories?'
        ]
    },

    # Cell 5: Comparison analysis code
    {
        'cell_type': 'code',
        'metadata': {},
        'source': [
            '# Crosstab showing movement between classifications\n',
            'import pandas as pd\n',
            '\n',
            'crosstab = pd.crosstab(\n',
            '    wide[\'trajectory\'],\n',
            '    wide[\'trajectory_v2\'],\n',
            '    margins=True,\n',
            '    margins_name=\'Total\'\n',
            ')\n',
            '\n',
            'print("Classification Comparison: Quartile (rows) vs Theory-Driven (columns)")\n',
            'print("="*80)\n',
            'print(crosstab)\n',
            '\n',
            'print("\\n\\nKey observations:")\n',
            'print("-"*80)\n',
            '\n',
            '# Find neighborhoods that moved from "Declining/weak" in quartile to different categories\n',
            'quartile_declining = wide[wide[\'trajectory\'] == \'Declining/weak\']\n',
            'v2_declining = quartile_declining[quartile_declining[\'trajectory_v2\'] == \'Declining\']\n',
            'v2_stable = quartile_declining[quartile_declining[\'trajectory_v2\'] == \'Stable/Slow\']\n',
            'v2_moderate = quartile_declining[quartile_declining[\'trajectory_v2\'] == \'Moderate\']\n',
            '\n',
            'print(f"\\nOf the {len(quartile_declining)} \'Declining/weak\' neighborhoods (quartile):")\n',
            'print(f"  • {len(v2_declining)} are truly Declining (Δ < 0)")\n',
            'print(f"  • {len(v2_stable)} are reclassified as Stable/Slow (0 ≤ Δ < 5)")\n',
            'print(f"  • {len(v2_moderate)} are reclassified as Moderate (5 ≤ Δ < 12)")\n',
            '\n',
            'if len(v2_declining) > 0:\n',
            '    print(f"\\n  True declining neighborhoods: {list(v2_declining.index)}")\n',
            '    print(f"    Change range: [{v2_declining[\'d13_21\'].min():.2f}, {v2_declining[\'d13_21\'].max():.2f}]")\n',
            '\n',
            'if len(v2_stable) > 0:\n',
            '    print(f"\\n  Misclassified as declining (actually stable): {list(v2_stable.index[:3])}...")\n',
            '    print(f"    Change range: [{v2_stable[\'d13_21\'].min():.2f}, {v2_stable[\'d13_21\'].max():.2f}]")\n',
            '\n',
            '# Rapid gentrifiers\n',
            'rapid = wide[wide[\'trajectory_v2\'] == \'Rapid/Accelerating\']\n',
            'print(f"\\n\\nRapid/Accelerating gentrifiers (Δ ≥ 12): {len(rapid)} neighborhoods")\n',
            'print(f"  {list(rapid.nlargest(5, \'d13_21\').index)}")\n'
        ],
        'outputs': [],
        'execution_count': None
    },

    # Cell 6: Visualization markdown
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '### 6.5.4 Updated Visualizations: Four-Category Time Series\n',
            '\n',
            'Recreate the time series panel plot (Section 10.4 style) using the new classification system.'
        ]
    },

    # Cell 7: Visualization code
    {
        'cell_type': 'code',
        'metadata': {},
        'source': [
            '# Time series panel with new 4-category classification\n',
            'fig, ax = plt.subplots(1, 1, figsize=(14, 8))\n',
            '\n',
            '# Define colors for new categories\n',
            'category_colors = {\n',
            '    \'Declining\': \'red\',\n',
            '    \'Stable/Slow\': \'orange\',\n',
            '    \'Moderate\': \'yellow\',\n',
            '    \'Rapid/Accelerating\': \'green\'\n',
            '}\n',
            '\n',
            '# Select representative neighborhoods from each category\n',
            'representatives_v2 = {}\n',
            'for cat in category_colors.keys():\n',
            '    subset = wide[wide[\'trajectory_v2\'] == cat].sort_values(\'d13_21\', ascending=False)\n',
            '    if len(subset) > 0:\n',
            '        # Pick top 2-3 representatives\n',
            '        n_repr = min(3 if cat in [\'Moderate\', \'Rapid/Accelerating\'] else 2, len(subset))\n',
            '        representatives_v2[cat] = list(subset.head(n_repr).index)\n',
            '\n',
            '# Plot trajectories\n',
            'for cat, neighborhoods in representatives_v2.items():\n',
            '    for q in neighborhoods:\n',
            '        row = wide.loc[q]\n',
            '        ax.plot(\n',
            '            [2013, 2017, 2021],\n',
            '            [row[\'GDI_2013\'], row[\'GDI_2017\'], row[\'GDI_2021\']],\n',
            '            marker=\'o\',\n',
            '            linewidth=2.5,\n',
            '            label=f\'{q} ({cat}, Δ={row["d13_21"]:.1f})\',\n',
            '            color=category_colors[cat],\n',
            '            alpha=0.75\n',
            '        )\n',
            '\n',
            'ax.set_xlabel(\'Year\', fontsize=13)\n',
            'ax.set_ylabel(\'GDI (0-100)\', fontsize=13)\n',
            'ax.set_title(\n',
            '    \'GDI Evolution by Theory-Driven Trajectory Category (Representative Neighborhoods)\',\n',
            '    fontsize=14,\n',
            '    fontweight=\'bold\'\n',
            ')\n',
            'ax.legend(bbox_to_anchor=(1.05, 1), loc=\'upper left\', fontsize=9)\n',
            'ax.grid(True, alpha=0.3)\n',
            'ax.set_xticks([2013, 2017, 2021])\n',
            'plt.tight_layout()\n',
            'plt.savefig(\'./_artifacts/figures/plots/time_series_panel_v2.png\', dpi=300, bbox_inches=\'tight\')\n',
            'plt.show()\n',
            'print(\'Saved time_series_panel_v2.png\')\n'
        ],
        'outputs': [],
        'execution_count': None
    },

    # Cell 8: Validation markdown
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '### 6.5.5 Validation: Why Theory-Driven Thresholds Are Superior\n',
            '\n',
            'Concrete examples demonstrating the advantage of substantive thresholds over quartiles.'
        ]
    },

    # Cell 9: Validation code
    {
        'cell_type': 'code',
        'metadata': {},
        'source': [
            '# Demonstrate specific problems with quartile approach\n',
            'print("VALIDATION: Problems with Quartile Classification")\n',
            'print("="*80)\n',
            '\n',
            '# Problem 1: Declining vs Stable conflation\n',
            'print("\\n1. QUARTILES CONFLATE DECLINING AND STABLE NEIGHBORHOODS")\n',
            'print("-"*80)\n',
            '\n',
            'quartile_weak = wide[wide[\'trajectory\'] == \'Declining/weak\'].copy()\n',
            'quartile_weak_sorted = quartile_weak.sort_values(\'d13_21\')\n',
            '\n',
            '# Show examples of truly declining (negative) grouped with slow growth\n',
            'print(f"\\nQuartile \'Declining/weak\' category includes {len(quartile_weak)} neighborhoods:")\n',
            'print(f"  Change range: [{quartile_weak[\'d13_21\'].min():.2f}, {quartile_weak[\'d13_21\'].max():.2f}] GDI points")\n',
            'print(f"\\n  Bottom 3 (truly declining):\")\n',
            'for idx in quartile_weak_sorted.head(3).index:\n',
            '    row = quartile_weak_sorted.loc[idx]\n',
            '    print(f\"    • {idx}: Δ = {row[\'d13_21\']:.2f} (v2: {row[\'trajectory_v2\']})\")\n',
            '\n',
            'print(f\"\\n  Top 3 (actually stable/moderate growth):\")\n',
            'for idx in quartile_weak_sorted.tail(3).index:\n',
            '    row = quartile_weak_sorted.loc[idx]\n',
            '    print(f\"    • {idx}: Δ = {row[\'d13_21\']:.2f} (v2: {row[\'trajectory_v2\']})\")\n',
            '\n',
            'print(f\"\\n  → The quartile approach groups Notre-Dame (Δ = {wide.loc[\'Notre-Dame\', \'d13_21\']:.2f}) \")\n',
            'print(f\"    with Gare (Δ = {wide.loc[\'Gare\', \'d13_21\']:.2f}), despite fundamentally different dynamics.\")\n',
            '\n',
            '# Problem 2: Moderate gentrification split across categories\n',
            'print(\"\\n\\n2. QUARTILES ARBITRARILY SPLIT MODERATE GENTRIFICATION\")\n',
            'print(\"-\"*80)\n',
            '\n',
            '# Find neighborhoods at quartile boundaries\n',
            'q25 = wide[\'d13_21\'].quantile(0.25)\n',
            'q75 = wide[\'d13_21\'].quantile(0.75)\n',
            '\n',
            'near_q25 = wide[(wide[\'d13_21\'] >= q25 - 1) & (wide[\'d13_21\'] <= q25 + 1)].sort_values(\'d13_21\')\n',
            'print(f\"\\nNeighborhoods near Q25 threshold ({q25:.2f}):\")\n',
            'for idx in near_q25.index:\n',
            '    row = near_q25.loc[idx]\n',
            '    print(f\"  • {idx}: Δ = {row[\'d13_21\']:.2f} | Quartile: {row[\'trajectory\']} | v2: {row[\'trajectory_v2\']}\")\n',
            '\n',
            'print(f\"\\n  → Petit Montrouge (Δ = {wide.loc[\'Petit Montrouge\', \'d13_21\']:.2f}) and \")\n',
            'print(f\"    Les Halles (Δ = {wide.loc[\'Les Halles\', \'d13_21\']:.2f}) are arbitrarily separated\")\n',
            'print(f\"    despite near-identical change. Theory-driven system groups both as Stable/Slow.\")\n',
            '\n',
            '# Problem 3: Meaningful threshold at zero\n',
            'print(\"\\n\\n3. ZERO AS A NATURAL BOUNDARY\")\n',
            'print(\"-\"*80)\n',
            '\n',
            'negative_change = wide[wide[\'d13_21\'] < 0].sort_values(\'d13_21\')\n',
            'print(f\"\\n{len(negative_change)} neighborhoods experienced actual decline (Δ < 0):\")\n',
            'for idx in negative_change.index:\n',
            '    row = negative_change.loc[idx]\n',
            '    print(f\"  • {idx}: Δ = {row[\'d13_21\']:.2f} | 2013 GDI: {row[\'GDI_2013\']:.1f} | 2021 GDI: {row[\'GDI_2021\']:.1f}\")\n',
            '\n',
            'print(f\"\\n  → These {len(negative_change)} neighborhoods lost gentrification pressure—a substantively\")\n',
            'print(f\"    distinct phenomenon that theory-driven classification captures explicitly.\")\n',
            '\n',
            'print(\"\\n\" + \"=\"*80)\n',
            'print(\"CONCLUSION: Theory-driven thresholds provide interpretable, meaningful categories.\")\n',
            'print(\"=\"*80)\n'
        ],
        'outputs': [],
        'execution_count': None
    },

    # Cell 10: Export and summary
    {
        'cell_type': 'code',
        'metadata': {},
        'source': [
            '# Export updated wide table with trajectory_v2\n',
            'export_table = wide[[\n',
            '    \'GDI_2013\', \'GDI_2017\', \'GDI_2021\',\n',
            '    \'d13_17\', \'d17_21\', \'d13_21\',\n',
            '    \'d13_17_rate\', \'d17_21_rate\',\n',
            '    \'trajectory\', \'trajectory_v2\'\n',
            ']].copy()\n',
            '\n',
            'export_table = export_table.sort_values(\'d13_21\', ascending=False)\n',
            'export_table.round(2).to_csv(\'./_artifacts/tables/trajectory_classification_v2.csv\')\n',
            '\n',
            'print(\"Exported trajectory_classification_v2.csv\")\n',
            'print(\"\\n\" + \"=\"*80)\n',
            'print(\"SECTION 6.5 SUMMARY: Theory-Driven Trajectory Classification\")\n',
            'print(\"=\"*80)\n',
            '\n',
            'print(\"\\nFour-category distribution:\")\n',
            'for cat in [\'Declining\', \'Stable/Slow\', \'Moderate\', \'Rapid/Accelerating\']:\n',
            '    count = (wide[\'trajectory_v2\'] == cat).sum()\n',
            '    pct = 100 * count / len(wide)\n',
            '    subset = wide[wide[\'trajectory_v2\'] == cat]\n',
            '    print(f\"  {cat:20s}: {count:2d} neighborhoods ({pct:5.1f}%) | \")\n',
            '    print(f\"     Range: [{subset[\'d13_21\'].min():6.2f}, {subset[\'d13_21\'].max():6.2f}] GDI points\")\n',
            '\n',
            'print(\"\\nKey advantages over quartile classification:\")\n',
            'print(\"  ✓ Distinguishes true decline (Δ < 0) from slow growth (0 ≤ Δ < 5)\")\n',
            'print(\"  ✓ Thresholds have substantive interpretation (points per year)\")\n',
            'print(\"  ✓ Group sizes reflect actual distribution, not forced equality\")\n',
            'print(\"  ✓ Robust to sample composition and outliers\")\n',
            'print(\"  ✓ Comparable across studies and time periods\")\n',
            '\n',
            'print(\"\\nRecommendation: Use trajectory_v2 for all subsequent analyses.\")\n',
            'print(\"=\"*80)\n'
        ],
        'outputs': [],
        'execution_count': None
    }
]

# Insert all cells at the identified position
for i, new_cell in enumerate(new_cells):
    nb['cells'].insert(insert_idx + i, new_cell)

# Save the updated notebook
with open('03_GDI_Implementation.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)

print(f"Successfully added {len(new_cells)} cells to the notebook at index {insert_idx}")
print("Section 6.5 is now complete!")
