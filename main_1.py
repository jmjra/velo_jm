import streamlit as st
import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt


####### importation des données / lecture fichier googlsheets
FICH = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ5fH6oWENyBy1Am4aT7Uw02JWrcZvhX1gmbJCQg-J3xiw9-Yj3yZLGjbUT72mult4D2T3pHld3508W/pub?output=csv"

data=pd.read_csv(FICH, header=None)

ANNEE=datetime.date.today().year

######## Traitement des données / préparation

data["date"]=pd.to_datetime(data[0])
data=data.drop(columns=[5,6])

#data["annee"]=data.apply(lambda x: x['date'].strftime('%Y'), axis=1)
data['annee']=data['date'].dt.year # modif 7/3/2021

#data["mois"]=data.apply(lambda x: x['date'].strftime('%m'), axis=1)
data['mois']=data['date'].dt.month # modif 7/3/2021

data=data.rename(columns={2:'km'})
data['sem']=data["date"].dt.dayofyear//7 # modif 7/3/2021


##### sidebar ##### à positionner ici car définition des variables
st.sidebar.write("# Paramétrage #")
#liste_choix=[an for an in range(2017,2022)]
liste_choix = data.annee.unique()
annee = st.sidebar.selectbox("Année", liste_choix, index=len(liste_choix)-1)
choix = st.sidebar.radio("Mode de présentation",["cumul","mensuel", "semaine"], index=1)

st.sidebar.info(f"Année : {annee} - Choix : {choix}")

######## Traitement des données / extraction

total = data.groupby(['annee'])['km'].agg(['sum','mean'])/1000

detail_annee = data.groupby(['annee','mois'])['km'].agg(['sum'])/1000

detail_annee = detail_annee['sum'][annee] # modif anciennement str(annee)


cumul_annee = data[data.annee == annee].groupby('mois')['km'].sum()/1000# idem modif
cumul_annee['cum'] = cumul_annee.cumsum()
cumul_annee = cumul_annee.cum

cumul_semaine = data[data.annee == annee].groupby('sem')['km'].sum()/1000# idem modif

#### page principale ####

st.title("Sorties vélo "+str(ANNEE))

col1,col2 = st.beta_columns(2)

with col1:
    st.write("Récapitulatif")
    st.dataframe(total)

with col2:
    st.write('Bilan précédent : < 2020')
    st.image('images/cumul_velo.png', use_column_width='auto')


message=f"Détail pour {annee}"
st.subheader(message)

if (annee == str(ANNEE)): 
	st.info('Par défaut l\'année en cours est affichée')

if choix == 'mensuel':
	st.bar_chart(detail_annee)

if choix == 'cumul':
	st.line_chart(cumul_annee)

if choix == 'semaine':
	st.bar_chart(cumul_semaine)



title = st.text_area('Exprimez vous !')

if title:
	#st.write('Commentaire :', datetime.date.today().strftime("%d/%m/%Y : ") + title)
	st.warning(datetime.date.today().strftime("%d/%m/%Y : ") + title)
else:
	st.write('Rien à signaler aujourd\'hui')







