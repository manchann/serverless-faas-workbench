#!/bin/bash

# Function app and storage account names must be unique.
export AZURE_STORAGE_ACCOUNT=jgstorage$RANDOM
functionAppName=jgfuncRANDOM
region=koreacentral
pythonVersion=3.6 #3.6 also supported
shareName=jgfileshare2
directoryName=jgdir
shareId=jgshare$RANDOM
mountPath=/ap

# Create a resource group.
az group create --name jgRG --location $region

# Create an Azure storage account in the resource group.
az storage account create \
  --name $AZURE_STORAGE_ACCOUNT \
  --location $region \
  --resource-group jgRG \
  --sku Standard_LRS

# Set the storage account key as an environment variable. 
export AZURE_STORAGE_KEY=$(az storage account keys list -g jgRG -n $AZURE_STORAGE_ACCOUNT --query '[0].value' -o tsv)

# Create a serverless function app in the resource group.
az functionapp create \
  --name $functionAppName \
  --storage-account $AZURE_STORAGE_ACCOUNT \
  --consumption-plan-location $region \
  --resource-group jgRG \
  --os-type Linux \
  --runtime python \
  --runtime-version $pythonVersion \
  --functions-version 2

# Work with Storage account using the set env variables.
# Create a share in Azure Files.
az storage share create \
  --name $shareName 

# Create a directory in the share.
az storage directory create \
  --share-name $shareName \
  --name $directoryName

az webapp config storage-account add \
  --resource-group jgRG \
  --name $functionAppName \
  --custom-id $shareId \
  --storage-type AzureFiles \
  --share-name $shareName \
  --account-name $AZURE_STORAGE_ACCOUNT \
  --mount-path $mountPath \
  --access-key $AZURE_STORAGE_KEY

az webapp config storage-account list \
  --resource-group jgRG \
  --name $functionAppName
