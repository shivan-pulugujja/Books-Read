import pandas as pd

df = pd.read_csv('books.csv',index_col='isbn')
for ind in df.index:
    print(type(ind)," ",df['title'][ind],df['author'][ind],type(df['year'][ind]))
    