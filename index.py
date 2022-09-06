import streamlit as st
import datetime
from urllib.request import urlopen
import base64 as b6
import io

######## données #######

dico_jour = {1:'Lundi',
			2:'Mardi',
			3:'Mercredi',
			4:'Jeudi',
			5:'Vendredi',
			6:'Samedi',
			7:'Dimanche'}

dico_mois = {1:'janvier',
			2:'février',
			3:'mars',
			4:'avril',
			5:'mai',
			6:'juin',
			7:'juillet',
			8:'août',
			9:'septembre',
			10:'octobre',
			11:'novembre',
			12:'décembre' }

## appel de le fonction image.php ##

site = 'http://jmadnet.free.fr/image'


######### récup image aléatoire ########

res = urlopen(site)
data = res.read().decode('utf-8')
image = b6.b64decode(data)
img_alea = io.BytesIO(image)
# img_alea = imread(img_alea)


#######################################

visu=True

dd = datetime.date.today()

date_jour = f"{dico_jour.get(dd.isoweekday())} {dd.day} \
	{dico_mois.get(dd.month)} {dd.year}"



if visu:
	st.sidebar.subheader('Choix de la fonctionnalité...')

	liste_choix=['Sorties vélo','Suivi poids','Accueil']

	choix = st.sidebar.selectbox('Option',liste_choix, index=len(liste_choix)-1)

	

if choix==liste_choix[0]:
	from mod_jma import velo
	
	velo.main() #lancement de la page vélo

if choix==liste_choix[1]:
	from mod_jma import poids

	

	#st.sidebar.markdown("[Téléchargement des données]('http://127.0.0.1:8501/images/output.gif')", unsafe_allow_html=True)

	poids.main() #lancement de la page poids \
								#+ transfert info enregistrement

		

if choix==liste_choix[-1]: # Page d'accueil
	
	st.sidebar.image('images/output.gif',use_column_width='auto')
	# st.sidebar.info(datetime.date.today().strftime("%d - %m - %Y"))
	st.sidebar.info(date_jour)

	st.info('Site perso de JMA fonctionnant sous python + streamlit')

	st.markdown("""

	Fonctionnalités actuelles :

		1) Suivi des sorties vélo
		2) Enregistrement du poids

	Les données sont stockées sur Google Sheets !


	 """)
	st.markdown(""" **Sélection du jour**""")

	st.image(img_alea, use_column_width='auto')














