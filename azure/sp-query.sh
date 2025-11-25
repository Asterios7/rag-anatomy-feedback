#!/bin/bash

az ad sp list --display-name "github-actions-sp" --query "[].{appId:appId,displayName:displayName}" -o table