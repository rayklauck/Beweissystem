from Terme import *



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


definierte_funktionen = [Null,Eins,Nicht,Und,Oder]


"""
kompakte Definition nach Huntington
"""
axiome = []

axiome.append(  (Und(t1,t2)  ,  Und(t2,t1))  )      # Kommutativ
axiome.append(  (Oder(t1,t2)  ,  Oder(t2,t1))  )      # Kommutativ

axiome.append(  (Und(t1,Oder(t2,t3))  ,  Oder(Und(t1,t2),Und(t1,t3)))  )      # Distributivität
axiome.append(  (Oder(t1,Und(t2,t3))  ,  Und(Oder(t1,t2),Oder(t1,t3)))  )      # Distributivität

axiome.append(  (Und(t1,Eins())  ,  t1)  )      # Neutralelement
axiome.append(  (Oder(t1,Null())  ,  t1)  )      # Neutralelement

axiome.append(  (Und(Nicht(t1),t1)  ,  Null())  )      # Inverse / Komplement
axiome.append(  (Oder(Nicht(t1),t1)  ,  Eins())  )      # Inverse / Komplement


