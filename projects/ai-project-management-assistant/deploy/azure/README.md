# Deploy Project Pilot to Azure

The `Publish Project Pilot images` GitHub Actions workflow builds the API and web images and pushes them to GitHub Container Registry. `deploy.sh` then creates everything on Azure:

| Piece | Azure service | Notes |
| --- | --- | --- |
| Web frontend (nginx + React) | Container Apps, external ingress | Public HTTPS URL, scales to zero |
| API (ASP.NET Core 8) | Container Apps, internal ingress | Only reachable from the web app |
| Database | PostgreSQL flexible server, Burstable B1ms | The main cost. Stop it between demos |

## Steps

1. Make sure the images are public: on GitHub open **Packages**, then `project-pilot-api` and `project-pilot-web`, then **Package settings**, and set visibility to **Public**. You only do this once.
2. Open [Azure Cloud Shell](https://shell.azure.com) in Bash mode (or use any machine with the Azure CLI signed in).
3. Optional: `export ANTHROPIC_API_KEY=...` to turn on the Claude-powered assistant.
4. Run:

   ```bash
   curl -fsSL https://raw.githubusercontent.com/Matthew-Uhlar/ai-project-management-assistant/main/deploy/azure/deploy.sh -o deploy.sh
   bash deploy.sh
   ```

5. The script prints the public URL and the demo logins.

## Cost

Container Apps includes a monthly free grant that a demo app at this size stays within. The PostgreSQL B1ms server is included in the Azure free account for 12 months, and otherwise costs roughly $12 to $15 a month while running. Stop it when you're not demoing:

```bash
az postgres flexible-server stop --resource-group project-pilot-rg --name <server name from the script output>
```

Delete everything with `az group delete --name project-pilot-rg --yes`.
