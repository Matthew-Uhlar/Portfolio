#!/usr/bin/env bash
# Deploys Project Pilot to Azure Container Apps with Azure Database for PostgreSQL.
#
# Run it in Azure Cloud Shell (Bash) or anywhere the Azure CLI is signed in:
#   curl -fsSL https://raw.githubusercontent.com/Matthew-Uhlar/ai-project-management-assistant/main/deploy/azure/deploy.sh -o deploy.sh
#   bash deploy.sh
#
# Optional settings (export before running):
#   LOCATION           Azure region (default southcentralus, close to Austin)
#   RESOURCE_GROUP     default project-pilot-rg
#   ANTHROPIC_API_KEY  turns on the Claude-powered assistant; otherwise the rules engine answers
#   IMAGE_OWNER        GitHub owner of the container images (default matthew-uhlar)
#
# Delete everything afterward with:  az group delete --name project-pilot-rg --yes
set -euo pipefail

LOCATION="${LOCATION:-southcentralus}"
RESOURCE_GROUP="${RESOURCE_GROUP:-project-pilot-rg}"
IMAGE_OWNER="${IMAGE_OWNER:-matthew-uhlar}"
API_IMAGE="ghcr.io/${IMAGE_OWNER}/project-pilot-api:latest"
WEB_IMAGE="ghcr.io/${IMAGE_OWNER}/project-pilot-web:latest"
ENVIRONMENT="project-pilot-env"
API_APP="pp-api"
WEB_APP="pp-web"
DB_NAME="project_assistant"
DB_ADMIN="pilotadmin"
DB_SERVER="${DB_SERVER:-projectpilot-$(openssl rand -hex 3)}"
DB_PASSWORD="$(openssl rand -base64 30 | tr -dc 'A-Za-z0-9' | cut -c1-24)Aa1!"
JWT_KEY="$(openssl rand -base64 48 | tr -dc 'A-Za-z0-9' | cut -c1-64)"

echo "==> Checking the Azure CLI"
az account show --query "{subscription:name, user:user.name}" -o table
az extension add --name containerapp --upgrade --only-show-errors
az provider register --namespace Microsoft.App --wait
az provider register --namespace Microsoft.OperationalInsights --wait
az provider register --namespace Microsoft.DBforPostgreSQL --wait

echo "==> Creating resource group ${RESOURCE_GROUP} in ${LOCATION}"
az group create --name "$RESOURCE_GROUP" --location "$LOCATION" --output none

echo "==> Creating PostgreSQL flexible server ${DB_SERVER} (smallest burstable size, takes about 5 minutes)"
az postgres flexible-server create \
  --resource-group "$RESOURCE_GROUP" \
  --name "$DB_SERVER" \
  --location "$LOCATION" \
  --tier Burstable \
  --sku-name Standard_B1ms \
  --storage-size 32 \
  --version 16 \
  --admin-user "$DB_ADMIN" \
  --admin-password "$DB_PASSWORD" \
  --public-access 0.0.0.0 \
  --yes \
  --output none

az postgres flexible-server db create \
  --resource-group "$RESOURCE_GROUP" \
  --server-name "$DB_SERVER" \
  --database-name "$DB_NAME" \
  --output none

CONNECTION="Host=${DB_SERVER}.postgres.database.azure.com;Port=5432;Database=${DB_NAME};Username=${DB_ADMIN};Password=${DB_PASSWORD};SSL Mode=Require;Trust Server Certificate=true"

echo "==> Creating the Container Apps environment"
az containerapp env create \
  --name "$ENVIRONMENT" \
  --resource-group "$RESOURCE_GROUP" \
  --location "$LOCATION" \
  --output none

SECRETS=("db-connection=${CONNECTION}" "jwt-key=${JWT_KEY}")
ENV_VARS=(
  "ASPNETCORE_URLS=http://+:8080"
  "ConnectionStrings__DefaultConnection=secretref:db-connection"
  "Jwt__Key=secretref:jwt-key"
  "Jwt__Issuer=ProjectAssistant"
  "Jwt__Audience=ProjectAssistantClient"
)
if [[ -n "${ANTHROPIC_API_KEY:-}" ]]; then
  SECRETS+=("anthropic-key=${ANTHROPIC_API_KEY}")
  ENV_VARS+=("Ai__ApiKey=secretref:anthropic-key")
  echo "    The assistant will use Claude."
else
  echo "    No ANTHROPIC_API_KEY set, so the assistant will use the built-in rules engine."
fi

echo "==> Deploying the API (internal only, scales to zero when idle)"
az containerapp create \
  --name "$API_APP" \
  --resource-group "$RESOURCE_GROUP" \
  --environment "$ENVIRONMENT" \
  --image "$API_IMAGE" \
  --target-port 8080 \
  --ingress internal \
  --min-replicas 0 \
  --max-replicas 1 \
  --cpu 0.5 --memory 1.0Gi \
  --secrets "${SECRETS[@]}" \
  --env-vars "${ENV_VARS[@]}" \
  --output none

echo "==> Deploying the web app (public)"
az containerapp create \
  --name "$WEB_APP" \
  --resource-group "$RESOURCE_GROUP" \
  --environment "$ENVIRONMENT" \
  --image "$WEB_IMAGE" \
  --target-port 80 \
  --ingress external \
  --min-replicas 0 \
  --max-replicas 1 \
  --cpu 0.25 --memory 0.5Gi \
  --env-vars "API_URL=http://${API_APP}" \
  --output none

URL="https://$(az containerapp show --name "$WEB_APP" --resource-group "$RESOURCE_GROUP" --query properties.configuration.ingress.fqdn -o tsv)"

cat <<DONE

Project Pilot is deployed:  ${URL}

Demo logins:
  admin@example.com / Admin123!
  member@example.com / Member123!

The apps scale to zero, so the first visit after a quiet period takes 20 to 40 seconds to wake up.
The database is the main cost. Stop it when you are not demoing:
  az postgres flexible-server stop --resource-group ${RESOURCE_GROUP} --name ${DB_SERVER}
Remove everything:
  az group delete --name ${RESOURCE_GROUP} --yes
DONE
