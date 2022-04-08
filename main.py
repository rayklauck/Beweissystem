"""
Ray Klauck   März 2022
Programm zum automatisierten Beweisen mittels Äquivalenzklassen
"""



# Hilfsfunktionen

def dict_verträglich(d1,d2):
    # prüft, dass kein Key der in beiden vorkommt zu unterschiedlichem Wert führt
    for k,v in d1.items():
        if k in d2.keys() and not d1[k]==d2[k]:
            return False

    for k,v in d2.items():
        if k in d1.keys() and not d1[k]==d2[k]:
            return False
    return True



### allgemeine Struktur von Termen bestehend aus definierten Funktionen und freien Variablen

class Term():
    def __init__(self):
        pass

    def __repr__(self):
        return str(self)

    def __hash__(self):                 # macht das alles wieder Hashable
        return str(self).__hash__()     # Achtung nicht ganz ungefährlich! Sicherstellen dass verschiedene Terme stehts verschiedene strings darstellen
                                        # und dass Variablen nur nach ihrem Namen beurteilt werden!!

class Variable(Term):
    """
    Elementare Variable, die auch nicht für einen Term steht, sondern nur für sich selbst
    """
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name
    def __eq__(self, other):
        if self.__class__!=other.__class__:
            return False
        return self.name==other.name
    def __copy__(self):
        return self.__class__(self.name)
    def __hash__(self):
        return super().__hash__()

class StrukturVariable(Variable):
    """
    kommen nur vor um die Struktur von Axiomen usw darzustellen. Sind Platzhalter für beliebige Terme
    """
    pass

class Funktion(Term):
    argumentzahl = 0
    symbol = "_"

    def __init__(self,*args):
        assert len(args)==self.argumentzahl
        self.terme=list(args)

    def __hash__(self):
        return super().__hash__()

    def __eq__(self, other):
        # gleich wenn gleiche Funktionsart und alle Argumente gleich
        if self.__class__!=other.__class__:
            return False
        for i in range(self.argumentzahl):
            if self.terme[i]!=other.terme[i]:
                return False
        return True

    def __copy__(self):
        return self.__class__(*self.terme)

    def __str__(self):
        if self.argumentzahl==0:
            return self.symbol
        elif self.argumentzahl==1:
            return self.symbol+"(" + str(self.terme[0]) + ")"
        elif self.argumentzahl==2:
            return "("+str(self.terme[0])+self.symbol+str(self.terme[1])+")"
        else:
            return "DARSTELLUNGSFEHLER"


#axiome = []
#definierte_funktionen = []
t1,t2,t3 = StrukturVariable("t1"),StrukturVariable("t2"),StrukturVariable("t3")
a,b,c = Variable("a"),Variable("b"),Variable("c")

from BoolscheLogik import *    # Hier die konkrete Theorie importieren, mit der du arbeiten willst


class Übergang():
    def __init__(self, func, argumente_an_stelle):
        assert len(argumente_an_stelle) == func.argumentzahl
        self.func = func

        self.argumente_an_stelle = argumente_an_stelle

    def einsetzen(self,wie,von,nach):
        neu = self.__class__(self.func,self.argumente_an_stelle.copy())
        for k,v in wie.items():
            for i in range(len(neu.argumente_an_stelle)):
                if str(neu.argumente_an_stelle[i])==k:
                    neu.argumente_an_stelle[i]=v
        neu.von, neu.nach = von, nach  # auch speichern zwischen welchen Knotennr die Kante besteht. Nur wichtig um später die Beweisführung rückverfolgen zu können
        return neu

    def __str__(self):
        if self.func.argumentzahl==1:
            return self.func.symbol+"(...)"
        elif self.func.argumentzahl==2:
            s=""
            if self.argumente_an_stelle[0]!=None:
                s+=f"{self.argumente_an_stelle[0]}"
            else:
                s+="(...)"
            s+=self.func.symbol
            if self.argumente_an_stelle[1]!=None:
                s+=f"{self.argumente_an_stelle[1]}"
            else:
                s+="(...)"
            return s
        else:
            return "DARSTELLUNGSFEHLER"
            #return f">>{self.func.__name__}({self.argumente_an_stelle})>>"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):        # geht nur wenn schon ZHK-Struktur erstellt ist. Bitte sonst nicht aufrufen
        if self.__class__==other.__class__:     # auch ein Übergang?
            if self.func==other.func:           # gleiche Funktionsart?
                for i in range(len(self.argumente_an_stelle)):          # alle Argumente gleich?
                    if self.argumente_an_stelle[i]!=other.argumente_an_stelle[i]:
                        return False
                return True

        return False

### mögliche Übergänge werden gänzlich durch die definierten Funktionen determiniert. Können einfach generiert werden
übergänge = []
for func in definierte_funktionen:
    if func.argumentzahl==1:
        übergänge.append(   ((func(t1), t1)   ,   Übergang(func,[None]))   )

    elif func.argumentzahl==2:
        übergänge.append(   ((t1, (func(t1, t2))), Übergang(func, [None, t2]))   )
        übergänge.append(((t2, (func(t1, t2))), Übergang(func, [t1, None])))





### Generiere alle Elemente

def required_additional_space(o):
    if isinstance(o,Variable):
        return 0
    elif issubclass(o,Funktion):    # wirkt das nicht auch mit oberklassen????
        return o.argumentzahl
    else:
        raise ValueError()

def k_aus(set,k):
    if k==0:
        return [[]]

    hinten = k_aus(set,k-1)

    ergs = []
    for i in set:
        for h in hinten:
            ergs.append([i]+h)
    return ergs

def generate_alles(l=3,vars=[Variable("a"), Variable("b")]):
    #l = 3  -  das ist die maximale Funktionstiefe
    #vars - nur diese Variablen sollen in den Termen vorkommen
    einsetzbar = vars + definierte_funktionen

    alles = set()

    # Grundfall wo nur Variablen und 0-argument-Funktionen zugefügt werden
    for m in einsetzbar:
        if required_additional_space(m)==0:
            if isinstance(m,Variable):
                alles.add(m)
            elif issubclass(m,Funktion):
                alles.add(m())


    # rekursiver aufbau in höhere Funktionstiefen
    for i in range(1,l):
        ebene = set()
        for m in definierte_funktionen:         # Nur Funktionen durchgehen mit mindestens einem Argument
            if m.argumentzahl>=1:
                al = k_aus(alles,m.argumentzahl)
                for tu in al:                       # alle möglichen Kombinationen passender Länge
                    ebene.add(m(*tu))             # neues Objekt zu ergebnissen dazu
        alles=alles.union(ebene)

    return list(alles)  # vorher mit Set gearbeitet, um doppelte zu vermeiden. Ab jetzt mit array, als zuordnung von nr zu obj



### versuche für alle die Gleichheit oder den Übergang zu machen

def hat_struktur(term,modell)->"boolean, dict mit Belegung":
    # prüft und gibt zurück, was für die vorkommenden t1, t2... Variablen eingesetzt werden muss

    # base case dass man einfach den Rest als Inhalt der Strukturvar nimmt
    if modell.__class__==StrukturVariable:
        return True, {modell.name: term}

    # Es ist eine Funktion und deshalb wird in tiefere Ebenen geguckt
    if modell.__class__==term.__class__:    # auf oberstem Level gleiche Funktionsart
        argumentzahl = modell.__class__.argumentzahl

        gesamt_ob = True
        gesamt_wie = {}
        for i in range(argumentzahl):
            ob, wie = hat_struktur(term.terme[i],modell.terme[i])
            gesamt_ob = gesamt_ob and ob
            for k in gesamt_wie.keys():
                if k in wie.keys():
                    if not gesamt_wie[k]==wie[k]:   # Terme überschreiben __eq__  wodurch das sinnvoll geht
                        # gleicher Term muss unterschiedlich belegt werden -> geht nicht
                        return False,{}
            gesamt_wie = {**gesamt_wie, **wie}
        return gesamt_ob, gesamt_wie

    return False,{}

def möglich_mit_axiom(termtupel, axiom):
    """
    Testet, ob man durch einfache Anwendung von diesem Axiom (oben im Strukturbaum) zwei Terme ineinander umwandeln kann
    Ist Symmetrisch.
    (auch für Übergänge nutzbar)

    :param termtupel:
    :param axiom:
    :return: Boolean
    """

    # Axiom von einem zum anderen nutzen
    o1,w1 = hat_struktur(termtupel[0],axiom[0])
    o2, w2 = hat_struktur(termtupel[1],axiom[1])
    if o1 and o2:
        if dict_verträglich(w1,w2):
            return True, {**w1,**w2}

    # Axiom von anderem zum einen nutzen
    o1, w1 = hat_struktur(termtupel[0], axiom[1])
    o2, w2 = hat_struktur(termtupel[1], axiom[0])
    if o1 and o2:
        if dict_verträglich(w1, w2):
            return True, {**w1,**w2}

    return False, {}

def richtung_möglich_mit_axiom(termtupel, axiom):
    # wie 'möglich_mit_axiom'  nur nicht sofort beidseitig
    o1, w1 = hat_struktur(termtupel[0], axiom[0])
    o2, w2 = hat_struktur(termtupel[1], axiom[1])
    if o1 and o2:
        if dict_verträglich(w1, w2):
            return True, {**w1, **w2}
    return False, {}

def phi(r1,r2):     # Phi berechnet für beliebige zwei Terme, ob sie sich durch anwendung eines einzigen Axioms (ganz oben im Baum) ineinander umwandeln lassen
    if r1==r2:  # soll reflexiv sein. Sozusagen durch leeres Axiom umwandelbar
        #print("Warnung: Phi von zwei mal dem gleichen berechnet. Wurde als True evaluirt")
        return True, None, None

    for axiom in axiome:
        ob, wie = möglich_mit_axiom((r1,r2),axiom)
        if ob:
            return True, wie, axiom
    return False, None, None

def tau(r1,r2):
    """
    Prüft ob das eine mit einfacher abänderung in das andere Umwandelbar ist
    NICHT SYMMETRISCH
    Gibt zurück ob möglich und was auf den Übergangspfeil muss
    """

    for regel,pfeil in übergänge:
        #print(pfeil)
        ob, wie = richtung_möglich_mit_axiom((r1,r2),regel)
        if ob:
            return True, pfeil.einsetzen(wie,Obj_zu_KnotenNr[r1],Obj_zu_KnotenNr[r2])#wie[pfeil.name]
    return False, None


### ZHKs finden und Graph generieren


alles = generate_alles(l=3,vars=[Variable("a")])



V = len(alles)

KnotenNr_zu_Obj = alles                                              # nr eines Punktes -> Term
Obj_zu_KnotenNr = {alles[i]:i for i in range(len(alles))}            # Term O  -> int nr des Punktes
KnotenNr_ZHKnr=[i for i in range(V)]                                # int Punkt  -> int ZHK-nr
ZHKnr_zu_KnotenNrList=[set([i]) for i in range(V)]                         # int ZHK-nr -> int[] Punktliste

# Adj die Interreasoning-Kanten zwischen ZHKs speichert
#inter_in = [[] for i in range(V)]       # jeder eintrag (übergangsinfo, nach)
inter_out = [[] for i in range(V)]      # jeder eintrag (übergangsinfo, von)

beweisAdj =  [[] for i in range(V)]     # enthält (Nach, Beweisschritt)


class Beweisschritt():
    pass

class Gleich_Beweisschritt(Beweisschritt):
    def __init__(self, termNr, axiom, belegung):
        self.termNr = termNr
        self.axiom = axiom
        self.belegung = belegung

    def __str__(self):
        s= f" {KnotenNr_zu_Obj[self.termNr[0]]} = {KnotenNr_zu_Obj[self.termNr[1]]}  ~  {self.axiom[0]} = {self.axiom[1]}  |  "
        for k,v in self.belegung.items():
            s+=f"{k}:={v}  "
        return s
    def __repr__(self):
        return self.__str__()

class Induzierter_Beweisschritt(Beweisschritt):
    def __init__(self, übergang, von1, von2):
        self.übergang = übergang
        self.vons = [von1, von2]
    def __str__(self):
        return f"{KnotenNr_zu_Obj[self.vons[0]]} = {KnotenNr_zu_Obj[self.vons[1]]}    und dann beide Seiten:   {self.übergang}"
    def __repr__(self):
        return self.__str__()



def merge(von,nach):
    zhk1, zhk2 = KnotenNr_ZHKnr[von], KnotenNr_ZHKnr[nach]  # sind nur die nummern der zhks!!

    if zhk1==zhk2:  # Nichts machen, falls schon in einer ZHK
        return

    #if len(zhk2)<len(zhk2):
    #    zhk1,zhk2=zhk2,zhk1             # Optimierung: kürzere in zhk1
   #     von,nach = nach,von

    for i in ZHKnr_zu_KnotenNrList[zhk1]:
        KnotenNr_ZHKnr[i]=zhk2

    ZHKnr_zu_KnotenNrList[zhk2]=ZHKnr_zu_KnotenNrList[zhk2].union(ZHKnr_zu_KnotenNrList[zhk1])
    ZHKnr_zu_KnotenNrList[zhk1]=set()

    # muss noch machen, dass die Interkanten zwischen den weggemacht werden


    # verhindern, dass es InterKanten von der zukünftigen ZHK zu sich selbst gibt. Actually egal, da redundante Kanten eliminiert werden. Dann gibt es pro ZHK höchstens eine reziproke
    #for richtung in [inter_in,inter_out]:
    #    for vona in [(zhk1,zhk2),(zhk2,zhk1)]:
    #        von, nach = vona
    #        for i in range(len(richtung[von])).__reversed__():      # TODO Warning, dieser Teil könnte buggy sein. (Ist es wirklich)
    #            print(richtung[von][i][1])
    #            if richtung[von][i][1]==nach:
    #                richtung.pop(i)


    #inter_in[zhk2]+=inter_in[zhk1]
    #inter_in[zhk1] = []

    inter_out[zhk2] += inter_out[zhk1]
    inter_out[zhk1] = []




for von in range(V):
    for nach in range(V):
        #print(PZ[von],PZ[nach])
        if not von == nach:         # nur wenn nicht einfach gleicher Knoten
            if not KnotenNr_ZHKnr[von] == KnotenNr_ZHKnr[nach]:   #falls nicht in gleicher ZHK
                ob_, wie, axiom = phi(alles[von],alles[nach])
                if ob_:
                    merge(von,nach)
                    beweisschritt = Gleich_Beweisschritt((von,nach),axiom,wie)      # In Beweisstruktur aufnehmen
                    beweisAdj[von].append((nach,beweisschritt))
                    beweisAdj[nach].append((von,beweisschritt))
                else:
                    # nur wenn nicht gerade gemergt
                    if KnotenNr_ZHKnr[von]!=KnotenNr_ZHKnr[nach]:
                        # nur wenn in verschiedenen ZHK (zur Zeit)
                        ob, übergang = tau(KnotenNr_zu_Obj[von], KnotenNr_zu_Obj[nach])
                        if ob:
                            inter_out[KnotenNr_ZHKnr[von]].append((übergang, nach))#KnotenNr_ZHKnr[nach]
                            #inter_in[KnotenNr_ZHKnr[nach]].append((übergang, von))#KnotenNr_ZHKnr[von]

                            # Ziel sollte nicht die nummer der jetzigen ZHK speichern, sondern lieber die nr des Zielknotens.
                            # Dann kann zu jeder Zeit geguckt werden in welche ZHK die Kante nun führt!

# Interkanten sind korrekt erstellt.




def etwas_anschaulich_zeigen():     # unwichtige hilfsmethode, die auch komplett behindert geschrieben ist
    print("+"*100)
    ergebnis_komponenten = [[] for i in range(V)]

    for i in range(V):
        #print(alles[i],PZ[i])
        ergebnis_komponenten[KnotenNr_ZHKnr[i]].append(alles[i])

    ergebnis_komponenten_nichtleer=[]
    for i in ergebnis_komponenten:
        if i!=[]:
            ergebnis_komponenten_nichtleer.append(i)

    for i in ergebnis_komponenten_nichtleer:
        pass#print(i)
    print("-"*100)
    for i in range(V):
        print(ergebnis_komponenten[i])
    print("-" * 100)
    for i in range(V):          # inter_out
        print(inter_out[i])
    #print("-" * 100)
    #for i in range(V):  # inter_in
    #    print(inter_in[i])

#etwas_anschaulich_zeigen()

### Interreasoning zum logischen Verschmelzen von ZHKs

def interreasoning():
    change = True

    # I   gleicher Ursprung, gleicher Übergang, verschiedenes Ziel??

    # Gilt nicht:  III gleiches Ziel, gleicher Übergang, verschiedener Ursprung?
    # Denn: a*0 = b*0 -> a=b  ist eine falsche Schlussfolgerung.

    while change:       # solange durchgehen, bis sich einen ganzen durchlauf lang nichts mehr geändert hat
        change=False

        for inter in [inter_out]:#, inter_in]: # Actually ist das Interreasoning mit inter_in falsch!!!    # reasoning nach vorn und nach hinten nacheinander
            for zhk in range(V):

                for i in range(len(inter[zhk])).__reversed__():           # eine Kante.  Reversed um auch beim durchgehen entfernen zu können
                    if len(inter[zhk]) == 0:    # billiger schutz vor problem
                        break
                    e1 = inter[zhk][i]
                    for j in range(i+1, len(inter[zhk])).__reversed__():        # andere Kante
                        #print(len(inter[zhk]))
                        if len(inter[zhk])==0:
                            break
                        e2 = inter[zhk][j]

                        if (e1[0]==e2[0]):                                          # Gleicher Übergang?    (verwendet __eq__ von 'Übergang')
                            if KnotenNr_ZHKnr[e1[1]]==KnotenNr_ZHKnr[e2[1]]:        # gleiches Ziel?
                                pass
                                #inter[zhk].pop(i) # eine redundant, also löschen # TODO gefährlich hier zu löschen?? Ja, hat sich gezeigt, dass es tatsächlich zu logikfehlern führt
                                #inter_in[KnotenNr_ZHKnr[e1[1]]].pop()  # gleich auch bei ankommenden löschen?
                            else:
                                #print("GEFUNDEN",e1[1], e2[1])


                                merge(e1[1],e2[1])  # Klassen vereingen


                                überg1, überg2 = e1[0], e2[0]
                                print(überg1.nach)

                                beweisschritt = Induzierter_Beweisschritt(überg1,überg1.von,überg2.von)
                                beweisAdj[überg2.nach].append((überg1.nach, beweisschritt))
                                beweisAdj[überg1.nach].append((überg2.nach, beweisschritt))

                                change = True
interreasoning()
etwas_anschaulich_zeigen()


def beweisbar(r1,r2):
    # guckt ob bewiesen werden konnte, dass  r1 = r2
    ind1, ind2 = Obj_zu_KnotenNr[r1], Obj_zu_KnotenNr[r2]
    return KnotenNr_ZHKnr[ind1] == KnotenNr_ZHKnr[ind2]

def beweis_ausgeben(r1,r2,einschub=0):

    # BFS um Pfad zu finden
    von, nach = Obj_zu_KnotenNr[r1],Obj_zu_KnotenNr[r2]

    besucht = [False for i in range(V)]
    vorgänger = [None for i in range(V)]           # Pfad merken
    hingekommen_mit = [None for i in range(V)]     # beweisschritt merken

    besucht[von]=True

    Q=[von]

    while len(Q)!=0:
        current = Q.pop(0)

        for (nachbar,schritt) in beweisAdj[current]:
            if not besucht[nachbar]:
                besucht[nachbar]=True
                vorgänger[nachbar]=current
                hingekommen_mit[nachbar]=schritt
                Q.append(nachbar)

                if nachbar==nach:
                    Q=[]    # Abbrechen, weil Ziel gefunden

    # Pfad extrahieren
    pfad=[nach]

    while True:
        c = pfad[-1]
        if c==von:
            break
        else:
            pfad.append(vorgänger[c])

    # Ausgabe
    vorne =     " "*16*(einschub)
    print(f"{vorne}Beweis für:  {r1} = {r2}")
    #print(f"{vorne}{str(r1):<8}",end="")
    # Ausgabe der Beweisschritte
    dazu = f"{vorne}{str(r1):<8}"
    for k in pfad[0:-1].__reversed__():
        if hingekommen_mit[k].__class__== Gleich_Beweisschritt:
            print(f"{dazu+'= '+str(KnotenNr_zu_Obj[k]):<70}   | {hingekommen_mit[k]}")
        elif hingekommen_mit[k].__class__== Induzierter_Beweisschritt:
            print(f"{dazu+'= '+str(KnotenNr_zu_Obj[k]):<70}   | {hingekommen_mit[k]}")
            beweis_ausgeben(KnotenNr_zu_Obj[hingekommen_mit[k].vons[0]],KnotenNr_zu_Obj[hingekommen_mit[k].vons[1]], einschub=einschub+1)
        else:
            print("FEHLER")
        dazu = " "*8+vorne
    #print(vorne+"QED")


def beweis_ausgeben_wenn_beweisbar(r1,r2):
    if beweisbar(r1,r2):
        beweis_ausgeben(r1,r2)
    else:
        print("Nicht beweisbar")

if __name__ == '__main__':
    beweis_ausgeben_wenn_beweisbar(Und(a,a),a)