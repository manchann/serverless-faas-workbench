#!/bin/bash

# Function app and storage account names must be unique.
export AZURE_STORAGE_ACCOUNT=jgstorage$RANDOM
region=westus
shareName=jgfileshare2
directoryName=jgdir
rg=RG

# Create a resource group.
az group create --name $rg --location $region

# Create an Azure storage account in the resource group.
az storage account create \
  --name $AZURE_STORAGE_ACCOUNT \
  --location $region \
  --resource-group $rg \
  --sku Standard_LRS

# Set the storage account key as an environment variable.
export AZURE_STORAGE_KEY=$(az storage account keys list -g $rg -n $AZURE_STORAGE_ACCOUNT --query '[0].value' -o tsv)

az storage share create \
  --name $shareName

# Create a directory in the share.
az storage directory create \
  --share-name $shareName \
  --name $directoryName
