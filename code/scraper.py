from bs4 import BeautifulSoup
import requests 
import re
from collections import defaultdict
import numpy as np
import pandas as pd
import os

formations_root = 'https://factpages.npd.no/en/strat/pageview/litho/formations/'

def download_formation_pages(soup):
    # links to all of the formation pages
    a_tags = soup.find_all('a', id=re.compile('tvCarrierst\d'))

    # fm means formation
    for a in a_tags:
        fm_name = a.text 
        fm_link_ = a.get('href')  # link to the middle page

        # contains formation info in iframe
        fm_page_ = requests.get(fm_link_, allow_redirects=True)

        soup = BeautifulSoup(fm_page_.content, 'html.parser')
        
        fm_link = soup.find('iframe').get('src')  # link to the actual formation page
        fm_page = requests.get(fm_link, allow_redirects=True)  # actual formation page
        
        directory = 'formations'
        if not os.path.isdir(directory):
            os.mkdir(directory)

        with open(f'{directory}/{fm_name}.html', 'wb') as f:
            f.write(fm_page.content)

    print('Success!')



def scrape_general_info(soup, val_dict):

    general_info_table = soup.find('table', class_='a155')
    general_info_rows = general_info_table.find_all('tr')

    for row in general_info_rows[1:]:
        divs = row.find_all('div')
        val_dict[divs[0].text].append(divs[-1].text)

    return val_dict

def scrape_wellbores(soup, fm_name):

    #--scraping 'Wellbores penetrating' table: contains all wellbores--#

    wellbores_table = soup.find('table', class_='a236')
    wellbores_rows = wellbores_table.find_all('tr')

    wellbores_cols = [div.text for div in wellbores_rows[1].find_all('div')] + ['Formation']
    wellbores_cols = list(filter(None, pd.unique(wellbores_cols)))
    
    wellbores_vals = []
    for row in wellbores_rows[2:]:
        divs = list(pd.unique([div.text for div in row.find_all('div')])) + [fm_name]
        wellbores_vals.append(divs)

    wellbores_df = pd.DataFrame(wellbores_vals, columns=wellbores_cols)

    #-------------------------------END--------------------------------#

    #----------------scraping 'Wellbores with cores' table-------------#

    withcores_table = soup.find('table', class_='a277')
    withcores_rows = withcores_table.find_all('tr')

    withcores_cols = [div.text for div in withcores_rows[1].find_all('div')]
    withcores_cols = list(filter(None, pd.unique(withcores_cols)))

    withcores_vals = []
    for row in withcores_rows[2:]:
        divs = pd.unique([div.text for div in row.find_all('div')])
        withcores_vals.append(divs)

    withcores_df = pd.DataFrame(withcores_vals, columns=withcores_cols)

    #-------------------------------END--------------------------------#

    # completion date col is already present in wellbores_df
    withcores_df.drop(withcores_cols[1], axis=1, inplace=True)
    
    all_df = wellbores_df.join(withcores_df.set_index(withcores_cols[0]),
                                on=wellbores_cols[0])
    # wellbores without cores will have core length = 0                            
    all_df.fillna(0, inplace=True)


    return all_df



def main():
    # page = requests.get(formations_root, allow_redirects=True)
    # if page.status_code != 200:
    #     print(page.status_code)
    # with open('1.html', 'wb') as f:
    #     f.write(page.content)

    # with open('1.html', encoding='utf-8') as f:
    #     soup = BeautifulSoup(f, 'html.parser')

    # download_formation_pages(soup)

    fm_directory = 'formations'
    val_dict = defaultdict(list)
    wellbores_df = pd.DataFrame()
    # parsing data
    for page in os.listdir(fm_directory):
        fpath = fm_directory + '/' + page
        with open(fpath, encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        val_dict = scrape_general_info(soup, val_dict)
        wellbore_name = list(val_dict.values())[0][-1]

        wellbores_df = pd.concat([wellbores_df, scrape_wellbores(soup, wellbore_name)])
    
    fm_df = pd.DataFrame.from_dict(val_dict)

    if not os.path.isdir('data'):
            os.mkdir('data')
    fm_df.to_csv('data/formations.csv', index=False)
    wellbores_df.to_csv('data/wellbores.csv', index=False)



if __name__ == '__main__':
    main()