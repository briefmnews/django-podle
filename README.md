# django-podle
[![Python 3.9](https://img.shields.io/badge/python-3.7|3.8|3.9-blue.svg)](https://www.python.org/downloads/release/python-390/) 
[![Django 2.2](https://img.shields.io/badge/django-2.2-blue.svg)](https://docs.djangoproject.com/en/2.2/)
[![Python CI](https://github.com/briefmnews/django-podle/actions/workflows/workflow.yaml/badge.svg)](https://github.com/briefmnews/django-podle/actions/workflows/workflow.yaml)
[![codecov](https://codecov.io/gh/briefmnews/django-podle/branch/main/graph/badge.svg?token=w8N0eR6uLr)](https://codecov.io/gh/briefmnews/django-podle)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)  
Integration with [Podle.io](https://podle.io/) podcast app.  
See Podle documentation [here](https://api.podle.io/documentation).

## Installation
Install with pip from PyPI:
```shell
pip install django-podle
```

Or install with pip from the main branch:
```shell
pip install -e git://github.com/briefmnews/django-podle.git@main#egg=django-podle
```

## Setup
In order to make `django-podle` works, you'll need to follow the steps below.


### Settings
First you need to add the following configuration to your settings:
```python
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',

    'podle',
    ...
)
```

### Migrations
Next, you need to run the migrations in order to update your database schema.
```shell
python manage.py migrate
```

### Mandatory settings
Here is the list of all the mandatory settings:
```python
PODLE_AUTH_TOKEN: api key to consume the api
PODLE_NEWSLETTER_NAME: name of the newsletter. Useful for RSS feed only
```

### Optional settings
Here is the list of all the optional settings:
```python
PODLE_RSS_FEED_GROUP_NAME: group name for creating / deleting private RSS feed. The native django signal is caught when the user enters or leaves the group to create or delete the RSS feed.
```

## Webhook
You can give an url to Podle to get a webhook when the newsletter audio file is created.
The webhook will be post to `{YOUR_DOMAIN}/podle/webhook`.
A signal called `audio_file` is sent when receiving the webhook.

In case of success, if the audio file is created with an existing `newsletter` object:
```python
audio_file.send(sender=Newsletter, success=True, audio_url=serializer.validated_data["newsletter_url"], newsletter=newsletter)
```

In case of an error:
```python
audio_file.send(sender=Newsletter, success=False, errors=serializer.errors)
```

## How to use?
### Create or update a newsletter
Here is a quick example of how to create an audio file with podle.
```python
from podle.models import Newsletter

json_content = {
  "correspondent": "John Doe or johndoe.mp3",
  "title": "Gestion de l???eau | Talibans | Correspondance amoureuse",
  "description": "Dans Brief.me ce week-end, la gestion de l???eau en France, les talibans, la rumba congolaise et la correspondance amoureuse d???un d??tenu.\nTest Thomas",
  "voiceGender": "female",
  "intro": "Brief.me : ??dition du 10 mai 2021",
  "sections": [
    {
      "title": "",
      "articles": [
        {
          "title": "",
          "body": "Dans Brief.me ce week-end, la gestion de l???eau en France, les talibans, la rumba congolaise et la correspondance amoureuse d???un d??tenu.\nTest Thomas",
          "voiceGender": "female",
          "source": ""
        }
      ]
    },
    {
      "title": "La gestion de l???eau en France",
      "articles": [
        {
          "title": "",
          "body": "Les entreprises fran??aises de gestion de l???eau et des d??chets Suez et Veolia ont annonc?? lundi ??tre parvenues ?? un accord de principe pour leur rapprochement. Suez s???opposait depuis l???an dernier aux offres de rachat de Veolia. Cette op??ration intervient alors que la gestion de l???eau en France, fortement d??l??gu??e par les communes ?? des op??rateurs priv??s dans les ann??es 1990, conna??t une ?? remunicipalisation ?? depuis quelques ann??es.?? l???origine. Au XIXe si??cle, l???industrialisation et la persistance d?????pid??mies dans les grandes villes font de la gestion de l???eau un sujet de pr??occupation majeur. Les communes, qui en sont charg??es depuis la R??volution fran??aise, se dotent progressivement de r??seaux de distribution d???eau salubre ?? partir de la moiti?? du XIXe si??cle. Se d??veloppent un service public, qui dessert gratuitement les fontaines publiques, et un service priv?? et payant d???eau ?? domicile. B??n??ficier de l???eau ?? domicile est toutefois le privil??ge d???une minorit?? ais??e. Les communes ont recours ?? des compagnies priv??es de distribution d???eau, auxquelles elles confient le service ?? domicile, en ??change de quoi ces entreprises participent au financement des fontaines publiques. Les premi??res soci??t??s cr????es sont la Compagnie g??n??rale des eaux en 1853 et la Lyonnaise des eaux en 1880. Les communes rurales commencent ?? s?????quiper dans les ann??es 1930. Le raccordement sera lent : il faut attendre la fin des ann??es 1980 pour que la quasi-totalit?? des Fran??ais b??n??ficient de l???eau potable ?? domicile.Les dates cl??s. 1964. La loi de 1964 sur l???eau est le premier texte qui organise la gestion de l???eau ?? l?????chelle nationale, alors que sa consommation progresse et que le niveau de pollution s???accro??t avec l???urbanisation et le d??veloppement de l???industrie et de l???agriculture intensive. La loi organise la gestion de l???eau autour de six grands bassins fluviaux en m??tropole (voir la carte). Elle cr??e une agence de l???eau pour chaque bassin, charg??e de percevoir des redevances aupr??s des personnes publiques ou priv??es, d??s lors qu???elles pr??l??vent de l???eau ou la polluent, et de financer ainsi la pr??servation de la ressource et la lutte contre la pollution. Les redevances permettent par exemple aux collectivit??s de financer les stations d?????puration des eaux us??es. Alors que la France ne comptait que 300 stations d?????puration avant l???adoption de la loi de 1964, plus de 2 100 stations ??taient recens??es en 1970 et 11 500 en 1990, selon deux rapports parlementaires de 2003.1997. En 1997, la Lyonnaise des eaux et la Compagnie financi??re de Suez, une soci??t?? fran??aise qui a exploit?? la concession du canal ??gyptien de Suez, fusionnent et deviennent le groupe Suez-Lyonnaise des eaux (rebaptis?? Suez en 2001). Le groupe recentre ses activit??s sur les services aux collectivit??s, dont la gestion de l???eau. Il concurrence ainsi sur le march?? la Compagnie g??n??rale des eaux (dont la filiale consacr??e ?? l???environnement deviendra Veolia) et Saur. En 1995, 75 % de la population, soit plus de 46 millions d???habitants, sont approvisionn??s en eau par un op??rateur priv??, la Compagnie g??n??rale des eaux alimentant ?? elle seule 25 millions de personnes, rapporte Christelle Pezon, chercheuse dans le domaine de l???eau potable, dans sa th??se en 2000. Les communes (ou les intercommunalit??s), auxquelles incombent la distribution de l???eau potable et l???assainissement et qui sont propri??taires des infrastructures, peuvent choisir d???exploiter le service selon plusieurs modes, dont la r??gie ??? en le g??rant directement ??? et la d??l??gation de service public ??? en le confiant ?? un op??rateur priv??.2000. La ville de Grenoble vote en 2000 le retour en r??gie du service de l???eau et de l???assainissement, qui ??tait g??r?? depuis 1989 par une filiale de la Lyonnaise des eaux. Cette d??cision fait suite ?? une affaire de corruption impliquant l???op??rateur et le maire de l?????poque, Alain Carignon, pour laquelle il a ??t?? condamn?? par la justice. Plusieurs villes ont fait le choix d???un retour ?? la r??gie, comme Paris, Brest et Nice, dans les ann??es 2010. Cette ?? remunicipalisation ?? de la gestion de l???eau intervient apr??s des constatations de mauvais entretien des r??seaux ou d?????carts de prix entre les deux modes de gestion. En 2018, seuls 31 % des services publics d???eau potable ??taient g??r??s par d??l??gation, mais ils approvisionnaient une majorit?? (57 %) de la population, selon un rapport publi?? ce mois-ci par l???Office fran??ais de la biodiversit??, un ??tablissement public.2015. Le Conseil constitutionnel, l???instance charg??e de contr??ler la conformit?? des lois ?? la Constitution, rend une d??cision en mai 2015 affirmant que l???eau ?? r??pond ?? un besoin essentiel de la personne ?? et ?? qu???aucune personne en situation de pr??carit?? ?? ne peut en ??tre priv??e. Il avait ??t?? saisi apr??s une demande du distributeur Saur, assign?? en justice pour avoir coup?? l???eau ?? un client entre avril 2013 et septembre 2014 pour un impay?? de pr??s de 280 euros. Saur contestait l???interdiction, introduite par une loi de 2013, pour les distributeurs d???eau de proc??der ?? des coupures dans une r??sidence principale en cas de d??faut de paiement des factures, et ce tout au long de l???ann??e. Le Conseil constitutionnel ayant valid?? la constitutionnalit?? de la loi, Saur est condamn?? dans cette affaire en octobre 2015. Plusieurs d??cisions de justice rendues par la suite ont statu?? ??galement sur l???interdiction de toute r??duction du d??bit d???eau par les distributeurs.Le concept. En France, l???eau qui alimente les robinets est capt??e majoritairement dans les nappes souterraines ou dans des plans et cours d???eau. Cette eau est rendue potable au sein d???une usine de potabilisation ?? travers diff??rents proc??d??s, dont la filtration et la d??sinfection. L???eau est test??e pour v??rifier que les teneurs de diverses substances (plomb, arsenic, pesticides, etc.) sont inf??rieures aux normes sanitaires ??tablies par l???UE. L???eau potable est ensuite stock??e, souvent dans des ch??teaux d???eau, afin de disposer de r??serves en cas de variations de la demande. L???eau potable est achemin??e jusqu???aux usagers gr??ce ?? un r??seau de canalisations. Environ 20 % de l???eau potable est perdue lors de sa distribution ?? cause de fuites, selon Eau de France, le service public de l???information sur l???eau. Les eaux us??es, vers??es au ?? tout-??-l?????gout ??, sont assainies dans une station d?????puration, avant d?????tre rejet??es, le plus souvent dans des rivi??res. En 2018, la consommation moyenne d???eau potable ??tait de 148 litres par jour et par habitant, selon l???Office fran??ais de la biodiversit??.",
          "voiceGender": "female",
          "source": ""
        }
      ]
    },
    {
      "title": "On rembobine la semaine",
      "articles": [
        {
          "title": "",
          "body": "Iran. La France, l???Allemagne et le Royaume-Uni ont exprim?? mercredi leur ?? grande pr??occupation ?? concernant l???annonce faite la veille par l???Iran du lancement d???un processus pour produire de l???uranium enrichi ?? 60 %, contre 20 % actuellement. Depuis le retrait en 2018 des ??tats-Unis de l???accord de 2015 sur le nucl??aire iranien, qui pr??voyait que l???Iran n???enrichisse pas l???uranium ?? plus de 3,67 % pendant 15 ans, l???Iran s???est affranchi progressivement des limites fix??es ?? ses capacit??s nucl??aires.Viticulture. La FNSEA, le principal syndicat agricole, a annonc?? mercredi qu???au moins un tiers de la production viticole fran??aise allait ??tre perdue cette ann??e ?? cause du gel, repr??sentant une perte de 2 milliards d???euros de chiffre d???affaires. 10 des 13 r??gions m??tropolitaines ont connu la semaine derni??re un ??pisode de gel exceptionnel, provoquant d???importants d??g??ts dans les cultures viticoles. Le Premier ministre, Jean Castex, avait annonc?? samedi dernier que ?? tous les m??canismes de soutien ?? seraient activ??s.S??curit??. Le Parlement a d??finitivement adopt?? jeudi la proposition de loi sur la ?? s??curit?? globale ??, soutenue par le gouvernement. L???Assembl??e nationale s???est prononc??e en seconde lecture par 75 voix contre 33 en faveur de ce texte tr??s critiqu?? par les syndicats de journalistes et plusieurs ONG comme Amnesty International, qui estime qu????? entre les mains d???un gouvernement autoritaire, une telle loi deviendrait une dangereuse arme de surveillance et de r??pression de la population ??. Le groupe des d??put??s socialistes a annonc?? hier son intention de saisir le Conseil constitutionnel, l???instance charg??e de contr??ler la conformit?? des lois ?? la Constitution.Russie. La Maison-Blanche a annonc?? jeudi l???adoption d???une s??rie de sanctions financi??res contre la Russie, ainsi que l???expulsion de 10 diplomates russes en poste aux ??tats-Unis. Cette d??cision vise ?? r??pondre aux ing??rences russes dans les ??lections am??ricaines de 2020 et ?? une cyberattaque massive ayant touch?? des agences f??d??rales et entreprises am??ricaines, attribu??e ?? la Russie. Le pr??sident am??ricain, Joe Biden, qui s???est entretenu avec son homologue russe Vladimir Poutine cette semaine, l???a ??galement appel?? ?? la ?? d??sescalade ?? en Ukraine, o?? un conflit oppose depuis 2014 s??paratistes pro-russes et arm??e ukrainienne dans l???est du pays.Violences sexuelles. Le Parlement a adopt?? jeudi soir, par un ultime vote ?? l???unanimit?? ?? l???Assembl??e nationale, une proposition de loi visant ?? mieux prot??ger les mineurs contre les crimes et d??lits sexuels. Le texte fixe un seuil de non-consentement ?? 15 ans, en de???? duquel tout acte de p??n??tration sexuelle commis par un adulte sera automatiquement consid??r?? comme un viol. Ce seuil est de 18 ans en cas d???inceste. ?? Avant 15 ans, plus aucun adulte agresseur ne pourra se pr??valoir du consentement d???un mineur ??, s???est f??licit?? jeudi le ministre de la Justice, ??ric Dupond-Moretti.Covid-19. Environ 35 500 cas quotidiens de Covid-19 avaient ??t?? d??tect??s en moyenne sur sept jours jeudi, contre pr??s de 34 900 une semaine plus t??t, et plus de 5 900 personnes se trouvaient en r??animation, soit 200 de plus en une semaine, selon le minist??re de la Sant??. Jeudi soir, pr??s de 12 millions de personnes avaient re??u au moins une dose de vaccin contre le Covid-19, selon Sant?? publique France, un organisme public d??pendant du minist??re de la Sant??. La vaccination est ??tendue depuis lundi aux personnes de 55 ans et plus. Le Premier ministre, Jean Castex, a annonc?? mardi la suspension des vols depuis et vers le Br??sil, en raison de la forte circulation dans le pays du variant P1, tr??s contagieux.",
          "voiceGender": "female",
          "source": ""
        }
      ]
    },
    {
      "title": "Talibans",
      "articles": [
        {
          "title": "",
          "body": "La Maison-Blanche a annonc?? mardi que le retrait des 2 500 soldats am??ricains encore d??ploy??s en Afghanistan s???ach??verait d???ici le 11 septembre. Le pr??c??dent pr??sident am??ricain, Donald Trump, s?????tait engag?? ?? retirer les troupes am??ricaines avant le 1er mai 2021, lors d???un accord sign?? en f??vrier 2020 avec les talibans. ?? Taliban ?? est le pluriel de ?? taleb ??, un mot d??signant en arabe et en pachto un ??tudiant en th??ologie, ce qui explique les deux orthographes au pluriel avec ou sans ?? s ??. Au d??but des ann??es 1990 se forme en Afghanistan un mouvement de combattants islamistes compos?? en grande partie d???anciens ??tudiants des ??coles coraniques, lui donnant leur nom. Ces combattants prennent le pouvoir dans le pays en 1996, imposant de nombreuses restrictions ?? la population. En 2001, ils sont destitu??s lors d???une intervention dirig??e par les ??tats-Unis qui les accusent de prot??ger le mouvement terroriste Al-Qa??da. Depuis, les talibans ont repris le contr??le de larges portions du pays. Ils ont revendiqu?? de nombreux attentats ces derni??res ann??es.",
          "voiceGender": "female",
          "source": ""
        }
      ]
    },
    {
      "title": "??a vaut un clic",
      "articles": [
        {
          "title": "",
          "body": "La rumba congolaise. La rumba congolaise, un style musical des deux Congo, est candidate ?? l???inscription sur la liste du patrimoine immat??riel de l???humanit??. Dans un article, RFI Musique revient sur les quelque 80 ans d???existence de la rumba congolaise, inspir??e de la musique cubaine, ses ??volutions et la place qu???elle occupe dans la soci??t??, jusqu????? devenir repr??sentative ?? de l???identit?? du peuple congolais ??. Cet article s???accompagne d???une playlist r??alis??e par RFI pour d??couvrir ce style particuli??rement dansant. Alicia, 16 ans, escort. Alicia, 20 ans, raconte, dans l?????mission de France Culture ?? Les Pieds sur Terre ??, comment elle est devenue escort pendant pr??s de deux mois ?? 16 ans. Apr??s la d??couverte imp??rieuse de sa sexualit?? et une rencontre fortuite, elle se prostitue via les applications Tinder et Snapchat, sans jamais tomber dans le pi??ge des prox??n??tes ni de la drogue. ?? Si moi j???ai pu le faire, combien d???autres filles de mon ??ge, voire plus jeunes, l???ont fait sous l???influence d???un prox??n??te ? ??, se demande-t-elle dans un t??moignage plein de lucidit??. ?? Mon oncle ??. ?? travers une belle s??rie photo en noir et blanc publi??e sur le site du journal suisse Le Temps, le photographe fran??ais Corentin Fohlen rend hommage ?? son oncle, surnomm?? ?? l???original de la famille ??. Il dresse un portrait tendre de son parrain, qu???il voit comme un ?? g??nie g??nial ??, ?? sans limite ??, et le repr??sente couvert de boue, en pleine manifestation des gilets jaunes ou encore en chaman, tout nu sur une pirogue. Lettres d???amour. Dans ?? The Letter Room ??, un court-m??trage diffus?? sur Arte.tv, un agent p??nitentiaire aux ??tats-Unis est affect?? au courrier des d??tenus. Il doit tout examiner avant la distribution, mais a interdiction de lire les lettres en entier. Sauf qu???il va ??tre intrigu?? par la correspondance d???une femme, Rosita, ?? un d??tenu condamn?? ?? mort. ?? la lecture de ces lettres d???amour, pleines de po??sie et de romantisme, il fait une d??couverte qui va le pousser ?? rendre visite ?? Rosita. ?? The Letter Room ?? est en lice pour l???Oscar du meilleur court-m??trage.",
          "voiceGender": "female",
          "source": ""
        }
      ]
    },
    {
      "title": "",
      "articles": [
        {
          "title": "",
          "body": "Vous voil?? ?? brief??s ?? sur l???actu de la semaine. Passez un bon week-end ?? vivre d???amour et d???eau fra??che.",
          "voiceGender": "female",
          "source": ""
        }
      ]
    }
  ]
}

Newsletter.objects.create_or_update_newsletter(YourModel, json_content)
```

### Private RSS feed
You can create an RSS feed for your users to use with podcast applications like Pocket Casts or Overcast.

You can handle RSS feed in the admin or with code:

#### Create a private RSS feed
```python
from podle.models import RssFeed

RssFeed.objects.create(user=user)
```

#### Get an existing private RSS feed
```python
from podle.models import RssFeed

RssFeed.objects.get_rss_feed(user=user)
```

#### Delete a private RSS feed
```python
from podle.models import RssFeed

RssFeed.objects.get(user=user).delete()
```

#### Create or delete Rss feeds
Adding a single user or users to the group defined in the PODLE_RSS_FEED_GROUP_NAME setting
will create or delete the rss feed for those users.

#### Batch create of delete Rss feeds
__Important__: In order to use those two endpoints you need to ask Podle to activate them and allocate the resources otherwise it will break.

Here is an example of usage:
```python
from django.contrib.auth import get_user_model
from podle.models import RssFeed
User = get_user_model()

users = User.objects.all()

RssFeed.objects.create_rss_feed(users)

RssFeed.objects.delete_rss_feed(users)
```
