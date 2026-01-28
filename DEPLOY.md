# Deployment Guide for Vercel

## Prerequisites
- **Vercel CLI**: Ensure you have the Vercel CLI installed.
  ```bash
  npm install -g vercel
  ```
- **Kutrim API Key**: You will need your API key `6CIYq3OVlXswA9FW4eME6Hqv`.

## Deployment Steps

1. **Login to Vercel**
   Open your terminal in the project root (`d:\SmartEdu-Agent`) and run:
   ```bash
   vercel login
   ```
   Follow the instructions to log in.

2. **Deploy the Project**
   Run the deployment command:
   ```bash
   vercel
   ```
   - Set up and deploy? **Yes**
   - Which scope? **[Select your scope]**
   - Link to existing project? **No**
   - Project name? **smartedu-agent** (or your preference)
   - In which directory is your code located? **./** (Keep default)
   - Want to modify these settings? **No** (We have set up `vercel.json` for you)

3. **Set Environment Variables**
   Once the project is linked, go to the Vercel Dashboard for your project.
   - Go to **Settings** > **Environment Variables**.
   - Add the following:
     - **Key**: `KUTRIM_API_KEY`
     - **Value**: `6CIYq3OVlXswA9FW4eME6Hqv`
   
   - Also, for the frontend to talk to the backend, you typically need to set the API URL. However, since they are on the same Vercel deployment, the relative path or default `/api` routing defined in `vercel.json` should handle it.
   - If you face issues, add:
     - **Key**: `VITE_API_BASE_URL`
     - **Value**: `https://your-project-name.vercel.app` (The URL Vercel gives you).

4. **Redeploy (if needed)**
   If you added environment variables after the build started, you might need to redeploy:
   ```bash
   vercel --prod
   ```

## Local Development
To run locally with the same configuration:
```bash
vercel dev
```
