# -*- coding: utf-8 -*-


# import libraries here
# from standardized import *
import nltk
from  tkinter import *
from nltk.corpus import stopwords
import rdflib


BASE_URI = "<http://www.semanticweb.org/gkb#"

g = rdflib.Graph()
g.load("initial.owl", format="turtle")

formations = set([])
for row in g.query(
            'select ?f where {?s a ns1:Formation; rdfs:label ?f}'
        ):
    formations = formations.union([str(row.f).title()])
# print("Formations are \n",formations)

wells = set([])
for row in g.query(
            'select ?w where {?s a ns1:Wellbore; rdfs:label ?w}'
        ):
    wells = wells.union([str(row.w).title()])
# print("Well Cores are \n", wells)

groups = set([])
for row in g.query(
        'select ?g where {?s a ns1:Group; rdfs:label ?g.}'
        ):
    groups = groups.union([str(row.g).title()])
# print("The groups collected are\n", groups)


def getNer():
    # print("Submitting form")
    # print(f"{namevalue.get()} ")
    query = namevalue.get()
    og_question = query
    final_query = None
    formation_sub = None
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
    # print("inside getNEr = ", query)

    if "formation" in query:
        print("formation is located")
        # check whether we currrently contain the instance
        subject = query[query.index("formation")-1]
        label = subject + " fm"
        if formations.intersection([label.title()]):
            formation_sub = BASE_URI + f"Formation/{subject}fm>"
            print(f"formation subject is = {formation_sub}")
        else:
            # add an instance
            print("Add to abox")
    # import pdb;pdb.set_trace()
    if "well" in query:
        # check whether current instance is found
        if "crosses" in query:
            print("Which wells cross a particular formation")
            final_query = "select ?ans where{ ?ws a ns1:Wellbore; rdfs:label ?ans; \
                        ns1:has_unit " + formation_sub + "}"
        else:
            wid = query.index("well")
            well_choice1 = query[wid-1]
            well_choice2 = query[wid+1]
            if wells.intersection([well_choice1]):
                well_subject = well_choice1
            elif wells.intersection([well_choice2]):
                well_subject = well_choice2
            well_ns = BASE_URI + f"Wellbore/{well_subject}>"
            # print("Well subject is ", well_ns)
            depth = "top"  if "top" in query else "bottom"
            final_query = "select ?ans where {" + well_ns + " a ns1:Wellbore;\
                            ns1:has_unit " + formation_sub + " ; ns1:" + \
                                depth+"depth ?ans.}"
    elif formation_sub:
        if "group" in query:
            final_query = "select ?ans where { " + formation_sub + \
                            "ns1:parent_unit ?g. \
                             ?g rdfs:label ?ans}"
        elif "members" in query:
            print("members of a particular formation")
            final_query = "select ?ans where { ?b ns1:parent_unit " + formation_sub + ";\n"\
                                            "a ns1:Member.\n ?b rdfs:label ?ans}"
        elif "age" in query:
            print("Age of formation")
            final_query = "select ?ans where { " + formation_sub + "ns1:age ?ans.}"
            # print([row.age for row in g.query(final_query)])
        elif "lithology" in query:
            print("Lithology of formation")
            final_query = "select ?ans where { " + formation_sub + "ns1:lithology ?ans.}"
        elif "where" in og_question:
            print("Location of formation")
            final_query = "select ?ans where { " + formation_sub + "ns1:located_in ?ans.}"
    if final_query:
        answers = [row.ans.title() for row in g.query(final_query)]
    else:
        getvals()
        answers = "Sorry, we cannot answer this question at the moment. \n" +\
            "System admins have been informed regarding the evolvement of the graph."

    print(f"The answer to the query\n{og_question} is \n {answers}")
    lbl_result["text"] = f"{answers}"


    # return query


'''
Questions that can be answered?

* Where is X formation? -- WORKS

* Which group does X formation belong to? --WORKS

* What are members of heimdal formation?

* What is lithology of Ekofisk formation? -- WORKS(NOT recommended)

* What is the age of X formation? -- WORKS

* what is the top depth for the well 2/1-15 in the ekofisk formation? -- WORKS
* what is the bottom depth for the well 2/1-15 in the ekofisk formation? -- WORKS

* which well crosses X formation? -- WORKS

'''




if __name__=="__main__":
    # Attempt 2
    root = Tk()

    def getvals():
        print("Submitting form")
        # print(f"{namevalue.get(), } ")



        with open("records.txt", "a") as f:
            f.write(f"{namevalue.get()}\n ")



    root.geometry("644x344")
    #Heading
    Label(root, text="Welcome to Schlumberger's Knowledge Center", font="comicsansms 13 bold", pady=15).grid(row=0, column=3)

    #Text for our form
    name = Label(root, text="Name")

    #Pack text for our form
    name.grid(row=1, column=2)

    # Tkinter variable for storing entries
    namevalue = StringVar()

    # Packing the Entries
    nameentry = Entry(root, textvariable=namevalue)

    #Button & packing it and assigning it a command
    btn_convert = Button(text="Submit your query", command=getNer)
    lbl_result = Label(master=root, text="Answers is")

    # grid assignment
    nameentry.grid(row=1, column=3)
    btn_convert.grid(row=7, column=3)
    lbl_result.grid(row=10,column=3, padx=10, pady=10)


    root.mainloop()