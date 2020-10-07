#!/bin/bash

# Function app and storage account names must be unique.
export AZURE_STORAGE_ACCOUNT=jgstorage30507
functionAppName=jgfunc1
region=westus
pythonVersion=3.6 #3.6 also supported
shareName=jgfileshare2
shareId=jgshare1
mountPath=/ap
rg=RG

# Set the storage account key as an environment variable.
export AZURE_STORAGE_KEY=$(az storage account keys list -g $rg -n $AZURE_STORAGE_ACCOUNT --query '[0].value' -o tsv)

# Create a serverless function app in the resource group.
az functionapp create \
  --name $functionAppName \
  --storage-account $AZURE_STORAGE_ACCOUNT \
  --consumption-plan-location $region \
  --resource-group $rg \
  --os-type Linux \
  --runtime python \
  --runtime-version $pythonVersion \
  --functions-version 2


# Work with Storage account using the set env variables.
# Create a share in Azure Files.
az webapp config storage-account add \
  --resource-group $rg \
  --name $functionAppName \
  --custom-id $shareId \
  --storage-type AzureFiles \
  --share-name $shareName \
  --account-name $AZURE_STORAGE_ACCOUNT \
  --mount-path $mountPath \
  --access-key $AZURE_STORAGE_KEY

az webapp config storage-account list \
  --resource-group $rg \
  --name $functionAppName