---
description: Forcefully create or reset the Sudo Admin user in the Render database
---
This workflow runs a Python script to connect directly to the Render production database and ensure that the root `sudo@JanSetu.com` account exists, is active, and has its password reset to `adminpassword`.

### Steps to Run

1. Open your Render Dashboard and navigate to your PostgreSQL database instance.
2. Find the **External Database URL** (e.g. `postgresql://user:pass@host/dbname`).
3. Run the script below, providing your Render DB URL as the argument:

```shell
cd c:\Users\abhay\Desktop\JanSetu\BackEnd
venv\Scripts\python.exe ..\.agents\workflows\scripts\seed_sudo.py --url "<YOUR_RENDER_DB_URL>"
```

*Note: Replace `<YOUR_RENDER_DB_URL>` with your actual database connection string. Once complete, you can log in as a Super Admin using `sudo@JanSetu.com` and `adminpassword`.*
