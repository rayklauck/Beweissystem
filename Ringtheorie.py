from Terme import *

class Null(Funktion):
    argumentzahl=0
    symbol = "0"

class Eins(Funktion):
    argumentzahl=0
    symbol = "1"

class Minus(Funktion):
    argumentzahl = 1
    symbol="-"

#class Durch(Funktion):
#    argumentzahl = 1
#    symbol="/"

class Plus(Funktion):
    argumentzahl = 2
    symbol = "+"

class Mal(Funktion):
    argumentzahl = 2
    symbol = "*"

definierte_funktionen = [Null,Eins,Minus,Plus,Mal]
axiome = []
axiome.append(  (Plus(Plus(t1,t2),t3),Plus(t1,Plus(t2,t3)))  )      # Ass Plus
axiome.append(  (Plus(t1,Null())  ,  t1)  )      # NE Plus
axiome.append(  (Plus(Null(),t1)  ,  t1)  )      # NE Plus
axiome.append(  (Plus(Minus(t1),t1)  ,  Null())  )      # Invers Plus
axiome.append(  (Plus(t1,Minus(t1))  ,  Null())  )      # Invers Plus

axiome.append(  (Mal(Mal(t1,t2),t3),Mal(t1,Mal(t2,t3)))  )      # Ass Plus
axiome.append(  (Mal(t1,Eins())  ,  t1)  )      # NE Mal
axiome.append(  (Mal(Eins(),t1)  ,  t1)  )      # NE Mal

axiome.append(  (Mal(t1,Plus(t2,t3))  ,  Plus(Mal(t1,t2),Mal(t1,t3)))  )      # Distributivität
axiome.append(  (Mal(Plus(t2,t3),t1)  ,  Plus(Mal(t2,t1),Mal(t3,t1)))  )      # Distributivität


# Auswahl von Termen, um a*0 = 0 zu beweisen
"""
alles = [Null(),
         Mal(Null(),a), Plus(Null(),a),a,
         Plus(Mal(Null(),a),a), Plus(Mal(Null(),a),Mal(Eins(),a)),
         Mal(Plus(Null(),Eins()),a), Mal(Eins(),a),Eins(),Plus(Null(),Eins()),
         Plus(Plus(Mal(Null(),a),a),Minus(a)), Plus(Plus(Null(),a),Minus(a)),
         Plus(Mal(Null(),a),Plus(a,Minus(a))), Plus(Null(),Plus(a,Minus(a))),
         Plus(a,Minus(a)), Plus(Mal(Null(),a),Null())]
"""