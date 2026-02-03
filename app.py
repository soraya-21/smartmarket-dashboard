import streamlit as st
import pandas as pd
import json
import plotly.express as px

st.set_page_config(
    page_title="Tableau de bord Marketing SmartMarket - Septembre 2025",
    layout="wide"
)

st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 28px; color: #1E3A8A; }
    .main { background-color: #F8FAFC; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_and_clean_data():
    try:
        df_leads = pd.read_csv('leads_smartmarket.csv')
        df_campaigns = pd.read_json('campaign_smartmarket.json')
        df_crm = pd.read_excel('crm_smartmarket.xlsx')
    except Exception as e:
        st.error(f"Erreur lors de la lecture des fichiers : {e}")
        st.stop()

    df_crm = df_crm.rename(columns={'industry': 'sector', 'subscription_status': 'status'})
    df_campaigns = df_campaigns.rename(columns={'budget': 'cost'})

    # Fusion et filtrage temporel (Périmètre : Septembre 2025)
    df_merged = pd.merge(df_leads, df_crm, on='lead_id', how='left')
    df_merged['date'] = pd.to_datetime(df_merged['date'])
    mask = (df_merged['date'] >= '2025-09-01') & (df_merged['date'] <= '2025-09-30')
    df_final = df_merged.loc[mask].copy()

    # Calcul des indicateurs de performance (KPI)
    df_campaigns['CTR'] = (df_campaigns['clicks'] / df_campaigns['impressions']) * 100
    df_campaigns['Conv_Rate'] = (df_campaigns['conversions'] / df_campaigns['clicks']) * 100
    df_campaigns['CPL'] = df_campaigns['cost'] / df_campaigns['conversions']
    
    return df_final, df_campaigns

df_final, df_campaigns = load_and_clean_data()

with st.sidebar:
    st.header("Paramètres et Filtres")
    
    canaux_list = list(df_campaigns['channel'].unique())
    
    canaux_selectionnes = st.multiselect(
        label="Sélectionner les canaux :", 
        options=canaux_list, 
        default=canaux_list
    )
    
    st.divider()
    
    st.subheader("Glossaire des indicateurs")
    st.info("""
        ### Indicateurs Publicitaires
        **CTR (Click-Through Rate)** : Taux de clic. Mesure l'attractivité de l'annonce par rapport au nombre d'affichages.
        
        **CPL (Cost Per Lead)** : Coût par prospect généré. Permet de mesurer la rentabilité financière de chaque canal.
        
        **Conv. Rate** : Taux de conversion du clic vers le lead. Mesure l'efficacité de votre site à transformer un visiteur en prospect.
        
        **Impressions** : Nombre total de fois où l'annonce a été affichée.
        
        ---
        ### Qualification CRM
        **MQL (Marketing Qualified Lead)** : Prospect ayant montré un intérêt via le marketing (ex: formulaire) mais nécessitant encore une maturation.
        
        **SQL (Sales Qualified Lead)** : Prospect validé par le marketing et jugé prêt par les commerciaux pour une offre directe.
        
        **Active** : Prospect ayant finalisé un achat ou signé un contrat. Il est officiellement devenu client.
        """)

df_f_final = df_final[df_final['channel'].isin(canaux_selectionnes)]
df_f_camp = df_campaigns[df_campaigns['channel'].isin(canaux_selectionnes)]

tab1, tab2, tab3 = st.tabs([
    "Performance Globale", 
    "Analyses Détaillées", 
    "Exploration des Données", 
])

with tab1:
    st.header("Indicateurs de Performance Globale")
    
    col1, col2, col3, col4 = st.columns(4)
    total_leads = len(df_f_final)
    total_spend = df_f_camp['cost'].sum()
    avg_cpl = total_spend / total_leads if total_leads > 0 else 0
    
    col1.metric("Leads Générés", f"{total_leads}")
    col2.metric("Budget Investi", f"{total_spend:,.0f} €")
    col3.metric("CPL Moyen", f"{avg_cpl:.2f} €")
    col4.metric("CTR Moyen", f"{df_f_camp['CTR'].mean():.2f} %")
    
    st.divider()
    
    c1, c2 = st.columns(2)
    
    with c1:
        fig_cpl = px.bar(
            df_f_camp.sort_values('CPL'),
            x='channel', y='CPL',
            title="Comparaison du Coût par Lead (CPL) par Canal",
            labels={'channel': 'Canal', 'CPL': 'Coût par Lead (€)'},
            color_discrete_sequence=['#1E3A8A']
        )
        st.plotly_chart(fig_cpl, use_container_width=True)
        
    with c2:
        status_data = pd.crosstab(df_f_final['channel'], df_f_final['status']).reset_index()
        fig_status_canal = px.bar(
            status_data, 
            x='channel', 
            y=status_data.columns[1:], 
            title="Répartition des Statuts CRM par Canal",
            labels={'channel': 'Canal', 'value': 'Nombre de Leads', 'variable': 'Statut'},
            barmode='stack',
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        st.plotly_chart(fig_status_canal, use_container_width=True)

with tab2:
    st.header("Analyse du Comportement des Leads et de l'Entonnoir")
    
    row1_c1 = st.columns(1)
    with row1_c1[0]:
        fig_device_canal = px.histogram(
            df_f_final, 
            x="channel", 
            color="device",
            barmode="group",
            title="Répartition des Terminaux (Appareils) par Canal",
            labels={'channel': 'Canal', 'device': 'Terminal'},
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_device_canal, use_container_width=True)

    row2_c1, row2_c2 = st.columns(2)
    with row2_c1:
        fig_imp = px.bar(df_f_camp.sort_values('impressions', ascending=False), 
                         x='channel', y='impressions', 
                         title="Volume d'Impressions par Canal",
                         color_discrete_sequence=['#636EFA'])
        st.plotly_chart(fig_imp, use_container_width=True)
        
    with row2_c2:
        secteur_data = df_f_final.groupby('sector').size().reset_index(name='leads')
        fig_sector = px.bar(
            secteur_data.sort_values('leads', ascending=True),
            y='sector', x='leads', orientation='h',
            title="Volume de Leads par Secteur d'Activité",
            labels={'sector': 'Secteur', 'leads': 'Nombre de Leads'}
        )
        st.plotly_chart(fig_sector, use_container_width=True)

with tab3:
    st.subheader("Registre détaillé des Leads (Septembre 2025)")
    st.dataframe(df_f_final, use_container_width=True)
    st.subheader("Synthèse des Performances Campagnes")
    st.dataframe(df_f_camp, use_container_width=True)