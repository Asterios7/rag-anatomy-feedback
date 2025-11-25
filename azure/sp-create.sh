#!/bin/bash
# Usage: bash ./sp-create.sh <subscription-id>
# Creates an Azure Service Principal and outputs creds to creds.json

if [ -z "$1" ]; then
  echo "Usage: $0 <subscription-id>"
  exit 1
fi

SUBSCRIPTION_ID="$1"
SP_NAME="github-actions-sp"
OUTPUT_FILE="creds.json"

echo "Creating Service Principal '$SP_NAME' for subscription $SUBSCRIPTION_ID ..."

# Create SP and save JSON to creds.json
az ad sp create-for-rbac \
    --name "$SP_NAME" \
    --role Contributor \
    --scopes "/subscriptions/$SUBSCRIPTION_ID" \
    --query "{clientId: appId, clientSecret: password, tenantId: tenant, subscriptionId: '$SUBSCRIPTION_ID'}" \
    -o json > "$OUTPUT_FILE"

if [ $? -eq 0 ]; then
  echo "Service Principal created successfully!"
  echo "Credentials saved to $OUTPUT_FILE"
else
  echo "Failed to create Service Principal."
  exit 1
fi