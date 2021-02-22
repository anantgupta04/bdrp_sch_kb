from rdflib import Graph, Namespace, URIRef, RDF, RDFS, OWL, Literal
import numpy as np
import pandas as pd
from utils import *
import owlready2

CURRENT_ONTOLOGY = 'initial.owl'
NEW_ONTOLOGY = 'evolved.owl'


class Ontology():

    def __init__(self):
        self.graph = Graph()
        self.gkb = Namespace('http://www.semanticweb.org/gkb#')
    
    def generate_TBox(self):
        
        # Classes
        self.graph.add((self.gkb.Unit, RDF.type, OWL.Class))
        self.graph.add((self.gkb.Wellbore, RDF.type, OWL.Class))
        
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
        self.graph.add((self.gkb.parent_unit, RDF.type, RDF.Property))

        # Unit subclasses
        self.graph.add((self.gkb.Group, RDFS.subClassOf, self.gkb.Unit))
        self.graph.add((self.gkb.Group, RDF.type, OWL.Class))
        self.graph.add((self.gkb.Formation, RDFS.subClassOf, self.gkb.Unit))
        self.graph.add((self.gkb.Formation, RDF.type, OWL.Class))
        self.graph.add((self.gkb.Member, RDFS.subClassOf, self.gkb.Unit))
        self.graph.add((self.gkb.Member, RDF.type, OWL.Class))
        
        # Wellbore subclasses
        self.graph.add((self.gkb.Core, RDFS.subClassOf, self.gkb.Wellbore))
        self.graph.add((self.gkb.Core, RDF.type, OWL.Class))
        
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

        df = pd.read_csv('../data/lithostrat_units.csv', header=0, nrows=100)
        df.dropna(inplace=True)
        groups = df[df['level'] =='GROUP']
        formations = df[df['level'] =='FORMATION']
        members = df[df['level'] =='MEMBER']

        for _, row in groups.iterrows():
            group_uri = self.gkb.Group + '/' + neatstr(row['unit'])
            self.graph.add((group_uri, RDF.type, self.gkb.Group))
            self.graph.add((group_uri, RDFS.label, Literal(row['unit'].strip())))
            self.graph.add((group_uri, self.gkb.lithology, Literal(row['lithology'])))
            self.graph.add((group_uri, self.gkb.age, Literal(row['age'])))

        for _, row in formations.iterrows():
            formation_uri = self.gkb.Formation + '/' + neatstr(row['unit'])
            self.graph.add((formation_uri, RDF.type, self.gkb.Formation))
            self.graph.add((formation_uri, RDFS.label, Literal(row['unit'].strip())))
            self.graph.add((formation_uri, self.gkb.lithology, Literal(row['lithology'])))
            self.graph.add((formation_uri, self.gkb.age, Literal(row['age'])))

            if row['parent']:
                parent_uri = getattr(self.gkb, row['level'].title()) + '/' + neatstr(str(row['parent']))
                self.graph.add((parent_uri, RDF.type, getattr(self.gkb, row['level'].title())))
                self.graph.add((parent_uri, RDFS.label, Literal(row['parent'])))
                self.graph.add((formation_uri, self.gkb.parent_unit, parent_uri))
        
        for _, row in members.iterrows():
            member_uri = self.gkb.Member + '/' + neatstr(row['unit'])
            self.graph.add((member_uri, RDF.type, self.gkb.Member))
            self.graph.add((member_uri, RDFS.label, Literal(row['unit'].strip())))
            self.graph.add((member_uri, self.gkb.lithology, Literal(row['lithology'])))
            self.graph.add((member_uri, self.gkb.age, Literal(row['age'])))
            
            if row['parent']:
                parent_uri = getattr(self.gkb, row['level'].title()) + '/' + neatstr(row['parent'])
                self.graph.add((parent_uri, RDF.type, getattr(self.gkb, row['level'].title())))
                self.graph.add((parent_uri, RDFS.label, Literal(row['parent'])))
                self.graph.add((member_uri, self.gkb.parent_unit, parent_uri))


    def load_wellbores(self):

        df = pd.read_csv('../data/litho_wellbore_unique.csv', header=0, nrows=100)
        df.dropna(inplace=True)

        for _, row in df.iterrows():
            core_uri = self.gkb.Core + '/' + neatstr(str(row['wellbore_name']))
            wellbore_uri = self.gkb.Wellbore + '/' + neatstr(str(row['wellbore_name']))

            if list(self.graph.triples((core_uri, RDF.type, self.gkb.Core))):
                self.graph.add((core_uri, self.gkb.topdepth, Literal(row['topdepth'])))
                self.graph.add((core_uri, self.gkb.bottomdepth, Literal(row['bottomdepth'])))
            else:
                unit_uri = getattr(self.gkb, row['unit_level'].title()) + '/' + neatstr(str(row['unit_name']))
                self.graph.add((wellbore_uri, RDF.type, self.gkb.Wellbore))
                self.graph.add((wellbore_uri, RDFS.label, Literal(row['wellbore_name'].strip())))
                self.graph.add((unit_uri, RDF.type, getattr(self.gkb, row['unit_level'].title())))
                self.graph.add((unit_uri, RDFS.label, Literal(row['unit_name'])))
                self.graph.add((wellbore_uri, self.gkb.has_unit, unit_uri))
                self.graph.add((wellbore_uri, self.gkb.completion_date, Literal(row['completion_date'])))
                self.graph.add((wellbore_uri, self.gkb.topdepth, Literal(row['topdepth'])))
                self.graph.add((wellbore_uri, self.gkb.bottomdepth, Literal(row['bottomdepth'])))
    

    def load_cores(self):
        
        df = pd.read_csv('../data/core_unique.csv', header=0, nrows=100)
        df.dropna(inplace=True)
        for _, row in df.iterrows():
            core_uri = self.gkb.Core + '/' + neatstr(str(row['wellbore_name']))
            unit_uri = getattr(self.gkb, row['unit_level'].title()) + '/' + neatstr(str(row['unit_name']))

            self.graph.add((core_uri, RDF.type, self.gkb.Core))
            self.graph.add((core_uri, RDFS.label, Literal(row['wellbore_name'].strip())))
            if row['core_length'] != 0:
                self.graph.add((core_uri, self.gkb.core_length, Literal(row['core_length'])))
            
            self.graph.add((unit_uri, RDF.type, getattr(self.gkb, row['unit_level'].title())))
            self.graph.add((unit_uri, RDFS.label, Literal(row['unit_name'])))
            self.graph.add((core_uri, self.gkb.has_unit, unit_uri))
            self.graph.add((core_uri, self.gkb.completion_date, Literal(row['completion_date'])))


    def generate_ABox(self):

        self.load_units()
        self.load_cores()
        self.load_wellbores()
        


    def new_source(self, file):

        class_uri = ''  # source means class
        df = pd.read_csv(file, header=0, nrows=100)
        df.dropna(inplace=True)
        classname = file.split('/')[-1].split('.')[0]
        # col with names of class instances
        class_idx = maincol(classname, df.columns[:2])
        class_col = df.columns[class_idx]
        ppty_cols = list(df.columns[:class_idx]) + list(df.columns[class_idx+1:])

        # reading the current graph
        # self.graph.parse(CURRENT_ONTOLOGY, format='turtle')
        ont_classes = self.get_classes()
        print(f'existing classes: {ont_classes}')
        ont_properties = self.get_properties()

        # get the closest existing class name
        ont_class = closest(classname, ont_classes)
        
        if ont_class:
            class_uri = getattr(self.gkb, ont_class)
            print(f'{classname} is similar to class {ont_class}')
        else:
            # create new class
            class_uri = getattr(self.gkb, classname.title())
            self.graph.add((class_uri, RDF.type, OWL.Class))


        col_ppty_dict = {}  # to keep col -> ppty_uri
        col_class = {}      # cols that contain classes: col -> class uri
        col_literal = []    # cols that contain literals
        for col in ppty_cols:
            ppty_uri = ''
            # get the closest existing property name
            ont_property = closest(col, ont_properties)
            print(f'{col} is similar to property {ont_property}')
            if ont_property:
                ppty_uri = getattr(self.gkb, ont_property)
            else:
                # create a new property
                ppty_uri = getattr(self.gkb, neatstr(col, space='_'))
                self.graph.add((ppty_uri, RDF.type, RDF.Property))
                self.graph.add((ppty_uri, RDFS.domain, class_uri))
                # col contains classes or literals
                range_type = closest(col, ont_classes)
                print(f'range_type of {col} is {range_type}')
                unique_rate = len(df[col].unique()) / len(df)
                if range_type:
                    # if classes
                    matched_class_uri = getattr(self.gkb, range_type)
                    existing_ppty = list(self.graph.predicates(class_uri, matched_class_uri))
                    ppty_uri = existing_ppty[0] if existing_ppty else ppty_uri
                    self.graph.add((ppty_uri, RDFS.range, matched_class_uri))
                    col_class[col] = matched_class_uri
                elif unique_rate < 0.1:
                    new_class_uri = getattr(self.gkb, col.title())
                    self.graph.add((new_class_uri, RDF.type, OWL.Class))
                    self.graph.add((ppty_uri, RDFS.range, new_class_uri))
                    col_class[col] = new_class_uri
                else:
                    # if literals   
                    self.graph.add((ppty_uri, RDFS.range, RDFS.Literal))
                    col_literal.append(col)

            # col -> corresponding uri
            col_ppty_dict[col] = ppty_uri

        for _, row in df.iterrows():
            instance_uri = class_uri + '/' + neatstr(str(row[class_col]))
            main_triple = (instance_uri, RDF.type, class_uri)
            if not list(self.graph.triples(main_triple)):
                self.graph.add((instance_uri, RDF.type, class_uri))
                self.graph.add((instance_uri, RDFS.label, Literal(row[class_col].strip())))
            for col in col_literal:
                lit_triple = (instance_uri, col_ppty_dict[col], Literal(row[col]))
                if not list(self.graph.triples(lit_triple)):
                    self.graph.add(lit_triple)
            for col, col_type in col_class.items():
                
                col_instance_uri = col_type + '/' + neatstr(str(row[col]))
                cls_triple = (instance_uri, col_ppty_dict[col], col_instance_uri)

                if not list(self.graph.triples(cls_triple)):
                    self.graph.add((col_instance_uri, RDF.type, col_type))
                    self.graph.add((col_instance_uri, RDFS.label, Literal(row[col])))
                    self.graph.add(cls_triple)
        



    def get_classes(self):
        class_uris = self.graph.subjects(predicate=RDF.type, object=OWL.Class)
        classes = [c.split(self.gkb)[1] for c in class_uris]
        return classes
    
    def get_properties(self):
        ppty_uris = self.graph.subjects(predicate=RDF.type, object=RDF.Property)
        properties = [ppty.split(self.gkb)[1] for ppty in ppty_uris]
        return properties
    
    def save(self):
        self.graph.serialize(destination=NEW_ONTOLOGY, format='turtle')
    
    def sync_save(self):
        
        onto = owlready2.get_ontology("file://D:/Uni/cs/courses/bdrp/bdrp_sch_kb/code/test1.owl").load()
        owlready2.sync_reasoner_pellet()
        onto.save("test1.owl", format='rdfxml')


g = Ontology()
# g.generate_TBox()
# g.generate_ABox()
# g.save()
g.graph.parse(CURRENT_ONTOLOGY, format='turtle')
g.new_source('../test_data/field.csv')
# g.save()
g.new_source('../test_data/discovery.csv')
# g.save()
g.new_source('../test_data/wellbore_exploration_all.csv')
# g.save()
g.new_source('../test_data/field_description.csv')
# g.save()
g.new_source('../test_data/discovery_description.csv')
g.save()