# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 13:28:33 2020

@author: anant
"""

import os
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs


BASE_URL = "http://nhm2.uio.no/norges/litho/form_tops.php?form_name=NORDLAND"
PATH = "C:\\Users\\akhilg\\Documents\\CollegeDocuments\\BDMA\\CentralSuperlec\\Coursework\\BDRP\\week 2"


def norlex():
    page = requests.get(BASE_URL)
    data = []
    if not page.status_code == 200:
            print("Some error occurred loading the page. Status code: " + str(page.status_code))
    else:
        print("\nThe scrapper for product information has been invoked.\n")
        soup = bs(page.text, "lxml")

        """
        soup.find("body").find("table",{"cellpadding":"10"})
            .find("table", {"border":"1"}).findAll("tr")
        """
        table = soup.find("body").find("table", {"border":"1"}).findAll("tr")
        for idx,i in enumerate(table):
            if idx < 2:
                continue

            values = i.text.split('\n')
            data.append([values[0], float(values[1])])

        df = pd.DataFrame(data=data, columns=["Well", "Depth"])

        df.to_csv(PATH + "\\Norlex.csv")
        print(f"Congratulations the file has been created at {PATH}.")

if __name__ == '__main__':
    norlex()