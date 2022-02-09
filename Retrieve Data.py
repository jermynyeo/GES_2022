import requests
import pandas as pd 
import tabula
import glob

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

df = pd.DataFrame()
for year in range(2013, 2020): 
    url_base = "https://data.gov.sg"
    endpoint = "/api/action/datastore_search?resource_id=9326ca53-9153-4a9c-b93f-8ae032637b70&q=" + str(year)

    while (True):     
        r = requests.get(url_base + endpoint)
        data = r.json()['result']
        if (data['records'] == []): 
            break
        endpoint = data['_links']['next']
        temp_df = pd.json_normalize(data, ["records"])
        temp_df.drop(columns=["_full_count"], inplace=True)
        temp_df.set_index('_id', inplace=True, drop=True)
        df = df.append(temp_df)

df.to_csv("data/GES_2013_2019.csv")

# files = glob.glob('data/*.pdf')
# for input_file in files: 
#     school = input_file.split("-")[2]
#     output_file = f"data/{school}_2020.csv"
#     tabula.convert_into(input_file, output_file, pages='all')