Ce programme permet de générer, afficher et résoudre un labyrinthe aléatoire à l’aide d’une interface graphique Tkinter.
Deux algorithmes de recherche sont proposés :

- BFS (Breadth-First Search) : recherche en largeur, garantit le chemin le plus court.
- DFS (Depth-First Search) : recherche en profondeur, plus rapide mais pas toujours optimal.
Le programme permet aussi de comparer les temps d’exécution et d’afficher des graphiques d’analyse.

Fonctionnalités principales :

- Génération d’un labyrinthe aléatoire (tailles impaires uniquement).
- Résolution automatique avec BFS ou DFS.
- Comparaison du temps d’exécution entre BFS et DFS.
- Graphique du temps moyen en fonction de la taille du labyrinthe.

Remarques :
- Plus la taille du labyrinthe est grande, plus la génération et la résolution sont longues.
- Le zoom d’affichage peut être ajusté dans la fonction afficher() (valeur par défaut ×3).
- Les bibliothèques nécessaires : tkinter, Pillow, matplotlib.
