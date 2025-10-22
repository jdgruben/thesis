# Education Datasets - Documentation

## Date: October 22, 2025

## Overview

Three new education datasets have been added to the project, covering higher education attainment levels at IRIS level for Paris intra-muros across three census years.

## Datasets Loaded

### 1. EDUCATION 2013
- **Source File**: `education_2013.xlsx`
- **Google Drive ID**: `1JmDo7waeztZukDAskj1PUGvzawussYWC`
- **Processed File**: `datasets/education_2013_paris.parquet`
- **IRIS Count**: 992
- **Variable Extracted**: `P13_NSCOL15P_SUP` → `pop_bac3_plus`

**Description**: Population de 15 ans ou plus non scolarisée, titulaires d'un diplôme de l'enseignement supérieur (all higher education levels)

**Total Population**: 914,174 personnes
**Average per IRIS**: 921.5 personnes

**Note**: For 2013, INSEE did not subdivide higher education into Bac+2, Bac+3/4, and Bac+5+ categories. Therefore, this variable includes ALL higher education degrees.

---

### 2. EDUCATION 2017
- **Source File**: `education_2017.xlsx`
- **Google Drive ID**: `1ZyxFLSPaGfnVi29HjdxNoMlLh9XoeWye`
- **Processed File**: `datasets/education_2017_paris.parquet`
- **IRIS Count**: 992
- **Variable Extracted**: `P17_NSCOL15P_SUP34` → `pop_bac34_plus`

**Description**: Population de 15 ans ou plus non scolarisée, titulaires d'un diplôme de l'enseignement supérieur de niveau Bac+3 ou Bac+4

**Total Population**: 245,114 personnes
**Average per IRIS**: 247.1 personnes

**Note**: Starting in 2017, INSEE subdivided higher education into:
- `P17_NSCOL15P_SUP2`: Bac+2
- `P17_NSCOL15P_SUP34`: Bac+3/4 ✅ **SELECTED**
- `P17_NSCOL15P_SUP5`: Bac+5+

---

### 3. EDUCATION 2021
- **Source File**: `education_2021.xlsx`
- **Google Drive ID**: `1gP0FNOwIM3KPq8nVbL_oj9U_IPVJdHQW`
- **Processed File**: `datasets/education_2021_paris.parquet`
- **IRIS Count**: 992
- **Variable Extracted**: `P21_NSCOL15P_SUP34` → `pop_bac34_plus`

**Description**: Population de 15 ans ou plus non scolarisée, titulaires d'un diplôme de l'enseignement supérieur de niveau Bac+3 ou Bac+4

**Total Population**: 238,092 personnes
**Average per IRIS**: 240.0 personnes

**Note**: Same structure as 2017 with subdivided categories.

---

## Variable Naming Convention

### Renamed Columns

| Year | Original Variable | Renamed Variable | Description |
|------|------------------|------------------|-------------|
| 2013 | `P13_NSCOL15P_SUP` | `pop_bac3_plus` | All higher education |
| 2017 | `P17_NSCOL15P_SUP34` | `pop_bac34_plus` | Bac+3/4 only |
| 2021 | `P21_NSCOL15P_SUP34` | `pop_bac34_plus` | Bac+3/4 only |

### Why Different Column Names?

- **2013**: Variable named `pop_bac3_plus` because it includes ALL higher education (not just Bac+3/4)
- **2017/2021**: Variable named `pop_bac34_plus` to be specific about Bac+3/4 level only

## Data Quality

### Coverage
- ✅ All 3 datasets cover the same 992 IRIS zones in Paris
- ✅ No missing values in any dataset
- ✅ All IRIS codes are consistent (9-digit format starting with '75')

### Temporal Comparison Notes

⚠️ **IMPORTANT**: Direct comparison between 2013 and 2017/2021 should be done with caution:

1. **2013 variable is broader**: Includes Bac+2, Bac+3/4, AND Bac+5+
2. **2017/2021 variables are specific**: Only Bac+3/4

**For comparable analysis**, you may need to:
- Option 1: Use only 2017 and 2021 for Bac+3/4 trends
- Option 2: Sum SUP2 + SUP34 + SUP5 for 2017/2021 to match 2013 methodology
- Option 3: Accept that 2013 is an approximation and note the limitation

## Integration with GDI Analysis

### Potential Use Cases

1. **Add as 9th GDI Component**
   - Current GDI uses 8 components
   - Could add `share_bac34_plus` = (pop_bac34_plus / pop_15plus) * 100
   - Would make GDI more sensitive to educational gentrification

2. **Alternative Education Metric**
   - Replace or complement `share_cs3` (executives)
   - Education may be more stable/reliable than occupation

3. **Separate Analysis**
   - Educational gentrification vs. income gentrification
   - Correlation between education levels and GDI scores

### Suggested Variable Creation

```python
# For each year's census data:
census_2017['share_bac34_plus'] = (
    education_2017['pop_bac34_plus'] / census_2017['pop_15plus'] * 100
)
```

## File Locations

### Raw Data
- `/workspaces/thesis/raw_datasets/education_2013.xlsx` (37.1 MB)
- `/workspaces/thesis/raw_datasets/education_2017.xlsx` (26.5 MB)
- `/workspaces/thesis/raw_datasets/education_2021.xlsx` (29.2 MB)

### Processed Data
- `/workspaces/thesis/datasets/education_2013_paris.parquet`
- `/workspaces/thesis/datasets/education_2017_paris.parquet`
- `/workspaces/thesis/datasets/education_2021_paris.parquet`

## Loading Code

All education datasets are loaded in `/workspaces/thesis/notebooks/load_data.ipynb`:

- Section 2: EDUCATION datasets
- Cells: 11-16 (loading and verification)

## Next Steps

1. ✅ **Data loaded and verified**
2. 🔄 **Merge with existing datasets**
   - Join education data with census data on `code_iris`
   - Calculate `share_bac34_plus` percentage
3. 🔄 **Update V4_GDI.ipynb**
   - Add education share to the data pipeline
   - Consider adding to GDI formula (optional)
   - Analyze correlation with existing components
4. 🔄 **Analysis**
   - Educational gentrification patterns
   - Relationship between education and income/occupation
   - Temporal trends in higher education attainment

## Technical Notes

### Data Type
- `code_iris`: object (string)
- `pop_bac3_plus` / `pop_bac34_plus`: float64

### Missing Values
- **0 missing values** in all datasets

### Coordinate System
- Not applicable (no geometry in these datasets)
- Will inherit geometry from IRIS GeoJSON after merge

---

**Implementation Date**: October 22, 2025
**Loaded by**: GitHub Copilot
**Status**: ✅ Complete and verified
**Ready for**: Integration with GDI analysis
