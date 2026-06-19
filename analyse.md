# Analyse des résultats

## Les cursor.execute()

Sans surprise les moins performants, simplement car ils insèrent ligne par ligne en database donc ils crééent un nombre énorme de requête. Légère amélioration des performances quand on stock toutes les requetes dans une transaction (commit()) hors de la boucle mais non significatif

## execute_many, execute_bach, execute_value

execute_values est le plus performant, en 1k, 100k ou 1M. Execute_batch est légèrement plus lent alors que executemany est significativement plus lent, que ce soit pour 1k, 100k ou 1M d'insertions
Ils font des insert massifs en base de données mais n'appellent pas de méthodes particulièrement efficaces comme on verra ensuite.
Très simples à utiliser et relativement performants pour des insertions qui ne sont pas massives

## COPY Expert, pandas default et pandas multi

### INSERT compare les valeurs, COPY 'shortcut' les analyses SQL

On peut voir que les méthodes de pandas, multi ou default sont assez similaires en terme de performances, pandas default semble même légèrement surperformer pandas multi. 
Par contre COPY Expert est nettement plus performant que les méthodes précédentes
COPY Expert utilise la méthode COPY de postgres et push du text virtuel, rendant la methode très efficace.
Panda default est optimisé en bas niveau mais reste une multitude d'inserts
pandas multi fait un execute_values mais, encore une fois, optimisé bas niveau

## Pandas callable et COPY

Ici les deux méthodes ont des performances assez similaires en terme de durée de traitement, COPY reste plus performant mais l'écart se ressert clairement à partir de 100k insertions. Par contre en terme d'usage de mémoire RAM, COPY est nettement meilleur que toutes les autres méthodes avec une utilisation mémoire mesurée à peine plus élevée que 0 Mo.

Exploitent toutes deux la puissance du COPY de spotgreSQL. 
La version de panda utilise un chunk pour découper les données et accélérer l'insertion massive.
La version de COPY on stream est simplement la plus performante car elle élimine l'allocation mémoire intermédiaire (stockage intermédiaire) en créant un pipeline direct
