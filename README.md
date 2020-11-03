# Azure batch ml sample

This repository demonstarte how to train models parallely using Azure Batch AI service.

You can refere architecture diagram for building blocks of solution.

![Solution Block Diagram](https://github.com/Coder-2xx/batch-ml/blob/master/using-azure-batch-ai/solution-architecture.png)

Solution depends on:

* Azure IoT Hub
* Azure Stream Analytics
* Azure Batch AI
* Azure Storage - SQL, BLOB

Solution steps:

1. Devices (Transformers) are connected to Azure IoT Hub. Devices are sending sensor data to Azure IoT Hub per 30 seconds. Azure IoT Hub is used for connecting IoT devices at scale.
2. Stream Analytics job will run on injested data and aggregate it per device type for last five minutes (10 sensor values per feature). Aggreagated data will be saved to Azure SQL database.
3. We need to run [create-batch-ai-jobs.py](https://github.com/Coder-2xx/batch-ml/blob/master/using-azure-batch-ai/create-batch-ai-jobs.py) file to create jobs for training a model for each device type.
4. Jobs will create ML model for respective device type and save it to Azure BLOB.
5. To detect an anamoly, we can run [detect-oil-temprature-anamoly.py](https://github.com/Coder-2xx/batch-ml/blob/master/using-azure-batch-ai/detect-oil-temprature-anamoly.py) and pass device type, oil temperature as command line parameters. It will return whether its anamoly or not.
