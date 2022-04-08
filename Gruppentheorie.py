from Terme import *

### definiere die spezifischen Funktionen

class E(Funktion):
    argumentzahl=0
    symbol = "e"

class Invers(Funktion):
    argumentzahl = 1
    symbol="!"


class Stern(Funktion):
    argumentzahl = 2
    symbol = "*"

definierte_funktionen = [E,Invers,Stern]




### Axiome werden als tupel geschrieben, wobei StrukturVariablen t1, t2, t3 als Platzhalter für Termreste stehen

# Assoziativität
axiome =[]
axiome.append(  (Stern(Stern(t1,t2),t3),Stern(t1,Stern(t2,t3)))  )

# Neutralelement
axiome.append(  (Stern(E(),t1),t1)  )   # links
axiome.append(  (Stern(t1,E()),t1)  )   # rechts

# Inverses
axiome.append(  (E(),Stern(t1,Invers(t1)))  )   # rechts
axiome.append(  (E(),Stern(Invers(t1),t1))  )   # links

# zusatz für besondere Gruppenart
#axiome.append(   (t1  ,  Invers(t1))   )
#axiome.append(  (Stern(t1,t1),  t1)  )
#axiome.append(   (Stern(t1,t2), Stern(t2,t1))   )     # kommutativ
#axiome.append(  (Stern(t1,t1),E())  )   # g*g=e
#axiome.append(  (Stern(t1,t3), Stern(t2,t3))  )



# definieren welche Sachen nicht für alles gelten, aber für eine bestimmte Variable als Spezialfall
#merge(Obj_zu_KnotenNr[Stern(a,b)], Obj_zu_KnotenNr[a])      # als Beispiel


