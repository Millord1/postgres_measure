# Brief : restituer et publier son travail

> Ici, le livrable n'est pas le code : c'est une page en ligne, propre, relue, qui présente votre démarche et vos chiffres.

Vous repartez du travail rendu sur le brief « insérer des données » (vos méthodes, votre tableau, votre graphique). Objectif : le transformer en page web publiée.

> Compétences visées (RNCP-37638) : **CT6** (présenter un travail réalisé) et **CT8** (interagir professionnellement : branches, revue de code).

## Situation professionnelle

Un·e data engineer ne livre jamais « un script ». Il livre un résultat **reproductible** que d'autres relisent, comprennent et déploient. Le code passe par une revue avant d'être intégré, et les résultats sont restitués dans un format consultable par tous, y compris ceux qui ne lisent pas Python.

## L'outil : Quarto

Quarto rend vos notebooks `.ipynb` et vos fichiers `.py` directement en site web, **sans écrire une seule ligne de HTML**, et le publie sur GitHub Pages en une commande.

- Installation : [quarto.org/docs/get-started](https://quarto.org/docs/get-started/)
- Vérifiez : `quarto --version`

## 1. Organiser le travail 

- Des commits petits et nommés clairement (un commit = une intention).

## 2. La revue de code croisée

> 🔴 Chaque groupe relit le rendu d'un autre groupe et essaie de relever :


- une chose qui n'est pas claire (un nom, une fonction, un résultat non expliqué) ;
- une amélioration concrète (factorisation, lisibilité, doc manquante) ;
- une chose qui est bien faite, et pourquoi.

## 3. Construire la page

- `quarto render` génère le site dans `_site/`. Ouvrez le résultat en local d'abord.
- Une page d'accueil en `index.qmd` : le contexte, les questions (la méthode la plus rapide ? la plus simple ?), vos recommandations.
- Vos notebooks deviennent des pages : Quarto exécute le code et affiche tableau et graphique au rendu.
- Soignez le texte : un·e lecteur·ice non technique doit comprendre l'écart de performance et pourquoi.

## 4. Publier sur GitHub Pages

- Dépôt poussé sur GitHub, puis : `quarto publish gh-pages`.
- La commande construit le site, le pousse sur la branche `gh-pages` et active Pages. L'URL s'affiche à la fin.
- Vérifiez le lien depuis un autre poste : si ça ne s'ouvre pas ailleurs que chez vous, ce n'est pas publié.

## Livrables

| Livrable | Forme |
|---|---|
| Le travail rendu via git | historique git |
| Une revue de code croisée argumentée | commentaires sur la PR d'un autre groupe |
| Le site Quarto | sources `.qmd` / `.ipynb` + `_quarto.yml` |
| La page publiée | une URL `github.io` qui s'ouvre |

## Indicateurs de performance

- le travail passe par `git` pour l'historisation 
- la revue croisée est faite et utile (trois retours concrets si possible), et prise en compte via un nouveau `commit` ;
- le site est généré par Quarto, sans HTML écrit à la main ;
- la page est réellement en ligne (via Github Pages) et accessible depuis un autre poste ;
- **la restitution est lisible par un·e non-spécialiste** : contexte, résultats, recommandation.

## Modalités

- Travail en groupe, revue croisée entre groupes.
- Prérequis : le rendu du brief « insérer des données », un compte GitHub, Quarto installé.
- Durée indicative : une demi-journée.
- 🔴 Le contenu (code, mesures, analyse) est le vôtre. Quarto et GitHub Pages ne font que le publier.