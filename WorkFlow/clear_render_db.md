---
description: Clear dummy users and complaints from the Render database
---
This workflow runs a Python script to connect to the Render production database and clear all dummy users, complaints, complaint activities, updates, and OTPs while preserving the admin users.

### Steps to Run

1. Open your Render Dashboard and navigate to your PostgreSQL database instance.
2. Find the **External Database URL** (e.g. `postgresql://user:pass@host/dbname`).
3. Run the script below, providing your Render DB URL as the argument:

```shell
cd c:\Users\abhay\Desktop\JanSetu\BackEnd
venv\Scripts\python.exe ..\.agents\workflows\scripts\clear_render_db.py --url "<YOUR_RENDER_DB_URL>"
```

*Note: Replace `<YOUR_RENDER_DB_URL>` with your actual database connection string. You can append `--force` at the end to skip the terminal confirmation prompt.*
