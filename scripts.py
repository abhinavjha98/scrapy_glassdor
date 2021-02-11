import pandas as pd
import numpy as np

data = pd.read_csv('r111.csv')

data.drop_duplicates(subset ="Company_name",keep=False,inplace=True)

data.to_csv('Sorted_Data.csv',index=False)