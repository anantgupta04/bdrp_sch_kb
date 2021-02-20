from rdflib import Graph, Namespace, URIRef, RDF, RDFS, OWL, Literal
import numpy as np
import pandas as pd
from utils import *

class Ontology():

    def __init__(self):
        self.graph = Graph()
        self.gkb = Namespace('http://www.semanticweb.org/gkb#')
    
    def generate_TBox(self):
        
        # Classes
        self.graph.add((self.gkb.Unit, RDF.type, RDFS.Class))
        self.graph.add((self.gkb.Wellbore, RDF.type, RDFS.Class))
        
        # Unit properties
        self.graph.add((self.gkb.located_in, RDF.type, RDF.Property))
        self.graph.add((self.gkb.located_in, RDFS.domain, self.gkb.Unit))
        self.graph.add((self.gkb.located_in, RDFS.range, RDFS.Literal))

        self.graph.add((self.gkb.age, RDF.type, RDF.Property))
        self.graph.add((self.gkb.age, RDFS.domain, self.gkb.Unit))
        self.graph.add((self.gkb.age, RDFS.range, RDFS.Literal))

        self.graph.add((self.gkb.lithology, RDF.type, RDF.Property))
        self.graph.add((self.gkb.lithology, RDFS.domain, self.gkb.Unit))
        self.graph.add((self.gkb.lithology, RDFS.range, RDFS.Literal))
        self.graph.add((self.gkb.is_in, RDF.type, RDF.Property))

        # Unit subclasses
        self.graph.add((self.gkb.Group, RDFS.subClassOf, self.gkb.Unit))
        self.graph.add((self.gkb.Formation, RDFS.subClassOf, self.gkb.Unit))
        # self.graph.add((self.gkb.Wellbore, RDFS.subClassOf, self.gkb.Unit))
        self.graph.add((self.gkb.Member, RDFS.subClassOf, self.gkb.Unit))
        self.graph.add((self.gkb.Core, RDFS.subClassOf, self.gkb.Wellbore))

        # Wellbore properties
        self.graph.add((self.gkb.has_unit, RDF.type, RDF.Property))
        self.graph.add((self.gkb.has_unit, RDFS.domain, self.gkb.Wellbore))
        self.graph.add((self.gkb.has_unit, RDFS.range, self.gkb.Unit))

        self.graph.add((self.gkb.topdepth, RDF.type, RDF.Property))
        self.graph.add((self.gkb.topdepth, RDFS.domain, self.gkb.Wellbore))
        self.graph.add((self.gkb.topdepth, RDFS.range, RDFS.Literal))

        self.graph.add((self.gkb.bottomdepth, RDF.type, RDF.Property))
        self.graph.add((self.gkb.bottomdepth, RDFS.domain, self.gkb.Wellbore))
        self.graph.add((self.gkb.bottomdepth, RDFS.range, RDFS.Literal))

        self.graph.add((self.gkb.completion_date, RDF.type, RDF.Property))
        self.graph.add((self.gkb.completion_date, RDFS.domain, self.gkb.Wellbore))
        self.graph.add((self.gkb.completion_date, RDFS.range, RDFS.Literal))

        # Core properties
        self.graph.add((self.gkb.core_length, RDF.type, RDF.Property))
        self.graph.add((self.gkb.core_length, RDFS.domain, self.gkb.Core))
        self.graph.add((self.gkb.core_length, RDFS.range, RDFS.Literal))


    def load_units(self):
        
        df = pd.read_csv('../data/lithostrat_units.csv')
        groups = df[df['level'] =='GROUP']
        formations = df[df['level'] =='FORMATION']
        members = df[df['level'] =='MEMBER']

        for _, row in groups.iterrows():
            group_uri = URIRef(self.gkb.Group + '/' + neatstr(row['unit']))
            self.graph.add((group_uri, RDF.type, self.gkb.Group))
            self.graph.add((group_uri, RDFS.label, Literal(row['unit'].strip())))
            self.graph.add((group_uri, self.gkb.lithology, Literal(row['lithology'])))
            self.graph.add((group_uri, self.gkb.age, Literal(row['age'])))

        for _, row in formations.iterrows():
            formation_uri = URIRef(self.gkb.Formation + '/' + neatstr(row['unit']))
            self.graph.add((formation_uri, RDF.type, self.gkb.Formation))
            self.graph.add((formation_uri, RDFS.label, Literal(row['unit'].strip())))
            self.graph.add((formation_uri, self.gkb.lithology, Literal(row['lithology'])))
            self.graph.add((formation_uri, self.gkb.age, Literal(row['age'])))

            if row['parent']:
                parent_uri = getattr(self.gkb, capletter(row['level'])) + '/' + neatstr(str(row['parent']))
                self.graph.add((formation_uri, self.gkb.is_in, parent_uri))
        
        for _, row in members.iterrows():
            member_uri = URIRef(self.gkb.Member + '/' + neatstr(row['unit']))
            self.graph.add((member_uri, RDF.type, self.gkb.Member))
            self.graph.add((member_uri, RDFS.label, Literal(row['unit'].strip())))
            self.graph.add((member_uri, self.gkb.lithology, Literal(row['lithology'])))
            self.graph.add((member_uri, self.gkb.age, Literal(row['age'])))
            
            if row['parent']:
                parent_uri = getattr(self.gkb, capletter(row['level'])) + '/' + neatstr(row['parent'])
                self.graph.add((member_uri, self.gkb.is_in, parent_uri))


    def load_wellbores(self):

        df = pd.read_csv('../data/litho_wellbore_unique.csv')

        for _, row in df.iterrows():
            core_uri = URIRef(self.gkb.Core + '/' + neatstr(str(row['wellbore_name'])))
            wellbore_uri = URIRef(self.gkb.Wellbore + '/' + neatstr(str(row['wellbore_name'])))
            try:
                next(self.graph.triples((core_uri, RDF.type, self.gkb.Core)))
                is_core = True
            except StopIteration:
                is_core = False

            if is_core:
                self.graph.add((core_uri, self.gkb.topdepth, Literal(row['topdepth'])))
                self.graph.add((core_uri, self.gkb.bottomdepth, Literal(row['bottomdepth'])))
            else:
                unit_uri = getattr(self.gkb, capletter(row['unit_level'])) + '/' + neatstr(str(row['unit_name']))
                self.graph.add((wellbore_uri, RDF.type, self.gkb.Wellbore))
                self.graph.add((wellbore_uri, RDFS.label, Literal(row['wellbore_name'].strip())))
                self.graph.add((wellbore_uri, self.gkb.has_unit, unit_uri))
                self.graph.add((wellbore_uri, self.gkb.completion_date, Literal(row['completion_date'])))
    

    def load_cores(self):
        
        df = pd.read_csv('../data/core_unique.csv')

        for _, row in df.iterrows():
            core_uri = URIRef(self.gkb.Core + '/' + neatstr(str(row['wellbore_name'])))
            unit_uri = getattr(self.gkb, capletter(row['unit_level'])) + '/' + neatstr(str(row['unit_name']))
            self.graph.add((core_uri, RDF.type, self.gkb.Core))
            self.graph.add((core_uri, RDFS.label, Literal(row['wellbore_name'].strip())))
            if row['core_length'] != 0:
                self.graph.add((core_uri, self.gkb.core_length, Literal(row['core_length'])))
            self.graph.add((core_uri, self.gkb.has_unit, unit_uri))
            self.graph.add((core_uri, self.gkb.completion_date, Literal(row['completion_date'])))


    def generate_ABox(self):

        self.load_units()
        self.load_cores()
        self.load_wellbores()
        




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
        class_idx = maincol(classname, df.columns)
        class_col = df.columns[class_idx]
        ppty_cols = df.columns[:class_idx] + df.columns[class_idx+1:]

        self.graph.parse('test.ttl', format='turtle')
        ont_classes = self.graph.subjects(predicate=RDF.type, object=RDFS.Class)
        ont_properties = self.graph.subjects(predicate=RDF.type, object=RDF.Property)

        # ont_class = np.argmax([word_compare(c, class_col) for c in ont_classes])
        for ppty in ont_properties:

        # if ont_class:
            # class_uri = getattr(self.gkb, ont_class)
        # else:
            # class_uri = getattr(self.gkb, classname)
        
        


    def save(self):
        self.graph.serialize(destination='test.ttl', format='turtle')


g = Ontology()
# g.from_source('../data/mini_formations.csv')
# g.new_source('../data/mini_formations.csv')
g.generate_TBox()
g.generate_ABox()

g.save()

