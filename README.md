# Azure FastAPI Text Adventure

A tiny FastAPI web app you can deploy to **Azure App Service** from GitHub Actions in minutes.

## Quick Start

### 1) Create a new GitHub repo
- Create a **new empty repo** in your GitHub account (public or private).
- Download this project as a ZIP, unzip it, and run:
  ```bash
  cd azure-fastapi-text-adventure
  git init
  git remote add origin https://github.com/<YOUR-USER>/<YOUR-REPO>.git
  git add .
  git commit -m "Initial commit"
  git push -u origin main
  ```

### 2) Create your Azure Web App (Linux)
- In the Azure Portal: **Create Resource → Web App**
- Publish: **Code**
- Runtime stack: **Python 3.11 (Linux)**
- Region: your choice
- App name: choose something unique, e.g. `yourname-text-adv`

After creation, open the Web App → **Configuration → General settings** and set:
- **Startup command**:  
  `gunicorn -w 2 -k uvicorn.workers.UvicornWorker app:app`

*(You can also use the provided Dockerfile with Web App for Containers; this README focuses on code deployment.)*

### 3) Add the publish profile to GitHub
- In your Web App, go to **Overview → Get publish profile** (download the `.PublishSettings` file).
- In your GitHub repo: **Settings → Secrets and variables → Actions → New repository secret**  
  Name: `AZURE_WEBAPP_PUBLISH_PROFILE`  
  Value: paste the content of the publish profile file.

### 4) Update the workflow for your app name
- Edit `.github/workflows/azure-webapp.yml` and set `AZURE_WEBAPP_NAME` to your Web App name.

### 5) Push to deploy
Any push to `main` will build and deploy automatically. The action will:
- Install Python deps
- Upload the package
- Tell Azure to run with gunicorn/uvicorn

Open your site: `https://<YOUR-APP-NAME>.azurewebsites.net/`

## Local dev

```bash
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload
# open http://127.0.0.1:8000
```

## Extending

- Add routes in `app.py`, new templates in `templates/`, client code in `static/`.
- You can add Supabase later for auth/db; FastAPI integrates cleanly with `supabase-py` or direct REST.
- If you prefer containers, build and push an image, then point an **Azure Web App for Containers** to your registry.

## Troubleshooting

- If your site boots but returns 404, re-check the **Startup command** and that `app:app` exists.
- View logs in Azure Portal → Web App → **Log stream**.
- In GitHub, check Actions tab for deployment logs.