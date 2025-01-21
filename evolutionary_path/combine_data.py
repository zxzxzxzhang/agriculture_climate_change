import pandas as pd

df1 = pd.read_excel('result_1984-2000.xlsx')
df2 = pd.read_excel('result_2001-2010.xlsx')
df3 = pd.read_excel('result_2011-2015.xlsx')
df4 = pd.read_excel('result_2016-2020.xlsx')
df5 = pd.read_excel('result_2021-2024.xlsx')

df = pd.concat([df1, df2, df3, df4,df5],axis=1)

df.columns = ['A0', 'B0', 'B1', 'C0', 'C1', 'C2', 'D0', 'D1', 'D2','E0', 'E1', 'E2']

df.to_excel(r'./sankey/TR_result.xlsx', index=False)
