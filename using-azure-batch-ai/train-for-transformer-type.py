# import basic utility packages
import sys
import json
from time import sleep

# import data processing and ML model utility packages
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.svm import OneClassSVM
from sklearn.pipeline import Pipeline
import pickle

# import DB access utility packages
import pyodbc
from azure.storage.blob import BlockBlobService


# get device name/id from query params
device = sys.argv[1]
print("Started working on job for {0}".format(device))

# get data from Azure SQL
sql_con_string = "Driver={ODBC Driver 13 for SQL Server};Server=tcp:akshayd.database.windows.net,1433;Database=nitadsqldb;Uid=akshay@akshayd;Pwd=$wami@SQL;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
sql_query = "SELECT [OilTemp] FROM [TransformerData] WHERE [DeviceId]='{0}'"
query = sql_query.format(device)
cnxn = pyodbc.connect(sql_con_string)
cursor = cnxn.cursor()
    
# loop through cursored data
def get_vals(cursor, n=1000):
    while True:
        results = cursor.fetchmany(n)
        if not results:
            break
        for result in results:
            yield result

cursor.execute(query)
vals = [x[0] for x in get_vals(cursor, 1000)]
vals = np.array(vals)

print("{0} Data: ".format(device), vals.size)

if 0 == vals.size:
    print ("No data found for {0}".format(device))

else:
    # train model using SVM algo (two class classification)
    sc = StandardScaler()
    clf = OneClassSVM(nu=0.0001, kernel='rbf', gamma=0.01)
    pipe = Pipeline(steps=[('scaler', sc), ('classifier', clf)])
    pipe.fit(vals.reshape(-1, 1))

    # save ML-SVM model to Azure Blob storage
    blob_account = "<blob account name>"
    blob_key = "<blob account access key>"
    blob_container = "<blob container name>"
    model_file_name = 'model_{0}'.format(device)
    blob_service = BlockBlobService(
        account_name=blob_account, account_key=blob_key)
    blob_service.create_blob_from_bytes(
        blob_container, model_file_name, pickle.dumps(pipe))

print("Completed working on job for {0}".format(device)) 