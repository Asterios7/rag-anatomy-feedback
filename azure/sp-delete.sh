#!/bin/bash
# Usage: ./delete-sp.sh <appId>
# Deletes an Azure Service Principal with the given appId

if [ -z "$1" ]; then
  echo "Usage: $0 <appId>"
  exit 1
fi

APP_ID="$1"

echo "Deleting Service Principal with appId: $APP_ID ..."
az ad sp delete --id "$APP_ID"

if [ $? -eq 0 ]; then
  echo "Service Principal deleted successfully."
else
  echo "Failed to delete Service Principal."
fi