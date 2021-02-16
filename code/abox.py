import pandas as pd
import rdflib
from rdflib import Graph, URIRef, Literal, XSD, Namespace, RDF, OWL


class ABox_Generator():
	def __init__(self):
		self.graph = Graph()
		self.dblp_ns = Namespace('https://dblp.org/db/')
		self.dbpedia_ns = Namespace('http://dbpedia.org/ontology/')
		self.gkb_ns = Namespace('http://www.semanticweb.org/gkb#')
		self.rdfs_ns = Namespace("http://www.w3.org/2000/01/rdf-schema#")
		self.rdf_ns = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
		self.owl_ns = Namespace("http://www.w3.org/2002/07/owl#")

	def generate_formations_abox(self):
		import os
		print(os.getcwd())
		df = pd.read_csv('../data/mini_formations.csv')

		formations = df['unit'].unique()
		self.graph.add((URIRef(self.gkb_ns.Formation), RDF.type, OWL.Class))
		self.graph.add((URIRef(self.gkb_ns.Group), RDF.type, OWL.Class))
		for form in formations:

			form_uri = rdflib.URIRef(self.gkb_ns + form.replace(' ', '').strip().lower())
			self.graph.add((form_uri, self.rdf_ns.type, URIRef(self.gkb_ns.Formation)))
			# self.graph.add((form_uri, self.gkb_ns, URIRef))
			# self.graph.add((form_uri, self.owl_ns.disjointWith, self.gkb_ns.Wellbore))
			# self.graph.add((form_uri, self.owl_ns.disjointWith, self.gkb_ns.Group))

			form_df = df[df['unit']==form]

			for _, row in form_df.iterrows():

				group_uri = rdflib.URIRef(self.gkb_ns + str(row['parentunit']).replace(' ', '').strip().lower())

				self.graph.add((group_uri, self.rdf_ns.type, URIRef(self.gkb_ns.Group)))
				self.graph.add((form_uri, self.gkb_ns.belongs_to, group_uri))
				self.graph.add((form_uri, self.gkb_ns.located_in, Literal(row['country'])))

	def generate_wellbores_abox(self):

		df = pd.read_csv('../data/mini_wellbores.csv')

		wellbores = df['wellborename'].unique()
		self.graph.add((URIRef(self.gkb_ns.Wellbore), RDF.type, OWL.Class))
		for wellbore in wellbores:

			well_uri = rdflib.URIRef(self.gkb_ns + wellbore.replace(' ', '').strip().lower())
			self.graph.add((well_uri, self.rdf_ns.type, URIRef(self.gkb_ns.Wellbore)))

			well_df = df[df['wellborename'] == wellbore]

			for _, row in well_df.iterrows():

				form_uri = rdflib.URIRef(self.gkb_ns + str(row['formation']).replace(' ', '').strip().lower())
				self.graph.add((form_uri, self.rdf_ns.type, URIRef(self.gkb_ns.Formation)))
				self.graph.add((form_uri, self.gkb_ns.has_well, well_uri))
				self.graph.add((well_uri, self.gkb_ns.completed_in, Literal(row['completiondate'])))
				self.graph.add((well_uri, self.gkb_ns.top_depth, Literal(row['topdepth'])))
				self.graph.add((well_uri, self.gkb_ns.bottom_depth, Literal(row['bottomdepth'])))
				self.graph.add((well_uri, self.gkb_ns.core_length, Literal(row['corelength'])))


	def save(self):
		self.graph.serialize(destination='gkb_abox123.ttl', format='turtle')
		print('saved')


abox_gen = ABox_Generator()
abox_gen.generate_formations_abox()
abox_gen.generate_wellbores_abox()
abox_gen.save()
