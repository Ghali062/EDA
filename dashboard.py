import streamlit as st
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

@st.cache_data

def load_data():
    df = pd.read_csv("creditcard.csv")
    df['hour'] = (df['Time'] // 3600) % 24
    return df

df = load_data()
filtered_df = df.copy()
st.title("Analyse de la fraude bancaire")

st.metric(label='Nombre totale de transactions',value=df.shape[0])
st.metric(label='Nombre totale de fraudes',value=df['Class'].sum())
st.metric(label="Taux de fraudes",value=df['Class'].sum()/df.shape[0])

#montant_max = st.sidebar.slider("Montant maximal", min_value, max_value, valeur_par_défaut)
montant = st.sidebar.slider(label="Montant maximal de transaction",min_value=df['Amount'].min(),max_value=df['Amount'].max(),value=float(df['Amount'].mean()))

fraudes_uniquement = st.sidebar.checkbox("Afficher uniquement les fraudes", value=False)
if fraudes_uniquement :
    filtered_df = df[df['Class']==1 ]

#Visualisations
filtered_df = filtered_df[filtered_df['Amount'] <= montant]

fig1, ax1 = plt.subplots()
sns.histplot(filtered_df['Amount'], bins=100, kde=True, ax=ax1)
st.pyplot(fig1)

fig2, ax2 = plt.subplots()
sns.countplot(data=filtered_df, x='hour', hue='Class', ax=ax2)
ax2.set_title("Transactions par heure")
ax2.set_xlabel("Heure de la journée")
ax2.set_ylabel("Nombre de transactions")
ax2.set_xticks(range(24))
ax2.set_xticklabels(range(24))
plt.xticks(rotation=0)
st.pyplot(fig2) 
