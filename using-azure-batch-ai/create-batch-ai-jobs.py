# IMPORT UTILITY PACKAGES
import os
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.compute import ComputeManagementClient
import azure.mgmt.batchai as batchai
import azure.mgmt.batchai.models as model

# AZURE SERVICE PRINCIPLE LOGIN CREDENTIALS
TENANT_ID = "<AZURE TENANT ID>"
CLIENT = '<CLIENT ID>'
KEY = '<PASSWORD>'

# BATCH AI CLUSTER PROPERTIES
resource_group_name = "<RESOURCE GROUP CONTAINING AZURE BATCH AI CLUSTER>"
subscription_id = '<SUBSCRIPTION ID>'
workspace_name = "<WORKSPACE NAME>"
cluster_name = '<CLUSTER NAME>'
location = '<LOCATION OF RESOURCE>'
experiment_name = "<EXPERIMENT NAME>"
node_count = 1
std_out_err_path_prefix = '<FILE SHARE TO SAVE ERROR LOGS>'

# DEVICE TYPES
device_ids = ["Transformer001", "Transformer003",
              "Transformer005", "Transformer007", "Transformer009"]

# LOG IN AND CREATE CLIENT
credentials = ServicePrincipalCredentials(
    client_id=CLIENT,
    secret=KEY,
    tenant=TENANT_ID
)

batchai_client = batchai.BatchAIManagementClient(
    credentials=credentials, subscription_id=subscription_id)

# GET CLUSTER OBJECT
cluster = batchai_client.clusters.get(
    resource_group_name, workspace_name, cluster_name)

# DELETE JOBS IF EXISTS
for j in batchai_client.jobs.list_by_experiment(resource_group_name, workspace_name, experiment_name):
    print("Deleting job- ",j.name)
    batchai_client.jobs.delete(
        resource_group_name, workspace_name, experiment_name, j.name)
    print ("Deleted job- {0}".format(j.name))

# RUN AN ASYNC JOB FOR EACH DEVICE TYPE (EXECUTE TRAIN.PY FOR EACH DEVICE TYPE)
for device_id in device_ids:
    job_name = 'train-{0}'.format(device_id)
    print ("Creating job- {0}".format(job_name))
    custom_settings = model.CNTKsettings(
        python_script_file_path="$AZ_BATCHAI_MOUNT_ROOT/nitadfileshare/train_for_transformer.py",
        command_line_args=device_id)

    params = model.JobCreateParameters(
        cluster=model.ResourceId(id=cluster.id),
        node_count=node_count,
        std_out_err_path_prefix=std_out_err_path_prefix,
        cntk_settings=custom_settings    )

    batchai_client.jobs.create(
        resource_group_name, workspace_name, experiment_name, job_name, params)
    print ("Created job- {0}".format(job_name))