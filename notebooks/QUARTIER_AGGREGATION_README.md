# Changement d'échelle: IRIS → Quartiers IRIS

## Vue d'ensemble

Les notebooks V3_EDA.ipynb et V4_GDI.ipynb ont été modifiés pour passer d'une analyse au niveau **IRIS individuel** à une analyse au niveau **quartier IRIS**.

## Transformation des données

### Principe

Les noms d'IRIS à Paris suivent un pattern: `"Nom du Quartier X"` où X est un numéro (1-22+).

**Exemple:**
- `"Amérique 1"`, `"Amérique 2"`, ... `"Amérique 15"` → **`"Amérique"`**
- `"Charonne 22"` → **`"Charonne"`**

### Fonction d'extraction

```python
def extract_iris_quartier(nom_iris):
    """
    Extrait le nom du quartier IRIS en enlevant le numéro final.
    """
    import re
    return re.sub(r'\s+\d+$', '', str(nom_iris))
```

## Agrégation des données

### Méthodes d'agrégation par type de variable

| Type de variable | Méthode | Exemples |
|-----------------|---------|----------|
| Revenus (médiane, Q1, Q3) | **Médiane** des médianes IRIS | `median_uc`, `q1_uc`, `q3_uc` |
| Ratios/Indices | **Médiane** | `d9d1_ratio`, `gini` |
| Parts/Pourcentages | **Moyenne** | `share_cs3`, `share_activity_income` |

### Géométries

Les géométries IRIS sont **fusionnées** (dissolved) par quartier pour créer des polygones continus représentant chaque quartier.

## Impact sur les analyses

### V3_EDA.ipynb

- **Avant:** 973 IRIS individuels
- **Après:** ~94 quartiers IRIS
- Les statistiques descriptives, visualisations et analyses spatiales sont maintenant au niveau quartier

### V4_GDI.ipynb (Gentrification Dynamics Index)

- **Avant:** 992 IRIS (dont certains avec données manquantes)
- **Après:** 94 quartiers
- Le GDI est calculé au niveau quartier, permettant:
  - Plus de stabilité statistique (échantillons plus grands)
  - Réduction des données manquantes (agrégation)
  - Meilleure cohérence territoriale

## Avantages de cette approche

1. **Réduction du bruit statistique**: Agrégation de plusieurs IRIS réduit la variabilité due aux petits effectifs
2. **Meilleure interprétabilité**: Les quartiers correspondent à des unités territoriales connues
3. **Moins de valeurs manquantes**: L'INSEE supprime parfois des données IRIS individuels (<1000 habitants), l'agrégation permet de récupérer ces informations
4. **Compatibilité avec analyses urbaines**: Les quartiers sont souvent l'échelle pertinente pour les politiques publiques

## Structure du code

### 1. Création du mapping (après chargement des données)

```python
iris_geo['quartier_iris'] = iris_geo['nom_iris'].apply(extract_iris_quartier)
iris_mapping = iris_geo[['code_iris', 'quartier_iris']].drop_duplicates()
iris_quartiers = iris_geo.dissolve(by='quartier_iris', as_index=False, aggfunc='first')
```

### 2. Ajout du quartier_iris aux datasets

Les fonctions de nettoyage (`clean_filosofi_data`, `calculate_census_shares`) ajoutent automatiquement la colonne `quartier_iris` via merge avec `iris_mapping`.

### 3. Agrégation avant analyse

```python
filosofi_agg = filosofi_df.groupby('quartier_iris').agg({
    'median_uc': 'median',
    'gini': 'median',
    'share_activity_income': 'mean',
    ...
})
```

## Fichiers modifiés

- `notebooks/V3_EDA.ipynb` - Analyse exploratoire des données
- `notebooks/V4_GDI.ipynb` - Calcul de l'indice de gentrification
- `notebooks/QUARTIER_AGGREGATION_README.md` - Cette documentation

## Notes techniques

- La colonne `code_iris` reste l'identifiant unique au niveau IRIS original
- Une nouvelle colonne `quartier_iris` est ajoutée à tous les datasets
- Les géométries quartier sont stockées dans `iris_quartiers` GeoDataFrame
- Les résultats (cartes, tableaux, fichiers de sortie) utilisent maintenant `quartier_iris` comme identifiant
