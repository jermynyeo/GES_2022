import requests
import pandas as pd 
import tabula
import glob

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

r = requests.get("https://data.gov.sg/api/action/datastore_search?resource_id=9326ca53-9153-4a9c-b93f-8ae032637b70")
data = r.json()['result']

df = pd.json_normalize(data, ["records"])
df.set_index('_id', inplace=True, drop=True)
print (df.columns)


files = glob.glob('data/*.pdf')
for input_file in files: 
    school = input_file.split("-")[2]
    output_file = f"data/{school}_2020.csv"
    tabula.convert_into(input_file, output_file, pages='all')