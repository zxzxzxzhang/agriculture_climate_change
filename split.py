
import pandas as pd
df =  pd.read_excel(r'new_agriculture_data.xlsx')


df['申请年'] = df['申请年'].astype(str)
df1 = df[(df['申请年'] <= '2000')]
df2 = df[(df['申请年'] >= '2001') & (df['申请年'] <= '2010')]
df3 = df[(df['申请年'] >= '2011') & (df['申请年'] <= '2015')]
df4 = df[(df['申请年'] >= '2016') & (df['申请年'] <= '2020')]
df5 = df[(df['申请年'] >= '2021') & (df['申请年'] <= '2024')]

df1.to_excel('./evolutionary_path/data_1984-2000.xlsx', index=False)
df2.to_excel('./evolutionary_path/data_2001-2010.xlsx', index=False)
df3.to_excel('./evolutionary_path/data_2011-2015.xlsx', index=False)
df4.to_excel('./evolutionary_path/data_2016-2020.xlsx', index=False)
df5.to_excel('./evolutionary_path/data_2021-2024.xlsx', index=False)

