# -*- coding: utf-8 -*-


# import libraries here
# from standardized import *
import nltk
from  tkinter import *
from nltk.corpus import stopwords
import rdflib


BASE_URI = "<http://www.semanticweb.org/gkb#"

g = rdflib.Graph()
g.load("test.owl", format="turtle")

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


def getNer():
    # import pdb;pdb.set_trace()
    print("Submitting form")
    print(f"{namevalue.get()} ")
    query = namevalue.get()
    og_question = query
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
        else:
            # add an instance
            print("Add to abox")
    import pdb;pdb.set_trace()
    if "well" in query:
        # check whether current instance is found
        if "crosses" in query:
            print("Which wells cross a particular formation")
            final_query = "select ?ans where{ ?ws a ns:Wellbore; rdfs:label ?ans; \
                        ns1:has_unit " + formation_sub + "}"
        else:
            wid = query.index("well")
            well_choice1 = og_query[wid-1]
            well_choice2 = og_query[wid+1]
            if wells.intersection([well_choice1]):
                well_subject = well_choice1
            elif wells.intersection([well_choice2]):
                well_subject = well_choice2
            final_query = "select ? where { }"
    else:
        if "group" in query:
            # print("parent group query")
            final_query = "select ?ans where { " + formation_sub + \
                            "ns1:parent_unit ?g. \
                             ?g rdfs:label ?ans}"
        elif "members" in query:
            print("members of a particular formation")
            final_query = ""
        elif "age" in query:
            print("Age of formation")
            final_query = "select ?ans where { " + formation_sub + "ns1:age ?ans.}"
            # print([row.age for row in g.query(final_query)])
        elif "lithology" in query:
            print("Lithology of formation")
            final_query = "select ?ans where { " + formation_sub + "ns1:lithology ?ans.}"
    answers = [row.ans for row in g.query(final_query)]
    print(f"The answer to the query\n{og_question} is \n {answers}")
    return query


'''
Questions that can be answered?

* Where is X formation?

* which well crosses X formation?

* Which group does X formation belong to? --WORKS

* What are members of Ekofisk formation?

* What is lithology of Ekofisk formation?

* What is the top of X Formation for the well A?

* What is the period and age of X formation?

'''




if __name__=="__main__":
    # nl_query = input("Enter the query: ")

    # win = Tk()# Application Name
    # win.title("Python GUI App")# Label
    # lbl = Label(win, text = "Enter your question:").grid(column = 0, row = 0)# Click event
    # name = StringVar()

    # def click():
    #     print("Hi," + name.get())# Textbox widget

    # nameEntered = Entry(win, width = 12, textvariable = name).grid(column = 0, row = 1)# Button widget
    # button = Button(win, text = "submit", command = click).grid(column = 1, row = 1)
    # win.mainloop()


    # Attempt 2
    root = Tk()

    def getvals():
        print("Submitting form")
        print(f"{namevalue.get(), phonevalue.get(), gendervalue.get(), emergencyvalue.get(), paymentmodevalue.get()} ")



        with open("records.txt", "a") as f:
            f.write(f"{namevalue.get(), phonevalue.get(), gendervalue.get(), emergencyvalue.get(), paymentmodevalue.get()}\n ")



    root.geometry("644x344")
    #Heading
    Label(root, text="Welcome to Schlumberger's Knowledge Center", font="comicsansms 13 bold", pady=15).grid(row=0, column=3)

    #Text for our form
    name = Label(root, text="Name")
    # phone = Label(root, text="Phone")
    # gender = Label(root, text="Gender")
    # emergency = Label(root, text="Emergency Contact")
    # paymentmode = Label(root, text="Payment Mode")

    #Pack text for our form
    name.grid(row=1, column=2)
    # phone.grid(row=2, column=2)
    # gender.grid(row=3, column=2)
    # emergency.grid(row=4, column=2)
    # paymentmode.grid(row=5, column=2)

    # Tkinter variable for storing entries
    namevalue = StringVar()
    # phonevalue = StringVar()
    # gendervalue = StringVar()
    # emergencyvalue = StringVar()
    # paymentmodevalue = StringVar()
    # foodservicevalue = IntVar()


    #Entries for our form
    nameentry = Entry(root, textvariable=namevalue)
    # phoneentry = Entry(root, textvariable=phonevalue)
    # genderentry = Entry(root, textvariable=gendervalue)
    # emergencyentry = Entry(root, textvariable=emergencyvalue)
    # paymentmodeentry = Entry(root, textvariable=paymentmodevalue)

    # Packing the Entries
    nameentry.grid(row=1, column=3)
    # phoneentry.grid(row=2, column=3)
    # genderentry.grid(row=3, column=3)
    # emergencyentry.grid(row=4, column=3)
    # paymentmodeentry.grid(row=5, column=3)

    # #Checkbox & Packing it
    # foodservice = Checkbutton(text="Want to prebook your meals?", variable = foodservicevalue)
    # foodservice.grid(row=6, column=3)

    #Button & packing it and assigning it a command
    Button(text="Submit your query", command=getNer).grid(row=7, column=3)



    root.mainloop()


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