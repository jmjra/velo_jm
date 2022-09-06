import matplotlib.pyplot as plt
import pandas as pd


def trace(type_courbe, data_courbe):

	choix = type_courbe
	donnees = pd.DataFrame()
	donnees = data_courbe

	fig, ax = plt.subplots()

	if choix == 'mensuel':
		ax.set_xlabel('mois')
		ax.set_ylabel("km")
		plt.title('Kilométrage mensuel')

		ax.bar(donnees.index, donnees, tick_label=donnees.index)

		return fig
		

	if choix == 'cumul':
		#st.line_chart(cumul_annee)
		pass
		

	if choix == 'semaine':
		#st.bar_chart(cumul_semaine)
		pass
		


