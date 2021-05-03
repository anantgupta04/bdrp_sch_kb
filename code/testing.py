from owlready2 import *
import owlready2

owlready2.JAVA_EXE = 'C:/Program Files/Java/jre1.8.0_271/bin/java.exe'



# hontology = get_ontology('https://raw.githubusercontent.com/anantgupta04/bdrp_sch_kb/main/code/human.owl')
onto_path.append('D:/Uni/cs/bdrp/bdrp_sch_kb/code/')
pontology = get_ontology('https://raw.githubusercontent.com/anantgupta04/bdrp_sch_kb/main/code/person.owl')
hontology = get_ontology('https://raw.githubusercontent.com/anantgupta04/bdrp_sch_kb/main/code/human.owl').load()
pontology.imported_ontologies.append(hontology)
# with hontology:
#     class Human(Thing):
#         pass

with pontology:
    class Person(Thing):
        equivalent_to = [hontology.Human]


# humans = ['Sarah', 'Michael', 'John', 'Marie']

# for human in humans:
#     inst = hontology.Human(human)

# with hontology:
#     sync_reasoner()

# hontology.save('human.owl')


with pontology:
    sync_reasoner()

pontology.save('code/person.owl')