# Automatisches Beweissystem

Dieses Projekt erlaubt dir eine Sprache und ein paar Axiome festzulegen, z.B. kannst du die Gruppentheorie oder die Bool'sche Logik nachbilden.
Anschließend kann das Programm für eine beliebige Aussage in der Sprache versuchen sie zu beweisen.

### Sprache festlegen und Axiome spezifizieren
Als Beispiel verwenden wir hier die Bool'sche Logik. Nach einer solchen Syntax können Operatoren in der Sprache festgelegt werden:
``` python
class Null(Funktion):
    argumentzahl=0
    symbol = "0"

class Eins(Funktion):
    argumentzahl=0
    symbol = "1"

class Nicht(Funktion):
    argumentzahl = 1
    symbol = "!"

class Und(Funktion):
    argumentzahl = 2
    symbol = "^"

class Oder(Funktion):
    argumentzahl = 2
    symbol = "v"
```

Anschließend kann man Axiome definieren:
```python
axiome = []

axiome.append(  (Und(t1,t2)  ,  Und(t2,t1))  )      # Kommutativ
axiome.append(  (Oder(t1,t2)  ,  Oder(t2,t1))  )      # Kommutativ

axiome.append(  (Und(t1,Oder(t2,t3))  ,  Oder(Und(t1,t2),Und(t1,t3)))  )      # Distributivität
axiome.append(  (Oder(t1,Und(t2,t3))  ,  Und(Oder(t1,t2),Oder(t1,t3)))  )      # Distributivität

axiome.append(  (Und(t1,Eins())  ,  t1)  )      # Neutralelement
axiome.append(  (Oder(t1,Null())  ,  t1)  )      # Neutralelement

axiome.append(  (Und(Nicht(t1),t1)  ,  Null())  )      # Inverse / Komplement
axiome.append(  (Oder(Nicht(t1),t1)  ,  Eins())  )      # Inverse / Komplement
```

Dabei gilt, dass der erste Teil jedes tupels durch den zweiten Teil ersetzt werden darf. Die Variablen t1, t2 ... stehen dabei für beliebige Terme.
Nach diesem Muster kann somit in jeder beliebigen Theorie gearbeitet werden und es können zusätzliche Annahmen in Form von weiteren Axiome hinzugenommen werden.

### Aussagen Beweisen

Am Ende der Main Datei kann man zwei Terme übergeben. Die Funktion versucht dann einen Beweis zu finden, dass beide Aussagen äquivalent sind. Gelingt dies,
so wird ein kompletter formaler Beweis ausgegeben.
```python
if __name__ == '__main__':
    beweis_ausgeben_wenn_beweisbar(Und(a,a),a)
```
Ausgabe:

![](https://github.com/rayklauck/Beweissystem/blob/b5472a0c64b0f29d8889273645a42492bd8d1def/Beispielbeweis-teil1.png)
![](https://github.com/rayklauck/Beweissystem/blob/b5472a0c64b0f29d8889273645a42492bd8d1def/Beispielbeweis-teil2.png)

### Prinzip

Basierend auf den definierten Operatoren entsteht eine Sprache legaler Terme. Um zu zeigen, dass zwei Aussagen äquivalent sind, muss gezeigt werden wie nur
durch Axiome die eine Aussage in die andere umgewandelt wird. 
+ erstelle die ersten n Terme der Sprache (wobei das Programm eine eigene Definition 'erste' verwendet)
+ erstelle eine Union-Find Datenstruktur für die Terme
+ versuche für jedes Paar von zwei Termen, ob sie sich durch die Anwendung eines Axioms ineinander Umwandeln lassen
  + wenn das geht, dann verschmelze die Äquivalenzkomponenten, in denen sie sich befinden
+ verwende den Determinismus von Funktionen, um weiterhin Komponenten zu verschmelzen: Seien A, B und C Terme. A und B seien äquivalent, sprich A = B. 
Dann gilt für jede Funktion f mit zwei Argumenten: f(A,C) = f(B,C)
+ speichere für jede Äquivalenz aufgrund welches Axioms oder welchem Funktionsdeterminismus sie gilt.
+ schaue ob beide Terme in der gleichen Äquivalenzklasse sind
  + wenn ja, dann verwende BFS um im Graph der beweisenen Äquivalenzen einen Pfad von der einen Aussage zu anderen zu finden. Gebe das aus
  
### Reflektion

Wenn es einen validen Beweis gibt, so wird nicht notwendigerweise der kürzeste gefunden. Durch den Funktionsdeterminismus werden Zwischenresultate bewiesen,
die anschließend verwendet werden können. Dies wird in der Ausgabe durch verschiedene Einrückungen dargestellt.

Es wird nur auf einer endlichen Menge von Termen gearbeitet. Wenn es einen Beweis gibt, der jedoch über einen Term geht, der nicht in der Termmenge ist,
so wird dieser Beweis nicht gefunden. Sind jedoch alle Zwischenterme in der Termmenge, so ist es sicher, dass der Beweis (oder ein anderer valider Beweis)
gefunden wird.

Die Laufzeit ist quadratisch in der Anzahl der Terme, da für jedes paar von Termen geprüft wird, ob sie durch ein Axiom ineinander umwandelbar sind. Die 
Anzahl der Terme wächst jedoch mit dem Grad der Verschachtelung, den man erlaubt, exponentiell.
