import streamlit as st
import numpy as np
import pandas as pd
import datetime
#import matplotlib.pyplot as plt
from mod_jma.fonctions import trace

# lien vers données Google Sheets
FICH = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ5fH6oWENyBy1Am4aT7Uw02JWrcZvhX1gmbJCQg-J3xiw9-Yj3yZLGjbUT72mult4D2T3pHld3508W/pub?output=csv"



def lecture(fich):

	return pd.read_csv(fich, header=None)


####### importation des données / lecture fichier google sheets

def main():

	data=lecture(FICH)

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

	objectif = st.sidebar.text_input('Objectif de l\'année', 4500)
	objectif_min = st.sidebar.text_input('Objectif minimal', round(4500/2,0))
	objectif_min = float(objectif_min)
	
	liste_choix = data.annee.unique()
	annee = st.sidebar.selectbox("Année", liste_choix, index=len(liste_choix)-1)
	choix = st.sidebar.radio("Mode de présentation",["cumul","mensuel", "semaine"], index=1)

	st.sidebar.info(f"Année : {annee} - Objectif : {objectif}")

	######## Traitement des données / extraction

	total = data.groupby(['annee'])['km'].agg(['sum','mean'])/1000

	detail_annee = data.groupby(['annee','mois'])['km'].agg(['sum'])/1000

	detail_annee = detail_annee['sum'][annee] # modif anciennement str(annee)


	cumul_annee = data[data.annee == annee].groupby('mois')['km'].sum()/1000# idem modif
	cumul_annee['cum'] = cumul_annee.cumsum()
	cumul_annee = cumul_annee.cum

	cumul_semaine = data[data.annee == annee].groupby('sem')['km'].sum()/1000# idem modif

	#### page principale ####

	st.info("Sorties vélo "+str(annee)+" : objectif = "+str(objectif)+" km")

	with st.expander("+ d'info"):


		#col1,col2 = st.columns(2)

		#with col1:
		st.write("Récapitulatif")
		st.dataframe(total)

		#with col2:
		st.write(f"Bilan précédent : < {ANNEE}")
		    #st.image('images/cumul_velo.png', use_column_width='auto')
		st.markdown("""<iframe width="600" height="400" src="https://docs.google.com/spreadsheets/d/e/2PACX-1vTparJCYwmqxiXxwZnaSx-F_7cHaZm9Nr-QGnkIM6H4jyZYg5CHGsUXy4MsynG5zfbTfepuzH5CeI7d/pubchart?oid=174466294&format=image"></iframe>""", unsafe_allow_html=True)											
													


	message=f"Détail pour {annee} - Total actuel : {round(total['sum'][annee],1)} km"
	st.subheader(message)

	## affichage courbe gsheet

	# st.markdown("""<iframe width ="600" height="400" src="https://docs.google.com/spreadsheets/d/e/2PACX-1vTBafAKsaj5mQxngpJQmmsdcHtFaU0DQbVpP2gPZe-f0q7VzTgYxZjoHFU97w4AC-SxbaqzsYIggdxb/pubchart?oid=174466294&amp;format=image"></iframe>""",unsafe_allow_html=True) 
	# st.markdown("""<iframe width ="600" height="400" src="https://docs.google.com/spreadsheets/d/e/2PACX-1vQBmY_1b2XT94E60Ma_PcEVQcuonGk6r9DR-oXNB2KhrmoQtoJRfkjuqzN-w1XR8HXN0j3h_JLYyqUm/pubchart?oid=174466294&amp;format=interactive"></iframe>""",unsafe_allow_html=True)
	
	#st.markdown("""<iframe width ="600" height="400" src="https://docs.google.com/spreadsheets/d/e/2PACX-1vQsZuVNcQd-bEICzpQsE0GOGPXN8sUHwoq920DVFpheNqDgIsMA9kkPPf1-tLh6YK64Amn_65GaljoH/pubhtml?gid=1308477466&single=true">""", unsafe_allow_html=True)
	
	#st.markdown("""<iframe width ="600" height="400" src="https://docs.google.com/spreadsheets/d/e/2PACX-1vQsZuVNcQd-bEICzpQsE0GOGPXN8sUHwoq920DVFpheNqDgIsMA9kkPPf1-tLh6YK64Amn_65GaljoH/pubchart?oid=174466294&amp;format=image"></iframe>""", unsafe_allow_html=True)
	st.markdown("""<iframe width ="600" height="400" src="https://docs.google.com/spreadsheets/d/e/2PACX-1vTparJCYwmqxiXxwZnaSx-F_7cHaZm9Nr-QGnkIM6H4jyZYg5CHGsUXy4MsynG5zfbTfepuzH5CeI7d/pubchart?oid=174466294&format=image"></iframe>""", unsafe_allow_html=True)

	
	if (annee == str(ANNEE)): 
		st.info('Par défaut l\'année en cours est affichée')

	if choix == 'mensuel':
		#st.bar_chart(detail_annee)
		st.pyplot(trace(choix, detail_annee))

	if choix == 'cumul':
		#st.line_chart(cumul_annee)
		_trace = trace(choix, cumul_annee, objectif, objectif_min)
		st.pyplot(_trace[0])
		st.warning(f"Estimation en fin d'année : {round(_trace[1],1)} km")
		

	if choix == 'semaine':
		#st.bar_chart(cumul_semaine)
		st.pyplot(trace(choix, cumul_semaine))	


if __name__ == '__main__':

	main()




