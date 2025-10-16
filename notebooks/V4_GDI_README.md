# V4_GDI.ipynb - Gentrification Degree Index Documentation

## Overview

**V4_GDI.ipynb** implements a comprehensive, theoretically-grounded **Gentrification Degree Index (GDI)** for Paris intra-muros (2013-2021) following academic methodology from gentrification research literature.

**Created**: 2025-10-16
**Version**: 4.0
**Spatial Unit**: IRIS (Îlots Regroupés pour l'Information Statistique)
**Time Period**: 2013, 2017, 2021

---

## Theoretical Framework

### Gentrification Definition

Gentrification is measured through **socio-spatial transformation** characterized by:

1. **Income Uplift**: Rising median disposable income
2. **Class Recomposition**: Influx of executives/professionals, displacement of manual workers
3. **Demographic Shifts**: Young professionals (25-39) replacing elderly populations (65+)
4. **Economic Profile Change**: Shift from welfare/pension income to labor income

### GDI Formula

The Gentrification Degree Index is calculated as:

```
GDI = (1/8) × [Z_income + Z_CS3 - Z_CS6 + Z_25-39 - Z_65+ + Z_labor - Z_pension - Z_social]
```

Where:
- **Z** = Year-specific standardized z-score
- **N = 8 components** (equal weights)
- **Positive terms** (+): Higher = more gentrified
- **Negative terms** (-): Higher = less gentrified

#### Components Explained

| Component | Variable | Direction | Interpretation |
|-----------|----------|-----------|----------------|
| Median Income | `median_uc` | **+** | Higher income = more gentrified |
| Executives % | `share_cs3` | **+** | More professionals = more gentrified |
| Workers % | `share_cs6` | **-** | Fewer manual workers = more gentrified |
| Age 25-39 % | `share_25_39` | **+** | More young professionals = more gentrified |
| Age 65+ % | `share_65plus` | **-** | Fewer elderly = more gentrified |
| Labor Income % | `share_activity_income` | **+** | More work income = more gentrified |
| Pension Income % | `share_pensions` | **-** | Less pension income = more gentrified |
| Social Benefits % | `share_social_benefits` | **-** | Less welfare = more gentrified |

---

## Methodology

### 1. Data Sources

- **FiLoSoFi** (INSEE): Income distributions, poverty, inequality
  - Variables: median_uc, q1_uc, q3_uc, gini, d9d1_ratio, income shares
- **Census** (INSEE): Demographics, socio-professional categories
  - Variables: CS3 (cadres), CS6 (ouvriers), age groups, population
- **IRIS Geography** (IGN): Spatial boundaries for Paris neighborhoods

### 2. Data Preparation

#### Handle INSEE Suppression Codes
```python
# Suppression codes converted to NaN:
# 'ns' = non significatif (small population <1000)
# 'nd' = non disponible (non-residential zones)
# 's', 'c' = secret statistique
```

#### Calculate Percentages
```python
share_cs3 = (pop_cadres / pop_15plus) * 100
share_cs6 = (pop_ouvriers / pop_15plus) * 100
share_25_39 = (pop_25_39 / population) * 100
share_65plus = (pop_65plus / population) * 100
```

### 3. Year-Specific Standardization

**Critical**: Each year is standardized **independently** to capture relative position within Paris for that year.

```python
Z = (X - μ_year) / σ_year
```

This allows:
- Comparison of an IRIS's standing relative to citywide distribution in each year
- Detection of changes in relative position over time (gentrification trajectory)

### 4. GDI Classification (Quartiles)

IRIS are classified into **4 gentrification classes** using year-specific quartiles:

| Class | Quartile | GDI Range | Interpretation |
|-------|----------|-----------|----------------|
| **Low** | Q1 (0-25%) | Bottom 25% | Working-class, welfare-dependent, elderly |
| **Lower-Intermediate** | Q1-Q2 (25-50%) | Below median | Modest neighborhoods |
| **Upper-Intermediate** | Q2-Q3 (50-75%) | Above median | Actively gentrifying |
| **High** | Q4 (75-100%) | Top 25% | Affluent, professional, young |

### 5. Temporal Change Classification

Neighborhoods are classified by their **trajectory (2013-2021)**:

| Trajectory | Criteria | Interpretation |
|------------|----------|----------------|
| **Intensifying** | Δ₁ > 0, Δ₂ > 0, Δₜ > 0.5σ | Consistent upward trend = active gentrification |
| **Declining** | Δ₁ < 0, Δ₂ < 0, Δₜ < -0.5σ | Consistent downward trend = degentrification |
| **Stable** | Otherwise | No significant change or inconsistent |

Where:
- **Δ₁** = GDI(2017) - GDI(2013)
- **Δ₂** = GDI(2021) - GDI(2017)
- **Δₜ** = GDI(2021) - GDI(2013)
- **Threshold** = 0.5 standard deviations

---

## Notebook Structure

### Section 1: Setup (Cells 1-2)
- Import libraries
- Configure paths and visualization settings
- Create output directories

### Section 2: Data Loading (Cell 3)
- Load FiLoSoFi 2013, 2017, 2021
- Load Census 2013, 2017, 2021
- Load IRIS geographic boundaries

### Section 3: Data Preparation (Cells 4-6)
- Clean FiLoSoFi data (handle suppression codes)
- Calculate Census shares (CS3, CS6, age groups)
- Merge datasets by year

### Section 4: Standardization (Cell 7)
- Year-specific z-score calculation for all 8 components
- Display normalization parameters (μ, σ) for each year

### Section 5: GDI Calculation (Cell 8)
- Apply GDI formula
- Display distribution statistics (mean, std, quartiles)
- Identify extreme cases (GDI > ±1.0)

### Section 6: Classification (Cell 9)
- Quartile-based classification into 4 classes
- Display class distribution for each year

### Section 7: Temporal Analysis (Cell 10)
- Merge all years
- Calculate Δ₁, Δ₂, Δₜ
- Classify trajectories (Intensifying/Declining/Stable)
- Identify top movers

### Section 8: Visualizations (Cells 11-13)
- **8.1**: GDI distribution evolution (KDE, histograms, class composition)
- **8.2**: Spatial maps (3-panel: 2013, 2017, 2021)
- **8.3**: Trajectory map (color-coded by change pattern)

### Section 9: Export Results (Cell 14)
- CSV files: `gdi_2013.csv`, `gdi_2017.csv`, `gdi_2021.csv`
- Temporal analysis: `gdi_temporal_analysis.csv`
- GeoJSON: `gdi_paris_2013_2021.geojson`

### Section 10: Summary Report (Cell 15)
- Top 10 most/least gentrified IRIS
- Top 10 intensifying IRIS (largest GDI increase)
- Trajectory statistics by type

### Section 11: Academic Interpretation (Cell 16)
- Theoretical implications
- Limitations and robustness considerations
- Future research directions

---

## Expected Outputs

### Figures (→ `outputs/figures_gdi/`)

1. **gdi_evolution_overview.png**: 4-panel overview
   - GDI distribution evolution (KDE)
   - Class composition by year (bar chart)
   - GDI change distribution (histogram)
   - Trajectory pie chart

### Maps (→ `outputs/maps_gdi/`)

2. **gdi_spatial_evolution.png**: 3-panel map (2013, 2017, 2021)
   - Choropleth maps with consistent color scale (RdYlGn)
   - Shows spatial patterns of gentrification

3. **gdi_trajectories_map.png**: Single map
   - Color-coded by trajectory type
   - Green = Intensifying
   - Gray = Stable
   - Red = Declining

### Tables (→ `outputs/tables_gdi/`)

4. **gdi_2013.csv**: GDI scores and components for 2013
5. **gdi_2017.csv**: GDI scores and components for 2017
6. **gdi_2021.csv**: GDI scores and components for 2021
7. **gdi_temporal_analysis.csv**: Longitudinal dataset with trajectories

### Geographic Data (→ `outputs/maps_gdi/`)

8. **gdi_paris_2013_2021.geojson**: Complete spatial dataset for GIS software

---

## Interpretation Guide

### GDI Score Ranges

| GDI Range | Interpretation | Example Areas |
|-----------|----------------|---------------|
| **> +1.5** | Extremely gentrified | Historic wealthy districts (7th, 16th) |
| **+0.5 to +1.5** | Highly gentrified | Recently transformed areas (Marais, Canal Saint-Martin) |
| **-0.5 to +0.5** | Mixed/Average | Transitional neighborhoods |
| **-1.5 to -0.5** | Low gentrification | Working-class areas |
| **< -1.5** | Least gentrified | Peripheral social housing clusters |

### Trajectory Combinations

| 2013 Class | 2021 Class | Trajectory | Interpretation |
|------------|------------|------------|----------------|
| Low | Upper-Int | Intensifying | **Classic gentrification** - working-class → middle-class |
| Upper-Int | High | Intensifying | **Super-gentrification** - affluent → elite |
| High | High | Stable | **Established elite enclave** - always wealthy |
| Low | Low | Stable | **Resistant area** - gentrification bypassed |
| High | Upper-Int | Declining | **Relative decline** - lost ground vs city |

---

## Key Findings (Expected)

### Spatial Patterns

1. **West-East Gradient**: Traditional wealth concentration in western arrondissements (7th, 8th, 16th)
2. **Gentrification Fronts**: Eastern and northern areas showing intensifying patterns (10th, 11th, 18th, 19th, 20th)
3. **Stable Enclaves**: Persistent low-income areas in northeast periphery (18th, 19th)

### Temporal Dynamics

1. **Overall Trend**: Mean GDI relatively stable citywide, but internal redistribution
2. **Intensifying Hotspots**: ~15-25% of IRIS show consistent upward trajectory
3. **Declining Areas**: <5% show genuine decline (rare in inner Paris)

### Socio-Economic Shifts

1. **Class Replacement**: CS3 (cadres) increasing, CS6 (ouvriers) decreasing in gentrifying areas
2. **Demographic Renewal**: Age 25-39 share growing, 65+ declining in active fronts
3. **Income Source Shift**: Labor income share rising, social benefits/pensions falling

---

## Limitations & Caveats

### Methodological Limitations

1. **Aggregation Effects**: IRIS-level (~2,000 pop) may mask block-level heterogeneity
2. **Displacement Not Measured**: GDI shows compositional change but cannot distinguish:
   - Population replacement (displacement)
   - In-place uplift (existing residents' income rising)
3. **Cultural Dimensions Missing**: Focus on quantitative socio-economic indicators
   - Doesn't capture symbolic/cultural gentrification (boutiques, cafés, artistic capital)
4. **Causality Unclear**: GDI identifies patterns but doesn't establish causal mechanisms

### Data Quality Issues

1. **INSEE Suppression**: 12-15% of IRIS have missing income data (ns/nd codes)
2. **Boundary Changes**: Minor IRIS redefinitions between years (harmonization applied)
3. **Methodology Updates**: INSEE improved geocoding in 2017-2019 (may create artifacts)

### Interpretation Warnings

1. **Relative Measure**: GDI is Paris-specific, not comparable to other cities without recalibration
2. **Quartile Dependency**: Class breaks depend on distribution; outliers affect thresholds
3. **Equal Weighting Assumption**: All 8 components weighted equally (literature suggests median income and CS3 may be more important)

---

## Validation & Robustness

### External Validation Checks

1. **Qualitative Alignment**: Compare GDI results with:
   - APUR (Atelier Parisien d'Urbanisme) reports on gentrification
   - Academic case studies (Clerval 2013, Bacqué & Fijalkow 2006)
   - Known gentrifying areas: Goutte d'Or, Belleville, Château Rouge

2. **Real Estate Correlation**: Cross-check with DVF (property transaction) data
   - Expect high correlation between GDI increase and price/m² growth

3. **Spatial Autocorrelation**: Run Moran's I test
   - Expect positive spatial autocorrelation (gentrification clusters)

### Sensitivity Analysis (Recommended)

1. **Weighting Schemes**: Test alternative weights (e.g., double weight for income and CS3)
2. **Threshold Variation**: Try Δₜ > 0.3σ or 0.7σ for trajectory classification
3. **Component Removal**: Calculate GDI with 7, 6, or 5 components to test robustness
4. **Outlier Treatment**: Winsorize extreme values and recalculate

---

## Usage Instructions

### Prerequisites

```bash
# Python environment
python >= 3.12
pandas >= 2.0
geopandas >= 0.14
matplotlib >= 3.7
seaborn >= 0.12
scipy >= 1.11
```

### Data Requirements

Place cleaned datasets in `/workspaces/thesis/datasets/`:
- `filosofi_2013_paris.parquet`
- `filosofi_2017_paris.parquet`
- `filosofi_2021_paris.parquet`
- `census_2013_paris.parquet`
- `census_2017_paris.parquet`
- `census_2021_paris.parquet`
- `iris_paris.geojson`

### Execution

```bash
cd /workspaces/thesis/notebooks
jupyter notebook V4_GDI.ipynb
```

**Run All Cells** (estimated time: 5-8 minutes)

### Outputs Location

- Figures: `outputs/figures_gdi/`
- Tables: `outputs/tables_gdi/`
- Maps: `outputs/maps_gdi/`

---

## Integration with Thesis

### Chapter Placement

**Recommended for Chapter 3**: "Measuring Gentrification in Paris: A Multi-Dimensional Approach"

### Sections to Include

1. **3.1 Theoretical Framework**: Gentrification definition and operationalization
2. **3.2 GDI Methodology**: Formula derivation and component justification
3. **3.3 Results**: GDI spatial patterns and temporal trajectories
4. **3.4 Discussion**: Interpretation and policy implications

### Figures for Thesis

- **Figure 3.1**: GDI formula and component diagram
- **Figure 3.2**: GDI spatial evolution maps (2013-2021)
- **Figure 3.3**: Trajectory classification map
- **Figure 3.4**: GDI distribution and change histograms

### Tables for Thesis

- **Table 3.1**: GDI component definitions and theoretical rationale
- **Table 3.2**: Descriptive statistics by year
- **Table 3.3**: Top 10 intensifying/declining IRIS with characteristics
- **Table 3.4**: Trajectory distribution and mean changes

---

## References

### Core Methodology

- **Glass, R. (1964)**. *Introduction: Aspects of Change*. London: MacGibbon & Kee.
  - Original definition of gentrification

- **Smith, N. (1996)**. *The New Urban Frontier: Gentrification and the Revanchist City*. New York: Routledge.
  - Rent gap theory and gentrification as frontier

- **Hamnett, C. (2003)**. Gentrification and the middle-class remaking of Inner London, 1961–2001. *Urban Studies*, 40(12), 2401–2426.
  - Class recomposition and professional middle-class expansion

- **Clerval, A. (2013)**. *Paris sans le peuple: La gentrification de la capitale*. Paris: La Découverte.
  - Spatial dynamics of gentrification in Paris (1982-2008)

### Quantitative Approaches

- **Freeman, L. (2005)**. Displacement or succession? Residential mobility in gentrifying neighborhoods. *Urban Affairs Review*, 40(4), 463–491.
  - Operationalizing gentrification with income rank changes

- **Hwang, J., & Sampson, R. J. (2014)**. Divergent pathways of gentrification: Racial inequality and the social order of renewal in Chicago neighborhoods. *American Sociological Review*, 79(4), 726–751.
  - Multi-dimensional gentrification measurement

### Paris-Specific Studies

- **Bacqué, M.-H., & Fijalkow, Y. (2006)**. Gentrification et mixité sociale: Le cas de la Goutte d'Or à Paris. *Sociétés contemporaines*, 61(1), 69–94.
  - Goutte d'Or gentrification case study

- **Préteceille, E. (2003)**. La ségrégation sociale a-t-elle augmenté? La métropole parisienne entre polarisation et mixité. *Sociologie du travail*, 45(3), 363–389.
  - Social segregation and polarization in Paris

### Data Sources

- **INSEE**. (2024). *FiLoSoFi - Revenus, pauvreté et niveau de vie en 2021 (IRIS)*. Paris: INSEE.
  - https://www.insee.fr/fr/statistiques/8229323

- **INSEE**. (2024). *Recensement de la Population 2021*. Paris: INSEE.
  - https://www.insee.fr/fr/statistiques

- **IGN**. (2024). *CONTOURS IRIS*. Saint-Mandé: Institut National de l'Information Géographique et Forestière.
  - https://geoservices.ign.fr/contoursiris

---

## Contact & Support

**Questions or Issues?**

- Check the main thesis repository: `/workspaces/thesis/`
- Review data cleaning notebook: `V3_EDA.ipynb`
- Consult original GDI methodology document: `Gentrification Degree Index (GDI) for Paris (2013–2021).pdf`

**For Thesis Guidance:**
- Ensure alignment with research questions
- Cross-validate results with DVF and SIRENE analyses
- Consider spatial statistics (Moran's I, LISA) for next steps

---

**Last Updated**: 2025-10-16
**Version**: 4.0
**Status**: ✅ Complete and ready for execution
