# -*- coding: utf-8 -*-


# import libraries here
# from standardized import *
import nltk

from nltk.corpus import stopwords
import rdflib

BASE_URI = "<http://www.semanticweb.org/gkb#"

g = rdflib.Graph()
g.load("test.ttl", format="turtle")

formations = set([])
for row in g.query(
            'select ?f where {?s a ns1:Formation; rdfs:label ?f}'
        ):
    formations = formations.union([str(row.f).title()])
# print("Formations are \n",formations)

wells = set([])
for row in g.query(
            'select ?w where {?s a ns1:Core; rdfs:label ?w}'
        ):
    wells = wells.union([str(row.w).title()])
# print("Well Cores are \n", wells)

groups = set([])
for row in g.query(
        'select ?g where {?s a ns1:Group; rdfs:label ?g.}'
        ):
    groups = groups.union([str(row.g).title()])
# print("The groups collected are\n", groups)


def getNer(query):
    import pdb;pdb.set_trace()
    final_query = ""
    og_query = query
    stop_words = set(stopwords.words('english'))
    try:
        query = nltk.word_tokenize(query.lower())
    except:
        nltk.download('stopwords')
        nltk.download('punkt')
        # nltk.download('averaged_perceptron_tagger')
        query = nltk.word_tokenize(query.lower())

    query = [w for w in query if not w in stop_words]


    # query = nltk.pos_tag(query)
    print("inside getNEr = ", query)

    if "formation" in query:
        print("formation is located")
        # check whether we currrently contain the instance
        subject = query[query.index("formation")-1]
        label = subject + " fm"
        if formations.intersection([label.title()]):
            formation_sub = BASE_URI + f"Formation/{subject}fm>"
            print(f"formation subject is = {formation_sub}")
    if "well" in query:
        # check whether current instance is found
        wid = query.index("well")
        well_choice1 = og_query[wid-1]
        well_choice2 = og_query[wid+1]
        if wells.intersection([well_choice1]):
            well_subject = well_choice1
        elif wells.intersection([well_choice2]):
            well_subject = well_choice2
    else:
        if "group" in query:
            print("parent group query")
            final_query = "select ?g where { " + formation_sub + "ns1:is_in ?g.}"
            print(g.query(final_query))
        elif "members" in query:
            print("members of a particular formation")
        elif "period" in query or "age" in query:
            print("Age and period of formation")

    return query


'''
Questions that can be answered?

* Where is X formation?

* which well crosses X formation?

* Which group does X formation belong to?

* What are members of Ekofisk formation?

* What is lithology of Ekofisk formation?

* What is the top of X Formation for the well A?

* What is the period and age of X formation?

'''


if __name__=="__main__":
    nl_query = input("Enter the query: ")
    ner = getNer(nl_query.lower())
    print(ner)
    # final_query = "@prefix ns1: <http://www.semanticweb.org/gkb#> ."
    import pdb; pdb.set_trace()
    '''
    for i in ner:
        if "where" in nl_query:
            subject = ner[ner.index("formation")-1]
            subject = subject + " formation"
            # check whether we contain the certain formation or not
            if subject.title() in formations:
                # final_query = final_query + "select ?c " + "where {ns1:" + \
                 subject.replace(" ","").lower()  +" ns1:located_in ?c}"
                break
            #print("Location required via query = \n",final_query)

        elif "which" in nl_query:
            if "group" in ner and "formation" in ner:

                print("group-formation")
            if "well" in ner and "formation" in ner:
                print("well-formation")
    '''