# FILOSOFI Missing Values: Detection & Imputation Summary

## Overview

Simplified missing value handling for FILOSOFI datasets (2017 and 2021) with clear detection by IRIS type and appropriate imputation strategies.

---

## FILOSOFI 2017: Single Missing Row

**Total IRIS**: 871

| Metric | Count | % |
|--------|-------|---|
| **Missing** | 1 | 0.1% |
| **Complete** | 870 | 99.9% |

### Missing Row Details
- **Code IRIS**: 751145625
- **Quartier**: Plaisance 25 (14th arr.)
- **IRIS Type**: A (Activity)

### Imputation Strategy
- **Method**: Median of arrondissement (14th arr.)
- **Median income filled**: 29,010€
- **Result**: ✅ Complete imputation - 0 missing values

---

## FILOSOFI 2021: Structured Missing by IRIS Type

**Total IRIS**: 992
**Total Missing Before Imputation**: 128 (12.9%)

### Missing Values by IRIS Type

| IRIS Type | Definition | Total | Missing | % Missing | Imputation |
|-----------|-----------|-------|---------|-----------|-----------|
| **H** | Housing (residential) | 861 | 9 | 1.0% | ✅ Imputed |
| **D** | Diversified (mixed use) | 43 | 43 | 100% | ⚠ Left as NaN |
| **A** | Activity (industrial/commercial) | 88 | 76 | 86.4% | ⚠ Left as NaN |

### Imputation Rationale

#### H (Housing IRIS) - ✅ IMPUTED
**Reason**: Residential IRIS should have income data; missing values are likely data suppression errors
- **Method**: Median of same arrondissement (H-type IRIS only)
- **Result**: 9 missing → 0 missing
- **Logic**: Housing areas in same arrondissement have similar income characteristics

#### D (Diversified IRIS) - ⚠ NOT IMPUTED
**Reason**: Mixed-use IRIS are heterogeneous; cannot rely on arrondissement median
- **Missing**: 43/43 (100%)
- **Decision**: Leave as NaN for sensitivity analysis
- **Note**: D-type IRIS vary too much internally; imputation would introduce bias

#### A (Activity IRIS) - ⚠ NOT IMPUTED
**Reason**: Industrial/commercial areas lack residential population income
- **Missing**: 76/88 (86.4%)
- **Decision**: Leave as NaN; these areas are not part of gentrification analysis
- **Note**: Activity zones have no "median household income" - the metric is undefined for A-type IRIS

---

## Implementation Details

### Suppression Codes Replaced with NaN
```python
suppression_codes = {'s', 'c', 'S', 'C', 'ns', 'nd', 'so'}
```
These are INSEE statistical secrecy codes indicating data withheld for confidentiality.

### Numeric Columns Processed
- `median_uc`: Median income per consumption unit
- `q1_uc`: 1st quartile income
- `q3_uc`: 3rd quartile income
- `d9d1_ratio`: Ratio of 90th to 10th percentile (income inequality)
- `gini`: Gini coefficient (income inequality)
- `share_activity_income`: Share of income from employment
- `share_pensions`: Share of income from pensions
- `share_social_benefits`: Share of income from social benefits

### French Format Conversion
FILOSOFI data uses comma as decimal separator (French locale):
- Example: `"29.010,50"` → `29010.5`
- Conversion: Replace `','` with `'.'` then `pd.to_numeric()`

---

## Results Summary

### Before Imputation
- FILOSOFI 2017: 1 missing (0.1%)
- FILOSOFI 2021: 128 missing (12.9%)
  - H: 9 missing (1.0%)
  - D: 43 missing (100%)
  - A: 76 missing (86.4%)

### After Imputation
- FILOSOFI 2017: **0 missing** ✅
- FILOSOFI 2021: **119 missing** (expected - D and A types)
  - H: **0 missing** ✅ (imputed)
  - D: 43 missing (unchanged - too heterogeneous)
  - A: 76 missing (unchanged - no residential income)

---

## Quality Assurance

### Validation Checks
1. ✅ All numeric columns converted to float64
2. ✅ Suppression codes replaced with NaN
3. ✅ French decimal format standardized
4. ✅ H-type imputation verified (median of arrondissement)
5. ✅ D and A types correctly left as NaN (policy decision)

### Data Integrity
- **No values removed**: All non-missing data preserved
- **Imputation transparent**: Marked which rows were imputed (D and A left as NaN in analysis)
- **Arrondissement-level**: Imputation uses local neighborhood (same arrondissement), not global median

---

## Usage in Analysis

### For Gentrification Analysis (GDI)
- **Use**: H-type IRIS only (residential areas)
  - All H-type IRIS now have complete income data
  - Analysis unbiased by missing values
  
- **Exclude**: D and A-type IRIS
  - D-type: Mixed-use; income not meaningful for residential gentrification
  - A-type: Activity zones; no residential population
  
- **Result**: Clean dataset of **861 housing IRIS** with complete income data

### Implication
The 119 remaining missing values (D and A types) do not affect gentrification analysis, as these IRIS types are excluded from residential gentrification studies by design.

---

## Code Location

**Notebook**: `V3_EDA.ipynb`
**Cell**: Data type conversion and imputation
**Function**: `clean_filosofi()` (inline)

**Output Visualization**: `filosofi_missing_values_summary.png`
- Chart showing missing values by IRIS type before imputation
- Summary table showing all types and imputation decisions

---

## Conclusion

The simplified imputation approach successfully addresses FILOSOFI missing values:
- ✅ FILOSOFI 2017: Fully imputed (1 row)
- ✅ FILOSOFI 2021 H-type: Fully imputed (9 rows)
- ⚠ FILOSOFI 2021 D-type: Intentionally left as NaN (design decision)
- ⚠ FILOSOFI 2021 A-type: Intentionally left as NaN (design decision)

The approach balances completeness (H-type imputation) with analytical integrity (D and A types excluded).
