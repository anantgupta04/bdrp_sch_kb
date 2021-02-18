from rdflib import Graph, Namespace, URIRef, RDF, OWL, Literal, RDFS
import pandas as pd
from utils import neatstr, capletter

class Ontology():

    def __init__(self):
        self.graph = Graph()
        self.gkb = Namespace('http://www.semanticweb.org/gkb#')
    
    def generate_TBox(self):
        
        self.graph.add((self.gkb.Unit, RDF.type, RDFS.Class))

        self.graph.add((self.gkb.located_in, RDF.type, RDF.Property))
        self.graph.add((self.gkb.located_in, RDFS.domain, self.gkb.Unit))
        self.graph.add((self.gkb.located_in, RDFS.range, RDFS.Literal))

        self.graph.add((self.gkb.has_age, RDF.type, RDF.Property))
        self.graph.add((self.gkb.has_age, RDFS.domain, self.gkb.Unit))
        self.graph.add((self.gkb.has_age, RDFS.range, RDFS.Literal))

        self.graph.add((self.gkb.has_lithology, RDF.type, RDF.Property))
        self.graph.add((self.gkb.has_lithology, RDFS.domain, self.gkb.Unit))
        self.graph.add((self.gkb.has_lithology, RDFS.range, RDFS.Literal))

        self.graph.add((self.gkb.Group, RDFS.subClassOf, self.gkb.Unit))
        self.graph.add((self.gkb.Formation, RDFS.subClassOf, self.gkb.Unit))
        self.graph.add((self.gkb.Wellbore, RDFS.subClassOf, self.gkb.Unit))
        self.graph.add((self.gkb.Member, RDFS.subClassOf, self.gkb.Unit))
        self.graph.add((self.gkb.Core, RDFS.subClassOf, self.gkb.Wellbore))

        self.graph.add((self.gkb.is_in, RDF.type, RDF.Property))

    def generate_ABox(self):
        
        df = pd.read_csv('../data/lithostrat_units.csv')
        groups = df[df['level'] =='GROUP']
        formations = df[df['level'] =='FORMATION']
        members = df[df['level'] =='MEMBER']

        for _, row in groups.iterrows():
            group_uri = URIRef(self.gkb.Group + '/' + neatstr(row['unit']))
            self.graph.add((group_uri, RDF.type, self.gkb.Group))
            self.graph.add((group_uri, RDFS.label, Literal(row['unit'].strip())))
            self.graph.add((group_uri, self.gkb.has_lithology, Literal(row['lithology'])))
            self.graph.add((group_uri, self.gkb.has_age, Literal(row['age'])))

        for _, row in formations.iterrows():
            formation_uri = URIRef(self.gkb.Formation + '/' + neatstr(row['unit']))
            self.graph.add((formation_uri, RDF.type, self.gkb.Formation))
            self.graph.add((formation_uri, RDFS.label, Literal(row['unit'].strip())))
            self.graph.add((formation_uri, self.gkb.has_lithology, Literal(row['lithology'])))
            self.graph.add((formation_uri, self.gkb.has_age, Literal(row['age'])))

            if row['parent']:
                parent_uri = getattr(self.gkb, capletter(row['level'])) + '/' + neatstr(str(row['parent']))
                self.graph.add((formation_uri, self.gkb.is_in, parent_uri))
        
        for _, row in members.iterrows():
            member_uri = URIRef(self.gkb.Member + '/' + neatstr(row['unit']))
            self.graph.add((member_uri, RDF.type, self.gkb.Member))
            self.graph.add((member_uri, RDFS.label, Literal(row['unit'].strip())))
            self.graph.add((member_uri, self.gkb.has_lithology, Literal(row['lithology'])))
            self.graph.add((member_uri, self.gkb.has_age, Literal(row['age'])))
            
            if row['parent']:
                parent_uri = getattr(self.gkb, capletter(row['level'])) + '/' + neatstr(row['parent'])
                self.graph.add((member_uri, self.gkb.is_in, parent_uri))



    def from_source(self, file):

        df = pd.read_csv(file, index_col=0)
        classname = file.split('/')[-1].split('.')[0]
        class_uri = getattr(self.gkb, classname)
        instance = df.columns[0]
        properties = df.columns[1:]

        self.graph.add((class_uri, RDF.type, OWL.Class))
        for _, row in df.iterrows():
            instance_uri = URIRef(class_uri + '/' + neatstr(str(row[instance])))
            self.graph.add((instance_uri, RDF.type, class_uri))
            for ppty in properties:
                self.graph.add((instance_uri, getattr(self.gkb, neatstr(str(ppty))), Literal(row[ppty])))


    def new_source(self, file):
        df = pd.read_csv(file, index_col=0)
        classname = file.split('/')[-1].split('.')[0]
        class_uri = getattr(self.gkb, classname)
        instance = df.columns[0]
        properties = df.columns[1:]

        self.graph.parse('test.ttl', format='turtle')
        classes = self.graph.subjects(predicate=RDF.type, object=OWL.Class)
        for c in classes:
            print(c)


    def save(self):
	    self.graph.serialize(destination='test.ttl', format='turtle')


g = Ontology()
# g.from_source('../data/mini_formations.csv')
# g.new_source('../data/mini_formations.csv')
g.generate_TBox()
g.generate_ABox()

g.save()