contenu(eau).
contenu(alcool).
liquide(eau).
objet(verre).


gele(eau) :- temperature(eau,Y), Y=<0.
ebulition(eau) :-  temperature(eau,Y), Y>=100.

froid(eau) :-  temperature(eau,Y), Y=<10.

class :- eau.
subclass(perrier,eau).
class(alcool).

contient(verre,X) :- contenu(X).
possede(joao,X) :- objet(X).

possede(joao,X) :- verre(X), contient(verre,perrier),
			contient(verre,G),G==eau, temperature(G,-10).



possede(joao,A) :- verre(A), contient(verre,alcool).







%Soit deux verres identiques (ils ont donc le même poids), un contenant de l'eau et l'autre contenant une même quantité d'alcool. Celui qui contient de l'eau est plus lourd.
%João a un autre verre, identique au premier, qui contient de l'alcool.
