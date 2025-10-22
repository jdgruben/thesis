# Critical Fix: Pooled Standardization for Temporal GDI Analysis

## Date: October 22, 2025

## Problem Identified

The original analysis calculated z-scores **separately for each year** (2013, 2017, 2021), which prevented valid temporal comparisons:

```python
# OLD APPROACH (INCORRECT)
for z_col, raw_col in components.items():
    values = residential_df[raw_col].dropna()
    mean = values.mean()  # Different mean for each year!
    std = values.std()    # Different std for each year!
    df_std[z_col] = (df_std[raw_col] - mean) / std
```

**Why this was problematic:**
- Each year was standardized to have mean=0, std=1 by construction
- GDI changes reflected **relative ranking shifts** within each year, not real socioeconomic changes
- A quartier could show GDI increase simply because others declined more
- Impossible to distinguish between:
  - Real gentrification (absolute improvement)
  - Relative position change (citywide distribution shift)

## Solution Implemented

### Pooled Standardization Methodology

Calculate **pooled parameters** once across all three years, then apply uniformly:

1. **Step 1: Calculate Pooled Parameters**
   ```python
   def calculate_pooled_standardization_params(data_2013, data_2017, data_2021):
       # Combine values from all three years for each variable
       all_values = []
       for year, df in [(2013, data_2013), (2017, data_2017), (2021, data_2021)]:
           residential_mask = df['quartier_label'] == 'Residential'
           values = df.loc[residential_mask, raw_col].dropna()
           all_values.extend(values.tolist())
       
       # Calculate POOLED statistics
       pooled_mean = np.mean(all_values)
       pooled_std = np.std(all_values)
       
       return {'mean': pooled_mean, 'std': pooled_std}
   ```

2. **Step 2: Apply Same Parameters to All Years**
   ```python
   def standardize_gdi_components(df, year, pooled_params):
       # Use SAME mean and std for all years
       pooled_mean = pooled_params[z_col]['mean']
       pooled_std = pooled_params[z_col]['std']
       
       df_std[z_col] = (df_std[raw_col] - pooled_mean) / pooled_std
   ```

### Mathematical Formula

$$Z_{pooled} = \frac{X_{year,i} - \mu_{pooled}}{\sigma_{pooled}}$$

Where:
- $X_{year,i}$ = Raw value for quartier $i$ in specific year
- $\mu_{pooled}$ = Mean across ALL three years (2013, 2017, 2021)
- $\sigma_{pooled}$ = Standard deviation across ALL three years

## Results & Validation

### Pooled Parameters Calculated (N=219 residential quartiers × 3 years)

| Component | Pooled Mean | Pooled SD | Interpretation |
|-----------|-------------|-----------|----------------|
| Median Income | €32,104 | €7,341 | Average household income |
| CS3 (Executives) | 30.87% | 5.71% | Share of professional class |
| CS6 (Workers) | 3.98% | 2.00% | Share of working class |
| Age 25-39 | 26.01% | 4.95% | Young adult population |
| Age 65+ | 16.42% | 4.07% | Elderly population |
| Labor Income | 84.32% | 9.41% | Income from work |
| Pension Income | 18.93% | 4.26% | Income from retirement |
| Social Benefits | 2.92% | 2.09% | Welfare dependency |

### Temporal Evolution Now Visible

With pooled standardization, we can now see **real changes**:

#### Mean GDI Evolution
- **2013**: -0.136 (below pooled average)
- **2017**: +0.029 (near pooled average)
- **2021**: +0.107 (above pooled average)

**Interpretation**: Paris residential quartiers show clear gentrification trajectory from 2013→2021, with mean GDI increasing by +0.243 standard deviations.

#### Year-Specific Means vs. Pooled Reference

**Example: Median Income**
- Pooled mean: €32,104
- 2013 mean: €30,419 (below average → negative contribution to GDI)
- 2017 mean: €31,748 (still below but improving)
- 2021 mean: €34,145 (above average → positive contribution to GDI)

This shows **real income growth** relative to the 2013-2021 baseline.

**Example: Labor Income Share**
- Pooled mean: 84.32%
- 2013 mean: 76.62% (well below → Paris more dependent on other income)
- 2017 mean: 88.63% (above average → shift toward work income)
- 2021 mean: 87.71% (above average, stabilizing)

This shows **structural economic change** in income sources.

## Benefits of Pooled Standardization

✅ **Valid Temporal Comparisons**
- GDI changes reflect real socioeconomic evolution
- Can track actual gentrification trajectories
- Changes are interpretable in standardized units

✅ **Consistent Baseline**
- Z-score = 0 means "equal to 2013-2021 Paris average" in all years
- Z-score = +1 means "one SD above 2013-2021 average" in all years
- Comparisons across years are meaningful

✅ **Detects Citywide Trends**
- Mean GDI can shift over time (not forced to 0 each year)
- Can identify overall gentrification or decline
- Distinguishes quartier-level from citywide changes

✅ **Preserves All Other Features**
- Residential quartier filtering maintained (≥50% residential)
- NaN handling for missing data preserved
- Non-residential quartiers still excluded from calculations

## Code Changes Summary

### Files Modified
- `notebooks/V4_GDI.ipynb` - Cell [50] (around line 423-575)

### New Function Added
```python
calculate_pooled_standardization_params(data_2013, data_2017, data_2021)
```
- Inputs: Three dataframes (one per year)
- Outputs: Dictionary with pooled mean/std for each of 8 components
- Called once before any standardization

### Existing Function Modified
```python
standardize_gdi_components(df, year, pooled_params)  # Added pooled_params argument
```
- New parameter: `pooled_params` (required)
- Changed logic: Uses pooled parameters instead of year-specific
- Preserves: All filtering, NaN handling, residential quartier logic

### Workflow Updated
```python
# OLD (incorrect)
data_2013_std = standardize_gdi_components(data_2013, 2013)
data_2017_std = standardize_gdi_components(data_2017, 2017)
data_2021_std = standardize_gdi_components(data_2021, 2021)

# NEW (correct)
pooled_params = calculate_pooled_standardization_params(data_2013, data_2017, data_2021)
data_2013_std = standardize_gdi_components(data_2013, 2013, pooled_params)
data_2017_std = standardize_gdi_components(data_2017, 2017, pooled_params)
data_2021_std = standardize_gdi_components(data_2021, 2021, pooled_params)
```

## Methodological Documentation Updated

Updated markdown cell (Section 4) to reflect pooled methodology:

**OLD TEXT:**
> "Each year is standardized independently to capture relative position within Paris for that year."

**NEW TEXT:**
> "Using pooled standardization across all three years (2013, 2017, 2021) to enable valid temporal comparisons. A single mean and standard deviation is calculated using data from all years combined, then applied uniformly."

## Next Steps

1. ✅ **Implementation Complete** - Pooled standardization is now active
2. ✅ **Validation Passed** - Cell executed successfully with expected output
3. 🔄 **Re-run Downstream Analysis** - Execute all subsequent cells to update:
   - GDI classifications
   - Temporal trajectories
   - Transition matrices
   - Visualizations
   - Export files

4. 📊 **Expected Changes in Results:**
   - Mean GDI will no longer be ~0 for each year
   - Temporal trajectories will show more variation
   - Gentrification patterns will be more pronounced
   - Stable categories may decrease (more real change detected)

## Impact Assessment

### What Changes in Results
- ✅ GDI values for all quartiers in all years (re-standardized)
- ✅ Temporal change calculations (Δ GDI)
- ✅ Trajectory classifications (stable/upward/downward)
- ✅ Transition matrices between categories
- ✅ All visualizations and maps

### What Stays the Same
- ✅ Raw data values (income, shares, etc.)
- ✅ Quartier classifications (Residential vs. non-residential)
- ✅ Data merging and aggregation logic
- ✅ GDI formula weights (1/8 for each component)
- ✅ Export formats and file structures

## References

**Methodological Justification:**
- Pooled standardization is standard practice for longitudinal analysis
- Enables detection of "period effects" (overall temporal trends)
- Used in: panel data analysis, growth mixture modeling, trajectory analysis
- Alternative name: "time-invariant standardization"

**Similar Approaches:**
- Fixed-effects models (economics)
- Grand-mean centering (multilevel modeling)
- Baseline-referenced scoring (psychology)

---

**Implementation Date**: October 22, 2025
**Tested**: ✅ Cell execution successful
**Validated**: ✅ Output shows expected temporal evolution
**Ready for**: Downstream analysis re-execution
