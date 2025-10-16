"""
V3_EDA Section 1: Foundation
Cells 1-15: Title, Setup, Data Loading, Quick Profile, Summary
"""

def create_cell(cell_type, source, metadata=None):
    """Create a notebook cell"""
    cell = {
        "cell_type": cell_type,
        "metadata": metadata or {},
        "source": source if isinstance(source, list) else [source]
    }
    if cell_type == "code":
        cell["execution_count"] = None
        cell["outputs"] = []
    return cell

def build_section1():
    """Build foundation section cells"""
    cells = []

    # Cells 1-2 already defined in main builder
    # Continue with data loading

    # Cell 3: Data Loading
    cells.append(create_cell("markdown", [
        "## 1. Data Loading and Quick Profile\n\n",
        "Load all pre-processed datasets and perform quick profiling to understand:\n",
        "- Dataset dimensions and memory usage\n",
        "- Data types and missing value counts\n",
        "- File sizes and loading performance\n"
    ]))

    cells.append(create_cell("code", [
        "# Data loading function\n",
        "def load_dataset(path, name, **kwargs):\n",
        "    \"\"\"Load dataset and return with metadata\"\"\"\n",
        "    logger.info(f'Loading {name}...')\n",
        "    start_time = datetime.now()\n",
        "    \n",
        "    if path.suffix == '.parquet':\n",
        "        df = pd.read_parquet(path, **kwargs)\n",
        "    elif path.suffix == '.geojson':\n",
        "        df = gpd.read_file(path, **kwargs)\n",
        "    else:\n",
        "        raise ValueError(f'Unsupported file type: {path.suffix}')\n",
        "    \n",
        "    load_time = (datetime.now() - start_time).total_seconds()\n",
        "    file_size_mb = path.stat().st_size / (1024 * 1024)\n",
        "    memory_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)\n",
        "    \n",
        "    logger.info(f'  ✓ Loaded {name}: {df.shape[0]:,} rows × {df.shape[1]} cols in {load_time:.2f}s')\n",
        "    \n",
        "    return df, {\n",
        "        'name': name,\n",
        "        'shape': df.shape,\n",
        "        'file_size_mb': file_size_mb,\n",
        "        'memory_mb': memory_mb,\n",
        "        'load_time_s': load_time\n",
        "    }\n\n",
        "# Load all datasets\n",
        "print('=' * 80)\n",
        "print('LOADING DATASETS')\n",
        "print('=' * 80)\n\n",
        "datasets = {}\n",
        "metadata = []\n\n",
        "# FILOSOFI datasets\n",
        "filosofi_2013, meta = load_dataset(DATA_DIR / 'filosofi_2013_paris.parquet', 'FILOSOFI 2013')\n",
        "metadata.append(meta)\n",
        "filosofi_2017, meta = load_dataset(DATA_DIR / 'filosofi_2017_paris.parquet', 'FILOSOFI 2017')\n",
        "metadata.append(meta)\n",
        "filosofi_2021, meta = load_dataset(DATA_DIR / 'filosofi_2021_paris.parquet', 'FILOSOFI 2021')\n",
        "metadata.append(meta)\n\n",
        "# CENSUS datasets\n",
        "census_2013, meta = load_dataset(DATA_DIR / 'census_2013_paris.parquet', 'CENSUS 2013')\n",
        "metadata.append(meta)\n",
        "census_2017, meta = load_dataset(DATA_DIR / 'census_2017_paris.parquet', 'CENSUS 2017')\n",
        "metadata.append(meta)\n",
        "census_2021, meta = load_dataset(DATA_DIR / 'census_2021_paris.parquet', 'CENSUS 2021')\n",
        "metadata.append(meta)\n\n",
        "# DVF and SIRENE\n",
        "dvf, meta = load_dataset(DATA_DIR / 'dvf_mutations_paris.parquet', 'DVF Transactions')\n",
        "metadata.append(meta)\n",
        "sirene, meta = load_dataset(DATA_DIR / 'sirene_2014_2024_paris.parquet', 'SIRENE Establishments')\n",
        "metadata.append(meta)\n\n",
        "# IRIS boundaries\n",
        "iris_geo, meta = load_dataset(DATA_DIR / 'iris_paris.geojson', 'IRIS Boundaries')\n",
        "metadata.append(meta)\n\n",
        "print('\\n' + '=' * 80)\n",
        "print('ALL DATASETS LOADED SUCCESSFULLY')\n",
        "print('=' * 80)\n"
    ]))

    # Cell 4: Quick Profile Function
    cells.append(create_cell("markdown", [
        "### 1.1 Quick Data Profile\n\n",
        "For each dataset, generate a concise profile showing:\n",
        "- Shape, dtypes distribution, memory usage\n",
        "- Missing value summary (count + percentage)\n",
        "- Sample records (first 3 rows)\n"
    ]))

    cells.append(create_cell("code", [
        "def quick_profile(df, name):\n",
        "    \"\"\"Generate quick data profile\"\"\"\n",
        "    print(f'\\n{\"=\" * 80}')\n",
        "    print(f'QUICK PROFILE: {name}')\n",
        "    print(f'{\"=\" * 80}')\n",
        "    print(f'Shape: {df.shape[0]:,} rows × {df.shape[1]} columns')\n",
        "    print(f'Memory: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB')\n",
        "    \n",
        "    # Data types\n",
        "    dtype_counts = df.dtypes.value_counts()\n",
        "    print(f'\\nData Types:')\n",
        "    for dtype, count in dtype_counts.items():\n",
        "        print(f'  {str(dtype):15s}: {count:3d} columns')\n",
        "    \n",
        "    # Missing values\n",
        "    missing = df.isna().sum()\n",
        "    missing_pct = (missing / len(df) * 100).round(2)\n",
        "    has_missing = missing[missing > 0]\n",
        "    \n",
        "    if len(has_missing) > 0:\n",
        "        print(f'\\nMissing Values: {len(has_missing)} / {df.shape[1]} columns')\n",
        "        print(has_missing.to_frame('count').assign(pct=missing_pct[has_missing.index]).head(5))\n",
        "    else:\n",
        "        print(f'\\nMissing Values: None detected')\n",
        "    \n",
        "    print(f'\\nSample Records:')\n",
        "    display(df.head(3))\n",
        "    \n",
        "    return {\n",
        "        'name': name,\n",
        "        'rows': df.shape[0],\n",
        "        'cols': df.shape[1],\n",
        "        'missing_cols': len(has_missing),\n",
        "        'missing_cells': missing.sum(),\n",
        "        'missing_pct': (missing.sum() / (df.shape[0] * df.shape[1]) * 100)\n",
        "    }\n\n",
        "# Profile all datasets\n",
        "profiles = []\n",
        "profiles.append(quick_profile(filosofi_2013, 'FILOSOFI 2013'))\n",
        "profiles.append(quick_profile(filosofi_2017, 'FILOSOFI 2017'))\n",
        "profiles.append(quick_profile(filosofi_2021, 'FILOSOFI 2021'))\n",
        "profiles.append(quick_profile(census_2013, 'CENSUS 2013'))\n",
        "profiles.append(quick_profile(census_2017, 'CENSUS 2017'))\n",
        "profiles.append(quick_profile(census_2021, 'CENSUS 2021'))\n",
        "profiles.append(quick_profile(dvf, 'DVF Transactions'))\n",
        "profiles.append(quick_profile(sirene, 'SIRENE Establishments'))\n",
        "profiles.append(quick_profile(iris_geo, 'IRIS Boundaries'))\n"
    ]))

    # Cell 5: Summary Table
    cells.append(create_cell("markdown", [
        "### 1.2 Dataset Summary Table\n"
    ]))

    cells.append(create_cell("code", [
        "# Create comprehensive summary table\n",
        "summary_df = pd.DataFrame(metadata)\n",
        "profile_df = pd.DataFrame(profiles)\n\n",
        "final_summary = summary_df.merge(\n",
        "    profile_df[['name', 'missing_cols', 'missing_pct']], \n",
        "    on='name'\n",
        ")\n\n",
        "# Format for display\n",
        "final_summary['shape_str'] = final_summary.apply(\n",
        "    lambda x: f\"{x['shape'][0]:,} × {x['shape'][1]}\", axis=1\n",
        ")\n",
        "final_summary['file_size_mb'] = final_summary['file_size_mb'].round(2)\n",
        "final_summary['memory_mb'] = final_summary['memory_mb'].round(2)\n",
        "final_summary['missing_pct'] = final_summary['missing_pct'].round(2)\n\n",
        "display_summary = final_summary[[\n",
        "    'name', 'shape_str', 'file_size_mb', 'memory_mb', \n",
        "    'missing_cols', 'missing_pct', 'load_time_s'\n",
        "]].copy()\n",
        "display_summary.columns = [\n",
        "    'Dataset', 'Shape', 'File (MB)', 'Memory (MB)', \n",
        "    'Cols w/ Missing', 'Missing %', 'Load Time (s)'\n",
        "]\n\n",
        "print('\\n' + '=' * 80)\n",
        "print('DATASET SUMMARY TABLE')\n",
        "print('=' * 80)\n",
        "display(display_summary)\n\n",
        "# Save summary\n",
        "display_summary.to_csv(TABLES_DIR / 'dataset_summary.csv', index=False)\n",
        "print(f'\\n✓ Summary table saved to {TABLES_DIR / \"dataset_summary.csv\"}')\n"
    ]))

    return cells

# Make this importable
if __name__ == '__main__':
    cells = build_section1()
    print(f"Generated {len(cells)} cells for Section 1")
