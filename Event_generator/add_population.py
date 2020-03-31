import pandas as pd
import sys
from random import randint,seed
records = pd.read_csv(sys.argv[1])
seed(1)
records['population'] = [randint(50,5000) for i in range(len(records))]
out_file = sys.argv[1][:-4]+"_with_population.csv"
records.to_csv (out_file, index = False, header=True)
