import pandas as pd
df1 = pd.read_csv("processed_incidents_part1.csv")
df2 = pd.read_csv("processed_incidents_part2.csv")
df3 = pd.read_csv("processed_incidents_part3.csv")
df4 = pd.read_csv("processed_incidents_part4.csv")
df5 = pd.read_csv("processed_incidents_part5.csv")
full = pd.concat([df1, df2, df3, df4, df5])
full.to_csv("processed_incidents.csv", index=False)
