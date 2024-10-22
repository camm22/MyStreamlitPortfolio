import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Master's Graduate Analysis", layout="wide", page_icon='📊')
st.sidebar.markdown("# 📊 Master's Graduate Analysis")

@st.cache_data
def load_data():
    df = pd.read_csv('fr-esr-insertion_professionnelle-master.csv', delimiter=';')
    df.drop(columns=['numero_de_l_etablissement', 'etablissementactuel', 'code_de_l_academie', 'code_du_domaine', 'code_de_la_discipline', 'remarque', 'nombre_de_reponses', 'taux_de_reponse', 'poids_de_la_discipline', 'taux_dinsertion', 'taux_d_emploi', 'taux_d_emploi_salarie_en_france', 'emplois_cadre_ou_professions_intermediaires', 'cle_disc', 'id_paysage', 'emplois_cadre', 'emplois_exterieurs_a_la_region_de_luniversite', 'de_diplomes_boursiers', 'cle_etab', 'salaire_brut_annuel_estime', 'femmes'], inplace=True)
    
    numerical_columns = [
        'emplois_stables', 
        'emplois_a_temps_plein', 
        'salaire_net_median_des_emplois_a_temps_plein',
        'taux_de_chomage_regional', 
        'salaire_net_mensuel_median_regional',
        'salaire_net_mensuel_regional_1er_quartile', 
        'salaire_net_mensuel_regional_3eme_quartile'
    ]
    
    for col in numerical_columns:
        df[col] = df[col].replace(['ns', 'nd', '.', ''], np.nan)
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.'), errors='coerce')
    
    return df

df = load_data()

st.title("Professional Integration of Master's Graduates in France 📈")
st.write("""
**This analysis explores the career outcomes of Master's graduates from French universities. 
We'll examine employment rates, salaries, and various factors affecting professional success.**
""")

st.sidebar.header("Filters")
selected_year = st.sidebar.selectbox("Select Year", sorted(df['annee'].unique()))
selected_situation = st.sidebar.selectbox("Time After Graduation", df['situation'].unique())

filtered_df = df[
    (df['annee'] == selected_year) &
    (df['situation'] == selected_situation)
]

st.header('1. Data set')
st.dataframe(df)
rows, columns = df.shape
st.write(f"- **{rows} rows** and **{columns} columns**")

st.header("2. Employment Stability and Full-time Employment")
col1, col2 = st.columns(2)

with col1:
    domain_stability = filtered_df.groupby('domaine')['emplois_stables'].mean().reset_index()
    domain_stability = domain_stability.dropna()
    domain_stability = domain_stability.sort_values('emplois_stables', ascending=True)
    
    if not domain_stability.empty:
        fig_stability = px.bar(
            domain_stability,
            x='emplois_stables',
            y='domaine',
            orientation='h',
            title=f'Stable Employment Rate by Domain ({selected_year})',
            labels={'emplois_stables': 'Stable Employment Rate (%)', 'domaine': 'Domain'}
        )
        st.plotly_chart(fig_stability)
    else:
        st.write("No data available for stable employment in this selection.")

with col2:
    domain_fulltime = filtered_df.groupby('domaine')['emplois_a_temps_plein'].mean().reset_index()
    domain_fulltime = domain_fulltime.dropna()
    domain_fulltime = domain_fulltime.sort_values('emplois_a_temps_plein', ascending=True)
    
    if not domain_fulltime.empty:
        fig_fulltime = px.bar(
            domain_fulltime,
            x='emplois_a_temps_plein',
            y='domaine',
            orientation='h',
            title=f'Full-time Employment Rate by Domain ({selected_year})',
            labels={'emplois_a_temps_plein': 'Full-time Employment Rate (%)', 'domaine': 'Domain'}
        )
        st.plotly_chart(fig_fulltime)
    else:
        st.write("No data available for full-time employment in this selection.")

st.header("3. Salary Analysis")
col3, col4 = st.columns(2)

with col3:
    salary_df = filtered_df.dropna(subset=['salaire_net_median_des_emplois_a_temps_plein'])
    
    if not salary_df.empty:
        fig_salary = px.box(
            salary_df,
            x='domaine',
            y='salaire_net_median_des_emplois_a_temps_plein',
            title=f'Salary Distribution by Domain ({selected_year})',
            labels={'salaire_net_median_des_emplois_a_temps_plein': 'Median Net Salary (€)',
                    'domaine': 'Domain'}
        )
        st.plotly_chart(fig_salary)
    else:
        st.write("No salary data available for this selection.")

with col4:
    # Compare MASTER LMD vs MASTER ENS
    masters_comparison = filtered_df.groupby(['diplome', 'domaine']).agg({
        'salaire_net_median_des_emplois_a_temps_plein': 'mean',
        'emplois_stables': 'mean',
        'emplois_a_temps_plein': 'mean'
    }).reset_index()
    
    metric_tabs = st.tabs(["Salary", "Stable Employment", "Full-time Employment"])
    
    with metric_tabs[0]:  # Salary comparison
        if not masters_comparison.empty:
            fig_masters_salary = px.bar(
                masters_comparison,
                x='domaine',
                y='salaire_net_median_des_emplois_a_temps_plein',
                color='diplome',
                barmode='group',
                title=f'Average Salary by Master Type ({selected_year})',
                labels={
                    'salaire_net_median_des_emplois_a_temps_plein': 'Average Salary (€)',
                    'domaine': 'Domain',
                    'diplome': 'Diploma Type'
                }
            )
            fig_masters_salary.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_masters_salary)
            
    with metric_tabs[1]:  # Stable employment comparison
        if not masters_comparison.empty:
            fig_masters_stable = px.bar(
                masters_comparison,
                x='domaine',
                y='emplois_stables',
                color='diplome',
                barmode='group',
                title=f'Stable Employment Rate by Master Type ({selected_year})',
                labels={
                    'emplois_stables': 'Stable Employment Rate (%)',
                    'domaine': 'Domain',
                    'diplome': 'Diploma Type'
                }
            )
            fig_masters_stable.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_masters_stable)
            
    with metric_tabs[2]:  # Full-time employment comparison
        if not masters_comparison.empty:
            fig_masters_fulltime = px.bar(
                masters_comparison,
                x='domaine',
                y='emplois_a_temps_plein',
                color='diplome',
                barmode='group',
                title=f'Full-time Employment Rate by Master Type ({selected_year})',
                labels={
                    'emplois_a_temps_plein': 'Full-time Employment Rate (%)',
                    'domaine': 'Domain',
                    'diplome': 'Diploma Type'
                }
            )
            fig_masters_fulltime.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_masters_fulltime)

st.header("4. Regional Analysis")

regional_df = filtered_df.dropna(subset=['taux_de_chomage_regional', 'salaire_net_mensuel_median_regional'])

if not regional_df.empty:
    fig_regional = px.scatter(
        regional_df,
        x='taux_de_chomage_regional',
        y='salaire_net_mensuel_median_regional',
        color='academie',
        hover_data=['etablissement'],
        title=f'Regional Unemployment Rate vs Median Salary ({selected_year})',
        labels={'taux_de_chomage_regional': 'Regional Unemployment Rate (%)',
                'salaire_net_mensuel_median_regional': 'Regional Median Monthly Salary (€)',
                'academie': 'Academy'}
    )
    st.plotly_chart(fig_regional, use_container_width=True)
else:
    st.write("No regional data available for this selection.")

st.header("5. Key Insights")
col5, col6 = st.columns(2)

with col5:
    avg_stable = filtered_df['emplois_stables'].mean()
    avg_fulltime = filtered_df['emplois_a_temps_plein'].mean()
    
    if not pd.isna(avg_stable):
        st.metric("Average Stable Employment Rate", f"{avg_stable:.1f}%")
    if not pd.isna(avg_fulltime):
        st.metric("Average Full-time Employment Rate", f"{avg_fulltime:.1f}%")

with col6:
    avg_salary = filtered_df['salaire_net_median_des_emplois_a_temps_plein'].mean()
    avg_unemployment = filtered_df['taux_de_chomage_regional'].mean()
    
    if not pd.isna(avg_salary):
        st.metric("Average Median Salary", f"€{avg_salary:.0f}")
    if not pd.isna(avg_unemployment):
        st.metric("Average Regional Unemployment Rate", f"{avg_unemployment:.1f}%")


st.header("Analysis Summary")
st.markdown("""
This dashboard provides insights into the professional integration of Master's graduates in France. Key observations:

1. **Employment Stability**: The dashboard shows variations in stable employment rates across different domains.
2. **Master's Type Comparison**: We can observe differences in outcomes between MASTER LMD and MASTER ENS programs across various metrics:
   - Salary levels
   - Stable employment rates
   - Full-time employment rates
3. **Regional Variations**: The visualization of regional unemployment rates versus salaries reveals geographical disparities in job markets.
4. **Full-time Employment**: The analysis shows the proportion of graduates who secure full-time positions across different fields.

Use the filters in the sidebar to explore different years and time periods after graduation.
""")
