# IMPORT UTILITY PACKAGES
import sys
from sklearn.externals import joblib 
from azure.storage.blob import BlockBlobService

# GET DEVICE TYPE AND OIL TEMPRATURE FROM COMMANDLINE
device = sys.argv[1]
oilTemp = sys.argv[2]

# READ MODEL FROM AZURE BLOB STORAGE
blob_account = "akshaystorageaccount1"
blob_key = "0Z1RtdiCfYhMO7cfD7aSq/rsew7Ry7fhZcarQqTdlpscEYwhFYRjs45h7FboSM5PWehRWGnVNB5hgwkGT4WFlA=="
blob_container = "datasciencefilecontainer"
blob_service = BlockBlobService(account_name=blob_account, account_key=blob_key)
blob_service.get_blob_to_path(blob_container, "model_{0}".format(device), "model_{0}.model".format(device))
model = joblib.load("model_{0}.model".format(device))

if -1 == model.predict(oilTemp):
    print("ALARM! anamoly detected")
else:
    print("Cool! no anamoly")