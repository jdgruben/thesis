# Comparison: Year-Specific vs. Pooled Standardization

## Visual Comparison of Approaches

### OLD APPROACH: Year-Specific Standardization ❌

```
Year 2013:                Year 2017:                Year 2021:
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│ Mean = 0     │         │ Mean = 0     │         │ Mean = 0     │
│ SD = 1       │         │ SD = 1       │         │ SD = 1       │
│              │         │              │         │              │
│ Income:      │         │ Income:      │         │ Income:      │
│ μ = €30,419  │         │ μ = €31,748  │         │ μ = €34,145  │
│ σ = €6,500   │         │ σ = €7,200   │         │ σ = €8,100   │
└──────────────┘         └──────────────┘         └──────────────┘
     ↓ Z-score                ↓ Z-score                ↓ Z-score
Each year forced            Each year forced            Each year forced
to mean=0, sd=1            to mean=0, sd=1            to mean=0, sd=1
```

**Problem**: Quartier with income €32,000 has:
- 2013: z = (32000-30419)/6500 = **+0.24** (above average!)
- 2021: z = (32000-34145)/8100 = **-0.26** (below average!)

**Same income, opposite conclusions!** ❌

---

### NEW APPROACH: Pooled Standardization ✅

```
POOLED ACROSS ALL YEARS (2013, 2017, 2021):
┌────────────────────────────────────────────┐
│ Single Reference Distribution              │
│                                            │
│ Pooled Mean = 0 (by construction)          │
│ Pooled SD = 1 (by construction)            │
│                                            │
│ Income Component:                          │
│ μ_pooled = €32,104                        │
│ σ_pooled = €7,341                         │
│ (calculated from N=219 quartiers×3 years) │
└────────────────────────────────────────────┘
                    ↓
    Applied to ALL years using SAME parameters
                    ↓
┌──────────────┬──────────────┬──────────────┐
│ Year 2013    │ Year 2017    │ Year 2021    │
├──────────────┼──────────────┼──────────────┤
│ Mean: -0.136 │ Mean: +0.029 │ Mean: +0.107 │
│ (Real change!│ (Real change!│ (Real change!│
│  Not forced  │  Not forced  │  Not forced  │
│  to zero)    │  to zero)    │  to zero)    │
└──────────────┴──────────────┴──────────────┘
```

**Solution**: Quartier with income €32,000 has:
- 2013: z = (32000-32104)/7341 = **-0.01** (at pooled average)
- 2017: z = (32000-32104)/7341 = **-0.01** (still at pooled average)
- 2021: z = (32000-32104)/7341 = **-0.01** (still at pooled average)

**Same income = same z-score = valid comparison!** ✅

---

## Concrete Example: Quartier Evolution

### Scenario: Quartier "Belleville North"

#### Raw Data
| Year | Median Income | CS3 (Executives) | Labor Income | Age 25-39 |
|------|---------------|------------------|--------------|-----------|
| 2013 | €27,000       | 25%              | 75%          | 28%       |
| 2017 | €29,500       | 27%              | 80%          | 27%       |
| 2021 | €33,000       | 30%              | 83%          | 26%       |

**Observation**: Income increased by €6,000 (+22%), executives increased by +5pp, labor income +8pp

---

### OLD STANDARDIZATION (Year-Specific)

| Component         | 2013 Z-score | 2017 Z-score | 2021 Z-score | Δ Z-score |
|-------------------|--------------|--------------|--------------|-----------|
| Income            | -0.5         | -0.3         | -0.2         | +0.3      |
| CS3               | -1.0         | -0.6         | -0.1         | +0.9      |
| Labor Income      | -0.8         | -0.4         | -0.2         | +0.6      |
| **GDI**          | **-0.43**    | **-0.22**    | **-0.06**    | **+0.37** |

**Interpretation**: "Modest improvement in relative position"
- Quartier improved, but so did everyone else
- Hard to tell if this is real gentrification or citywide improvement
- Z-scores change even if the quartier stayed the same but others changed

---

### NEW STANDARDIZATION (Pooled)

**Pooled Parameters:**
- Income: μ=€32,104, σ=€7,341
- CS3: μ=30.87%, σ=5.71%
- Labor Income: μ=84.32%, σ=9.41%

| Component         | 2013 Z-score | 2017 Z-score | 2021 Z-score | Δ Z-score |
|-------------------|--------------|--------------|--------------|-----------|
| Income            | -0.70        | -0.35        | +0.12        | **+0.82** |
| CS3               | -1.03        | -0.68        | -0.15        | **+0.88** |
| Labor Income      | -0.99        | -0.46        | -0.14        | **+0.85** |
| **GDI**          | **-0.57**    | **-0.29**    | **+0.04**    | **+0.61** |

**Interpretation**: "Strong gentrification trajectory"
- Quartier moved from well below average (2013: z=-0.57)
- Through below average (2017: z=-0.29)
- To above average (2021: z=+0.04)
- This represents **real socioeconomic change** relative to the overall Paris distribution

---

## Impact on Trajectory Classification

### OLD APPROACH
```
Using ±0.5 SD threshold:

Significant Change: |Δ GDI| > 0.5
→ Belleville North: Δ = +0.37 → STABLE ❌

Problems:
- Many real changes classified as "stable"
- Threshold has no absolute meaning (varies by year)
- Hard to distinguish real vs. relative change
```

### NEW APPROACH
```
Using ±0.5 SD threshold:

Significant Change: |Δ GDI| > 0.5
→ Belleville North: Δ = +0.61 → UPWARD ✅

Benefits:
- Captures real socioeconomic transformation
- Threshold has absolute meaning (relative to 2013-2021 Paris)
- Clear distinction between real change and stability
```

---

## Statistical Implications

### Distribution of Mean GDI by Year

#### OLD APPROACH
```
Year    Mean GDI    SD GDI    Interpretation
────────────────────────────────────────────
2013     0.00       1.00     Forced by design
2017     0.00       1.00     Forced by design
2021     0.00       1.00     Forced by design
────────────────────────────────────────────
Temporal trend: UNDETECTABLE ❌
```

#### NEW APPROACH
```
Year    Mean GDI    SD GDI    Interpretation
────────────────────────────────────────────
2013    -0.136      0.535    Below pooled average
2017    +0.029      0.562    Near pooled average
2021    +0.107      0.557    Above pooled average
────────────────────────────────────────────
Temporal trend: +0.243 SD increase (GENTRIFICATION) ✅
Δ per year: +0.03 SD/year
```

---

## Mathematical Formulation

### OLD (Incorrect)
For each year $t \in \{2013, 2017, 2021\}$:

$$Z_{i,t} = \frac{X_{i,t} - \mu_t}{\sigma_t}$$

Where:
- $\mu_t$ = mean in year $t$ only
- $\sigma_t$ = standard deviation in year $t$ only

**Problem**: $\mu_{2013} \neq \mu_{2017} \neq \mu_{2021}$

Cannot compare $Z_{i,2013}$ with $Z_{i,2021}$ because they use different reference distributions!

---

### NEW (Correct)
For all years, using pooled parameters:

$$Z_{i,t} = \frac{X_{i,t} - \mu_{pooled}}{\sigma_{pooled}}$$

Where:
$$\mu_{pooled} = \frac{1}{N} \sum_{t=2013,2017,2021} \sum_{i=1}^{n_t} X_{i,t}$$

$$\sigma_{pooled} = \sqrt{\frac{1}{N-1} \sum_{t=2013,2017,2021} \sum_{i=1}^{n_t} (X_{i,t} - \mu_{pooled})^2}$$

With $N = n_{2013} + n_{2017} + n_{2021}$ = 73 + 73 + 73 = 219

**Solution**: Same reference distribution for all years → valid comparisons!

---

## Validation: Expected Patterns

### What Should We See?

✅ **Mean GDI can shift over time**
- Not forced to 0 each year
- Can detect citywide gentrification or decline
- Our result: -0.136 → +0.029 → +0.107 (increasing trend)

✅ **Standard deviation can vary by year**
- Not forced to 1 each year
- Can detect increasing/decreasing inequality
- Our result: 0.535 → 0.562 → 0.557 (slightly increasing variance)

✅ **Year-specific means differ from pooled means**
- Income 2013: €30,419 < €32,104 pooled (Paris was poorer in 2013)
- Income 2021: €34,145 > €32,104 pooled (Paris is richer in 2021)
- This is EXPECTED and shows real economic growth!

✅ **Z-scores are interpretable across years**
- z = 0 means "at 2013-2021 Paris average" in all years
- z = +1 means "1 SD above 2013-2021 Paris average" in all years
- Changes in z reflect real socioeconomic change

---

## Conclusion

| Aspect | Year-Specific ❌ | Pooled ✅ |
|--------|-----------------|----------|
| **Valid temporal comparison** | No | Yes |
| **Detects citywide trends** | No | Yes |
| **Interpretable changes** | No | Yes |
| **Consistent baseline** | No | Yes |
| **Real vs. relative change** | Cannot distinguish | Can distinguish |
| **Scientific validity** | Low | High |
| **Recommended for longitudinal data** | No | **Yes** |

**Bottom Line**: Pooled standardization is the **only valid approach** for comparing gentrification over time. Year-specific standardization creates an illusion of stability by forcing each year to the same distribution, masking real socioeconomic change.

---

**Implementation**: ✅ Complete as of October 22, 2025
**Status**: Active in `V4_GDI.ipynb` Cell [50]
**Next**: Re-run all downstream analyses to propagate corrected values
