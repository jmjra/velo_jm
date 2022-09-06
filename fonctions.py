import matplotlib.pyplot as plt
import pandas as pd
from numpy import polyfit


def trace(type_courbe, data_courbe, objectif=None, objectif_min=None):

	choix = type_courbe
	donnees = data_courbe

	fig, ax = plt.subplots(figsize=(8,4))

	if choix == 'mensuel':
		
		moyenne = donnees.mean()

		ax.set_xlabel('mois')
		ax.set_ylabel("km")
		ax.set_xlim([0,13])
		ax.set_ylim([0,donnees.max()*1.25])
		
		plt.title(f'Kilométrage mensuel - Moyenne : {round(moyenne,1)} km/mois')

		

		ax.bar(donnees.index, donnees, width = 0.5)

		ax.plot([1,12],[moyenne,moyenne], linestyle='--', color='orange')
	

		return fig
		

	if choix == 'cumul':
		
		# reg lin sur points
		_x = donnees.index.tolist()
		_y = donnees.tolist()


		# ajout du point (0,0)
		_x.insert(0,0)
		_y.insert(0,0)
		

		(coeff, ordo_or) = polyfit(_x,_y, deg=1)
		reg_lin = [coeff*it+ordo_or for it in range(1,13)]

		prev = reg_lin[-1]


		ax.set_xlabel('mois')
		ax.set_ylabel("km")

		ax.set_xlim(0,12)
		# ax.set_ylim(0,donnees.max()+100)
		ax.set_ylim(0, 5000)
		ax.xaxis.set_ticks(range(0,13))

		plt.title('Kilométrage cumulé')

		# ax.plot(donnees.index,donnees,'go-', linewidth=2, markersize=8)
		ax.plot(_x,_y,'bo-', linewidth=2, markersize=8)
		ax.plot([0,12],[0,int(objectif)], linestyle = '--', color='red')
		# ax.plot([0,12],[0,int(objectif_min)], linestyle = '--', color='orange')
		# trace de reg lin
		ax.plot(list(range(1,13)),reg_lin, linestyle = '--', color='gray')

		return fig, prev
		
		

	if choix == 'semaine':
		
		moyenne = donnees.mean()

		ax.set_xlabel('semaine')
		ax.set_ylabel("km")
		ax.set_ylim([0,donnees.max()+50])
		plt.title(f'Kilométrage hebdomadaire - Moyenne : {round(moyenne,1)} km/semaine')

		ax.bar(donnees.index, donnees)
		ax.plot([0,52],[moyenne,moyenne], linestyle = '--', color = 'orange')

		return fig
		


