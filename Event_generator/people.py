import pandas as pd
from random import randint,seed
seed(1)
data = [[i,randint(15,70)] for i in range(900000,1000000)]
pd.DataFrame(data,columns=['SSN','Age']).to_csv('people.csv',index = False, header=True)
