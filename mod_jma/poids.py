import streamlit as st
import datetime
import re
import json
import pandas as pd
import matplotlib.pyplot as plt

DATE = datetime.date.today()
MOIS = DATE.month
ANNEE = DATE.year

def trace_courbe(data):

		fig, ax = plt.subplots(1,1)
		ax.set_ylim(50,100)

		plt.title("Enregistrements")
		ax.scatter(data.Date, data.Poids)

		return fig

def main():

	st.sidebar.write('Gestion des données')

	sel=st.sidebar.radio("Sélection",('Enregistrement','Visualisation'),index=1)

	if sel == 'Enregistrement':
	        
	        st.header('Formulaire Google')
	        st.markdown('<iframe src="https://docs.google.com/forms/d/e/1FAIpQLScf6dhJo8YaGJMIIYkL-YPOAUHSPJl4_V0tVgOUIo7vB2nByg/viewform?embedded=true" width="640" height="700" frameborder="0" marginheight="0" marginwidth="0">Chargement…</iframe>',unsafe_allow_html=True)

	if sel == 'Visualisation':
	        
	        RESULTATS = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQq0cqyMFLx3YQlWJxgmxYdynKIsOPKODEd_4KJXjMY5iLJ3WSGY14LkkQspXUD7M--4cRF-CbCtqSl/pub?gid=1289613281&single=true&output=csv'

	        st.sidebar.write(f"Année : {ANNEE}")
	        opt=st.sidebar.radio("Options",('total','mois en cours'))

	        donnees=pd.read_csv(RESULTATS)
	        donnees=donnees.loc[:, ['Date','Poids']]

	        donnees['Date']=pd.to_datetime(donnees.Date, format='%d/%m/%Y')
	        
	        donnees['mois']=donnees['Date'].dt.month
	        donnees['jour']=donnees['Date'].dt.day
	        donnees['annee']=donnees['Date'].dt.year

	        cond = (donnees.mois == MOIS) & (donnees.annee == ANNEE)

	        mois = donnees[cond][['Date','Poids']]
	        mois['Date']=mois.Date.dt.day


	        with st.expander('voir les données'):

	        	if opt == 'total':
	        		st.write(donnees.tail(5))
	        	else:
	        		st.write(mois)

	        

	        if opt == 'total':	
	        	if len(donnees) != 0:

	        		donnees['Date']=donnees[donnees.annee == ANNEE].Date.dt.dayofyear
	        		st.pyplot(trace_courbe(donnees))
	        	else:
	        		st.info('pas de donnée enregistrée')

	        if opt == 'mois en cours':
	        	if len(mois) != 0:
	        		st.pyplot(trace_courbe(mois))
	        	else:
	        		st.info('pas de donnée enregistrée')



	        st.write("Poids moyen actuel : ",round(donnees[donnees.annee == ANNEE].Poids.mean(),1))
	        st.write("Mois : ", MOIS)
		

if __name__ == "__main__":
	main()

