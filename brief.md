# Brief : insérer des données

> Le « transvasement » (i.e. l'insertion de lignes depuis Python vers PostgreSQL) peut être réalisé de différentes façons, et avec un facteur d'au moins 100 entre la méthode la plus lente et la méthode plus rapide. L'objectif est ici de comparer différentes méthodes et le temps nécessaire pour leur exécution.

- vous allez charger un même jeu de données en base de plusieurs manières 
- chronométrer chacune
- expliquer pourquoi les écarts sont aussi grands

**L'enjeu n'est pas d'apprendre la syntaxe par coeur**, mais de comprendre **d'où vient la lenteur** et de savoir choisir la bonne méthode selon le contexte.

> Compétence visée (RNCP-37638) : **C11, niveau 1-2** : « créer une base de données [...] et **en programmant leur import**. Réinvestissement de C8 (automatisation) et du module numérique responsable (sobriété : un import efficace, c'est moins de CPU et de temps machine).

## Situation professionnelle emblématique

- Vous êtes data engineer et votre script d'ETL charge un fichier de quelques milliers de lignes en base, toutes les nuits.
- Le volume monte : le client passe de 5 000 à 2 millions de lignes par jour. Le chargement, qui prenait 3 secondes, prend maintenant 40 minutes et fait sauter la fenêtre de traitement nocturne.
- On vous demande de **diagnostiquer** et de **réécrire l'étape d'import**, chiffres à l'appui, sans changer le résultat en base.

**⚠️ « Ça marche » n'est pas « ça tient à l'échelle ». La même boucle d'insertion qui passe sur 1 000 lignes peut être inexploitable sur 1 million.**

## 1. Préparer le jeu de données et la table

- Générez (ou récupérez) un jeu d'au moins **plusieurs colonnes et trois tailles** : 1 000, 100 000 et 1 000 000 de lignes. 
- Un `DataFrame` pandas ou une liste de tuples conviennent.  
- Variez les types (entier, texte, date, float) pour que ce soit réaliste.
- Créez une table PostgreSQL cible avec ses contraintes. 
- Prévoyez un `DROP`/`CREATE`  (ou `TRUNCATE`) entre chaque méthode : on repart toujours d'une table vide pour comparer dans des conditions identitques.

> 🟠 Le générateur de données et la création de table ne doivent pas être chronométrées. On ne mesure que l'insertion.

## 2. Les méthodes à comparer

Implémentez **au minimum les six premières**. Les suivantes sont des bonus pour creuser.

| # | Méthode | Idée |
|---|---|---|
| 1 | `cursor.execute()` dans une boucle `for`, un `commit()` par ligne | la version naïve |
| 2 | `cursor.execute()` dans une boucle `for`, **un seul** `commit()` à la fin | mesurer l'effet de la transaction unique |
| 3 | `cursor.executemany()` | la méthode « évidente » (pourtant assez lente) |
| 4 | `psycopg2.extras.execute_batch()` (jouez sur `page_size`) | regroupe les requêtes en paquets |
| 5 | `psycopg2.extras.execute_values()` (jouez sur `page_size`) | un seul `INSERT` à valeurs multiples |
| 6 | `COPY` via `cursor.copy_expert()` + `StringIO` | le chemin rapide de PostgreSQL |
| 7  | `pandas.to_sql()` par défaut | la facilité (mais pas la plus rapide!!) |
| 8  | `pandas.to_sql(method='multi', chunksize=...)` | la variante « groupée » de pandas |
| 9 💫 | `pandas.to_sql(method=callable)` branché sur `COPY` | le meilleur des deux mondes |
| 10 💫 | `COPY` via un itérateur (sans tout charger en mémoire) | le plus rapide ET le plus sobre en RAM |

- Chaque implémentation doit produire **exactement le même contenu** en base. 
- Vérifiez-le par un `SELECT count(*)` et un contrôle de cohérence après chaque méthode.

## 3. Le protocole de mesure

- Chronométrez **uniquement** l'insertion, avec `time.perf_counter()` (pas `time.time()`).
- **Répétez** chaque mesure au moins 10 fois et gardez la médiane : une mesure unique ne vaut rien.
- Faites varier la **taille** (1 k / 100 k / 1 M) : certaines méthodes sont correctes à petite échelle et mais pas à grande échelle.
- Notez aussi, quand vous le pouvez, la **mémoire** consommée (la méthode 6 via `StringIO` est rapide mais gourmande en RAM ; la méthode 10 corrige ça).


## 4. Restituer les résultats

- Un **tableau** récapitulatif : méthode × taille -> temps médian (et mémoire si mesurée).
- Un **graphique** (matplotlib) temps en fonction de la taille (échelle log utile vu les écarts)
- Une **analyse écrite** : pourquoi ces écarts de temps ? 

Ordres de grandeur observés dans la littérature (benchmark de référence, ~32 000 lignes, à titre indicatif, vos chiffres dépendront de votre machine) :

| Méthode | Temps relatif |
|---|---|
| insertion ligne par ligne | ≈ 128 s |
| `executemany()` | ≈ 125 s (à peine mieux : ça reste un `INSERT` par ligne) |
| `execute_batch()` | ≈ 2,5 à 4 s |
| `execute_values()` | ≈ 1,5 à 3,7 s |
| `COPY` (StringIO / itérateur) | ≈ 0,5 à 0,6 s |

> 🔴 Ces chiffres sont une indication, et en aucun cas une cible !! On attend **vos** mesures, sur **votre** machine, avec le constat de l'écart et son explication.

## Livrables

| Livrable | Forme |
|---|---|
| Le script de génération et de création de table | `.py` ou notebook |
| Les implémentations des méthodes | une fonction par méthode|
| Le tableau et le graphique des temps | dans le notebook ou un `.md` |
| L'analyse écrite des écarts | quelques paragraphes : round-trips, transaction, COPY |

Le tout versionné dans le dépôt `simplon-de-indiv`.

## Indicateurs de performance


- au moins six méthodes implémentées et **fonctionnellement équivalentes** (même contenu final en base, vérifié) ;
- le protocole de mesure doit être honnête et valide statistiquement : répétitions, médiane, plusieurs tailles, chronomètre posé au bon endroit (insertion seule) ;
- les résultats sont présentés lisiblement (tableau + graphique) et l'écart de plusieurs ordres de grandeur est constaté ;
- l'analyse identifie correctement la cause (allers-retours serveur, regroupement des requêtes, rôle de la transaction et de `COPY`) ;
- une recommandation de choix est formulée selon le contexte (petit volume vs gros volume, contraintes mémoire) ;
- votre analyse précisera les liens vers la documentation officielle de chacune des méthodes utilisées
- **prise en compte de la sobriété (temps machine, mémoire) en lien avec le module numérique responsable.**

## Modalités pédagogiques

- TP technique en présentiel de la phase 2 (ETL et chargement d'entrepôt) et le module numérique responsable
- Travail en binôme, en autonomie accompagnée
- Prérequis : psycopg2 et pandas (semaine 02), SQL et `CREATE TABLE` 
- Durée indicative : une demi-journée
- 🔴 Aucun usage de LLM pour produire le code des méthodes (le brief n'aurait alors plus aucun intérêt)

## Modalités d'évaluation

- Le travail est rendu sous forme de commits git. 
- Le barème suit les indicateurs ci-dessus : 
    - couverture et équivalence des méthodes
    - sérieux du protocole
    - qualité de la restitution
    - justesse de l'analyse

