import pymongo
import pandas as pd

client = pymongo.MongoClient("mongodb+srv://marwa:marwa_98@cluster0-c3mtu.gcp.mongodb.net/test?retryWrites=true&w=majority")

db= client['aliexpress']
collection = db['product-flashdeals']
df= pd.read_excel('just_arrived_sephora.xlsx', index_col=0)
print(df)
db.collection.insert_many(df.to_dict('records'))