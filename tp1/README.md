	Explication de l’implémentation 1 (algorithme arborescent)
Pour l’algorithme arborescent, nous avons choisi d’utiliser un algorithme A*.
Heuristique :   h(n)= K *n  
« K » étant le cout de l’ajout d’une antenne (sans compter le rayon) et « n » étant de points non couverts. Le but d’une heuristique est d’estimer la distance entre l’état évalué et notre but. Celle-ci est simplement de constater si notre action couvre un nouveau point. Il ne s’agit pas d’une heuristique vérifiée, mais elle nous aide quand même bien à atteindre notre but.
Cout :  
« K » étant le cout de l’ajout d’une antenne, « C » la constante multiplicative du cout associé au rayon, « n » étant de points non couverts et « r » étant le rayon de l’a « nem» antenne. Le but de ce cout est d’évaluer le cout de la solution.
Finalement, f(n) = g(n)+h(n) évalue la combinaison du cout pour ce rendre a un état et la distance de celui-ci par rapport au but tout en guidant l’algorithme A* vers une solution optimale.

Voisinage :
	Ajouter une antenne sur n’importe quel point non couvert;
	Ajouter une antenne entre n’importe quel pair de points non couvert proche un de l’autre (distance plus petite que la moyenne des distances entre tous les points);
	Grossir le rayon de n’importe quelle antenne en ajoutant le point non couvert le plus proche. Cette action repositionne l’antenne au barycentre de ces points couverts et change sont rayon par la distance entre celle-ci et sont point le plus éloigné.



	 Explication de l’implémentation 2 (algorithme de recherche local)
Nous avons décidé d’utiliser l’algorithme de recuit simulé. Nous utilisons la même heuristique et le même cout pour évaluer nos états. Les transitions qui suivent un peux la même philosophie de couverture, mais sous forme simplifié et aléatoire. 

Voisinage :
	Ajouter une antenne sur un point aléatoire non couvert;
	Ajouter une antenne entre un pair de points aléatoires non couverts proche un de l’autre (distance plus petite que la moyenne des distances entre tout les points);
	Grossir le rayon d’une antenne aléatoire et grandir son rayon d’une taille aléatoire en ajoutant les points non couverts.

La différence est que nous appelons cet ensemble d’états sur un algorithme de recuit simulé qui était disponible avec le TP. De cette manière, les actions sont appelées de manière aléatoire alors on obtient des solutions (ou des non-solutions) de manière aléatoire. L’algorithme continue de trouver des solutions aléatoires en gardant seulement la meilleure de celle-ci.









Question 1
Ceci est une fonction qui prend comme paramètre une liste de prédicats (des fonctions que retourne truie or fasse) et une liste de paramètre quelconque. Ensuite, la fonction utilise «filer » qui prend chaque paramètre de inputList et utilise la fonction qui est en premier paramètre de « filter » dessus.  La fonction qui est en premier paramètre de « filter » est créée à l’aide de « lambda » ce qui permet de créer rapidement une fonction sans avoir à la déclarer, etc. Ici, lambda x : signifie que x sera le paramètre de la fonction alors lorsque que cette fonction « filter » sera appeler elle sera comme ceci : « filter( all(f(Elementdeinputlist) for f in predList), inputList). » La fonction «all» prend une liste de prédicats et retourne true seulement si tous les éléments de la liste sont true. « f(x) for f in predlist» signifie que l’on exécute chaque fonction dans predlist avec le paramètre x. Donc, la fonction complète fait que on créer une liste de tous les éléments de inputList ayant retourné « truie » à chacun des prédicats de « predList » (après avoir été passer en paramètre à ces prédicats). Cette fonction peut être utilisée pour sélectionner par exemple des candidats pour une équipe sportive de rêve. Par exemple, predList contiendrais une liste de prédicats que les candidats se doivent d’avoir pour être dans l’équipe de rêve (exemple : a un bon lancé, cours assez vite, est assez grand, etc). Ensuite, on pourrait utiliser la fonction « fct » en passant par paramètre cette liste de prédicats et une liste de tous les joueurs existants et on obtiendrait une liste des joueurs ayant réussi tous les tests de la liste.


Question 2
La principale force notre implémentation de  l’algorithme A* est que celle-ci suit toujours le un chemin optimal vers la solution. Donc si l’échantillon est petit la solution est garantie en très peu de temps. Le désavantage de notre algorithme A* est qu’il possède un nombre de transitions possibles proportionnelles à la taille de l’échantillon. Nous avons observé que l’algorithme  est extrêmement inefficace pour un échantillon plus gros que 100 points.
La principale force de l’algorithme de recuit simulé est sa simplicité d’implémentation et le fait qu’il ne tombe pas dans des minimums locaux. C’est un algorithme très pratique lorsque l’échantillon n’est pas trop grand. Cela dit, cet algorithme est susceptible à ne pas retourner la bonne solution si on ne lui donne pas le temps nécessaire, ce qui dans certains cas peut s’avérer à un temps très élevé. C’est un algorithme qui utilise le hasard ce qui peut jouer pour et contre nous, dépendant des cas.



