# Datasets Éducation - Structure Finale

## Date: October 22, 2025

## 📊 Structure des Données

### EDUCATION 2013
**Colonnes** : `code_iris`, `pop_bac_sup`

| Colonne | Description | Total | Moyenne/IRIS |
|---------|-------------|-------|--------------|
| `pop_bac_sup` | Tous diplômes supérieurs (Bac+2/3/4/5+) | 914,174 | 921.5 |

**Note** : En 2013, l'INSEE ne subdivisait pas l'enseignement supérieur.

---

### EDUCATION 2017
**Colonnes** : `code_iris`, `pop_bac2`, `pop_bac34`, `pop_bac5_plus`, `pop_bac_sup`

| Colonne | Description | Total | Moyenne/IRIS |
|---------|-------------|-------|--------------|
| `pop_bac2` | Bac+2 uniquement | 133,482 | 134.6 |
| `pop_bac34` | Bac+3 et Bac+4 | 245,114 | 247.1 |
| `pop_bac5_plus` | Bac+5 et plus | 606,156 | 611.0 |
| **`pop_bac_sup`** | **TOTAL (somme des 3)** | **984,751** | **992.7** |

**Répartition** :
- Bac+2 : 13.6%
- Bac+3/4 : 24.9%
- Bac+5+ : 61.5%

---

### EDUCATION 2021
**Colonnes** : `code_iris`, `pop_bac2`, `pop_bac34`, `pop_bac5_plus`, `pop_bac_sup`

| Colonne | Description | Total | Moyenne/IRIS |
|---------|-------------|-------|--------------|
| `pop_bac2` | Bac+2 uniquement | 123,521 | 124.5 |
| `pop_bac34` | Bac+3 et Bac+4 | 238,092 | 240.0 |
| `pop_bac5_plus` | Bac+5 et plus | 642,412 | 647.6 |
| **`pop_bac_sup`** | **TOTAL (somme des 3)** | **1,004,025** | **1,012.1** |

**Répartition** :
- Bac+2 : 12.3%
- Bac+3/4 : 23.7%
- Bac+5+ : 64.0%

---

## 📈 Évolution Temporelle

### Population avec Diplôme Supérieur (Total)

```
Année    Total       Variation vs 2013
─────────────────────────────────────
2013    914,174     (baseline)
2017    984,751     +70,577 (+7.7%)
2021  1,004,025     +89,851 (+9.8%)
```

**Observation** : Augmentation continue du niveau d'éducation à Paris (+9.8% sur 8 ans)

---

### Évolution par Niveau (2017 → 2021)

```
Niveau      2017        2021        Variation    %
──────────────────────────────────────────────────
Bac+2      133,482    123,521     -9,961     -7.5%
Bac+3/4    245,114    238,092     -7,022     -2.9%
Bac+5+     606,156    642,412    +36,256     +6.0%
──────────────────────────────────────────────────
TOTAL      984,751  1,004,025    +19,274     +2.0%
```

**Tendance Clé** : 
- ⬇️ Diminution des Bac+2 et Bac+3/4
- ⬆️ **Forte augmentation des Bac+5+** (+6.0%)
- → Élévation du niveau d'éducation moyen

---

## 🎯 Colonnes pour Analyse GDI

### Colonne Comparable sur 3 Années
✅ **`pop_bac_sup`** : Disponible pour 2013, 2017, 2021
- Permet l'analyse temporelle cohérente
- Somme de tous les niveaux supérieurs

### Colonnes Détaillées (2017 & 2021 uniquement)
✅ **`pop_bac2`** : Bac+2
✅ **`pop_bac34`** : Bac+3/4 (votre demande initiale)
✅ **`pop_bac5_plus`** : Bac+5+

**Usage recommandé** :
- Pour analyse **2013-2017-2021** : Utiliser `pop_bac_sup`
- Pour analyse **2017-2021** uniquement : Utiliser les colonnes détaillées

---

## 💡 Utilisation pour le GDI

### Option 1 : Pourcentage Total Diplômés Supérieurs
```python
# Calculer le % de diplômés du supérieur
census_2017['share_bac_sup'] = (
    education_2017['pop_bac_sup'] / census_2017['pop_15plus'] * 100
)
```
**Avantage** : Comparable sur 2013, 2017, 2021

---

### Option 2 : Pourcentage Bac+3/4+ (2017 et 2021)
```python
# Calculer le % de Bac+3/4 et plus
census_2017['pop_bac34_plus'] = (
    education_2017['pop_bac34'] + education_2017['pop_bac5_plus']
)
census_2017['share_bac34_plus'] = (
    census_2017['pop_bac34_plus'] / census_2017['pop_15plus'] * 100
)
```
**Avantage** : Plus sélectif (exclut Bac+2), meilleur marqueur de gentrification

---

### Option 3 : Focus Bac+5+ (marqueur d'élite)
```python
# Calculer le % de Bac+5+
census_2017['share_bac5_plus'] = (
    education_2017['pop_bac5_plus'] / census_2017['pop_15plus'] * 100
)
```
**Avantage** : Très sélectif, capture l'élite éducative

---

## 📁 Fichiers Générés

### Datasets Finaux
```
datasets/
├── education_2013_paris.parquet  (2 colonnes)
├── education_2017_paris.parquet  (5 colonnes)
└── education_2021_paris.parquet  (5 colonnes)
```

### Structure Identique pour 2017 et 2021
```
['code_iris', 'pop_bac2', 'pop_bac34', 'pop_bac5_plus', 'pop_bac_sup']
```

### Structure pour 2013
```
['code_iris', 'pop_bac_sup']
```

---

## ✅ Cohérence Vérifiée

### Test : Somme des 3 Niveaux = Total

**2017** :
```
pop_bac2 + pop_bac34 + pop_bac5_plus = pop_bac_sup
133,482 + 245,114 + 606,156 = 984,751 ✅
```

**2021** :
```
pop_bac2 + pop_bac34 + pop_bac5_plus = pop_bac_sup
123,521 + 238,092 + 642,412 = 1,004,025 ✅
```

---

## 📊 Recommandation pour GDI

### Meilleure Variable : `share_bac34_plus`

**Pourquoi** :
1. ✅ Plus discriminant que "tout le supérieur"
2. ✅ Capture mieux la gentrification (Bac+3/4 + Bac+5+)
3. ✅ Corrélation attendue avec cadres/professions intellectuelles
4. ✅ Exclut Bac+2 qui peut être technique/moins gentrificateur

**Formule** :
```python
# Pour 2017 et 2021
share_bac34_plus = (pop_bac34 + pop_bac5_plus) / pop_15plus * 100

# Pour 2013 (approximation)
share_bac_sup = pop_bac_sup / pop_15plus * 100
```

**Ajout au GDI** (si souhaité) :
```python
# Nouvelle composante (9ème)
df['z_bac34_plus'] = standardize(df['share_bac34_plus'])

# GDI étendu
GDI = (z_income + z_cs3 - z_cs6 + z_age_25_39 - z_age_65plus + 
       z_labor - z_pension - z_social + z_bac34_plus) / 9
```

---

## 🔄 Prochaines Étapes

1. ✅ **Données chargées** : Les 3 fichiers sont prêts
2. 🔄 **Merger avec Census** : Joindre sur `code_iris`
3. 🔄 **Calculer les pourcentages** : `share_bac_sup`, `share_bac34_plus`, etc.
4. 🔄 **Intégrer à V4_GDI.ipynb** : Ajouter au pipeline d'analyse
5. 🔄 **Analyse de corrélation** : Vérifier lien avec autres variables GDI

---

**Date de création** : 22 octobre 2025
**Status** : ✅ Complet et vérifié
**Prêt pour** : Intégration avec analyse GDI
