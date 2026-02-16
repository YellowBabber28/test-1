# Database Setup Guide

## Quick Setup

The "Tenant or user not found" error means your database connection is not configured correctly.

## Step 1: Create .env File

Copy the template file:
```bash
# Windows PowerShell
Copy-Item backend\env.template backend\.env

# Linux/Mac
cp backend/env.template backend/.env
```

## Step 2: Get Your Supabase Connection String

1. Go to your **Supabase Dashboard**: https://supabase.com/dashboard
2. Select your project (the same one used by GeniusLaw)
3. Go to **Settings** → **Database**
4. Scroll down to **Connection string**
5. Select **Transaction mode** (not Session mode)
6. Copy the connection string

The connection string should look like:
```
postgresql://postgres.[PROJECT_REF]:[YOUR_PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres?sslmode=require
```

## Step 3: Update backend/.env

Edit `backend/.env` and replace the DATABASE_URL:

```env
DATABASE_URL=postgresql://postgres.[PROJECT_REF]:[YOUR_PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres?sslmode=require
```

**Important:**
- Replace `[PROJECT_REF]` with your actual project reference (e.g., `abcdefghijklmnop`)
- Replace `[YOUR_PASSWORD]` with your actual database password
- Replace `[REGION]` with your region (e.g., `us-west-1`, `us-east-1`, etc.)

## Step 4: Set SUPABASE_POOLER_HOST (if needed)

If you still get "Tenant or user not found", you may need to set the pooler host explicitly.

In your Supabase Dashboard → Settings → Database, look for the pooler hostname. It should be something like:
- `aws-0-us-west-1.pooler.supabase.com`
- `aws-0-us-east-1.pooler.supabase.com`
- etc.

Add this to your `backend/.env`:
```env
SUPABASE_POOLER_HOST=aws-0-[YOUR_REGION].pooler.supabase.com
```

## Step 5: Verify Connection

After updating `.env`, restart the application:
```bash
python run.py
```

You should see:
```
[DB] Supabase PostgreSQL pool initialized successfully
```

## Using the Same Database as GeniusLaw

If you want to use the **exact same database** as GeniusLaw:

1. Check the GeniusLaw project's `.env` file (if accessible)
2. Copy the `DATABASE_URL` and `SUPABASE_POOLER_HOST` values
3. Paste them into `RA automator/backend/.env`

The RA Automator will use the same `users` table, so you can log in with the same credentials!

## Troubleshooting

### "Tenant or user not found"
- Verify your `DATABASE_URL` username includes the project ref: `postgres.[PROJECT_REF]`
- Check that the pooler host region matches your Supabase project region
- Ensure `SUPABASE_POOLER_HOST` is set to the correct region

### "Network is unreachable"
- Make sure you're using the **pooler** host (port 6543), not the direct host (port 5432)
- Verify your network allows connections to Supabase

### "Invalid password"
- Double-check your database password in the connection string
- Make sure there are no extra spaces or quotes in the `.env` file
