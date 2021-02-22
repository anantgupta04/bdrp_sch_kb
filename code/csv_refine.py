import pandas as pd
import datetime
import numpy as np
from random import sample

inpath = '../new_data/discovery_description.csv'
outpath = '../test_data/discovery_description.csv'
df = pd.read_csv(inpath,
                header=0
                )
to_drop = []
for i in df.columns:
    if 'id' in i:
        to_drop.append(i)
df.drop(to_drop, axis=1, inplace=True)
# df = df[df['description_heading']=='Development ']
# df.drop('description_heading', axis=1, inplace=True)
# lithology = {}
# age = {}
# badrows = []
# for index, row in df['description'].iteritems():
#     try:
#         lithology[index] = row.split('Lithology')[1].split('\r\n')[1].strip()
#         # print(lithology[index])
        
#         age[index] = row.split('Age')[1].split('\r\n')[1].strip()
#     except IndexError:
#         badrows.append(index)
#         pass

# df.drop(badrows, inplace=True)
# df['lithology'] = lithology.values()
# df['age'] = age.values()
# df.drop('description', axis=1, inplace=True)
# print(df.head(100))

# print(lithology)
print(df.head(10))
# print(df.columns)

# not_cores = df[df['core_length']==0].index
# df.drop(not_cores, inplace=True)
# unique = df.wellbore_id.unique()
# for elem in unique:
#     indices = list(df[df['wellbore_id'] == elem].index)
#     to_drop = sample(indices, len(indices)-1)
#     df.drop(to_drop, inplace=True)

df.to_csv(outpath, index=False)
