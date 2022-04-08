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

t1,t2,t3 = StrukturVariable("t1"),StrukturVariable("t2"),StrukturVariable("t3")
a,b,c = Variable("a"),Variable("b"),Variable("c")