import streamlit as st
import datetime
import pandas as pd
import matplotlib.pyplot as plt


def trace_courbe(data, opt):
	_opt = opt

	p_min = round(data.Poids.min()*0.95,0)
	p_max = round(data.Poids.max()*1.05,0)
	fig, ax = plt.subplots(1,1)
	ax.set_ylim(p_min,p_max)

	plt.title("Enregistrements")
	if _opt == 'total':
		ax.scatter(data.Date, data.Poids)
		ax.plot([0,data.Date.max()],[data['Poids'].min(),data['Poids'].min()], '--g')
		ax.plot([0,data.Date.max()],[data['Poids'].max(),data['Poids'].max()], '--r')
	else:
		ax.bar(data.Date, data.Poids)
		ax.set_xlim(0,31)
		ax.plot([0,31],[data.Poids.mean(), data.Poids.mean()], '--r')

	return fig

def main():
	
	DATE = datetime.date.today()
	MOIS = DATE.month
	ANNEE = DATE.year


	st.sidebar.write('Gestion des données')

	sel=st.sidebar.radio("Sélection",('Enregistrement','Visualisation'),index=1)

	if sel == 'Enregistrement':
	
		st.header('Formulaire Google')
		st.markdown('<iframe src="https://docs.google.com/forms/d/e/1FAIpQLScf6dhJo8YaGJMIIYkL-YPOAUHSPJl4_V0tVgOUIo7vB2nByg/viewform?embedded=true" width="640" height="700" frameborder="0" marginheight="0" marginwidth="0">Chargement…</iframe>', unsafe_allow_html=True)

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
				st.pyplot(trace_courbe(donnees, opt))
			else:
				st.info('pas de donnée enregistrée')

		if opt == 'mois en cours':
			if len(mois) != 0:
				st.pyplot(trace_courbe(mois, opt))
			else:
				st.info('pas de donnée enregistrée')



		st.write("Poids moyen actuel : ",round(donnees[donnees.annee == ANNEE].Poids.tail(5).mean(),1))
		st.write("Mois : ", MOIS)
	

if __name__ == "__main__":
	main()

