#!/bin/bash
# ./azure/login.sh
# Login to Azure CLI using environment variables

az account show --query id -o tsv