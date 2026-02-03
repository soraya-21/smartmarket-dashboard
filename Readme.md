# Dashboard de Pilotage Marketing - SmartMarket
Le rapport a été déployé au lien suivant :
https://smartmarket-super-dashboard.streamlit.app/

## Aperçu du Projet
Ce projet consiste en une application de Business Intelligence (BI) développée avec **Streamlit**. L'objectif est d'offrir une vision claire et actionnable de la performance des campagnes marketing de SmartMarket pour la période de **septembre 2025**.

Le tableau de bord permet de réconcilier des données provenant de sources hétérogènes pour mesurer la rentabilité des investissements (ROI) et la qualité de la transformation commerciale.

---

## Fonctionnalités Clés
* **Analyse de Performance** : Suivi en temps réel du CPL (Coût par Lead) et du CTR (Taux de clic).
* **Suivi de la Qualité CRM** : Visualisation du passage des prospects par les stades MQL, SQL et Active.
* **Segmentation Avancée** : Analyse des leads par secteur d'activité et par terminal (Appareil) utilisé.
* **Exploration Granulaire** : Accès aux registres de données consolidés et nettoyés.

---

## Structure des Données
L'application traite et fusionne trois sources de données principales :
1.  **Leads (CSV)** : Données de navigation et origine des prospects (`lead_id`, `date`, `canal`, `device`).
2.  **Campagnes (JSON)** : Métriques publicitaires (`coûts`, `impressions`, `clics`, `conversions`).
3.  **CRM (Excel)** : Suivi commercial (`statut`, `secteur d'activité`, `taille d'entreprise`).

**Périmètre :** Un filtrage temporel est appliqué pour isoler uniquement le mois de septembre 2025.

---

## Installation et Utilisation

### Prérequis
* Python 3.8 ou supérieur.
* Gestionnaire de paquets `pip`.

### Installation des dépendances
```bash
pip install -r requirements.txt