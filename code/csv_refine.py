import pandas as pd
import datetime
import numpy as np

inpath = '../new_data/lithostrat_units.csv'
outpath = '../data/lithostrat_units.csv'
df = pd.read_csv(inpath,
                header=0
                )

lithology = {}
age = {}
badrows = []
for index, row in df['description'].iteritems():
    try:
        lithology[index] = row.split('Lithology')[1].split('\r\n')[1].strip()
        # print(lithology[index])
        
        age[index] = row.split('Age')[1].split('\r\n')[1].strip()
    except IndexError:
        badrows.append(index)
        pass

df.drop(badrows, inplace=True)
df['lithology'] = lithology.values()
df['age'] = age.values()
df.drop('description', axis=1, inplace=True)
print(df.head(100))

# print(lithology)
# print(df.head(10))
# print(df.columns)


df.to_csv(outpath, index=False)