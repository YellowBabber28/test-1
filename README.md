# RA Automator

A premium SaaS-style web application built with HTML, CSS, Vanilla JavaScript, and Python FastAPI.

## Features

- 🎨 **Premium UI/UX** - Modern, clean design with smooth animations
- 🔐 **Secure Authentication** - JWT-based auth with bcrypt password hashing
- 🗄️ **Supabase Integration** - Uses the same database as GeniusLaw
- 📱 **Responsive Design** - Works beautifully on desktop and mobile
- ⚡ **Fast Performance** - Optimized for speed

## Tech Stack

- **Frontend**: HTML, CSS, Vanilla JavaScript
- **Backend**: Python FastAPI
- **Database**: Supabase (PostgreSQL)
- **Authentication**: JWT tokens, bcrypt password hashing

## Project Structure

```
ra-automator/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── auth/
│   │   ├── routes.py        # Authentication endpoints
│   │   └── deps.py          # Auth dependencies
│   ├── core/
│   │   ├── config.py        # Configuration
│   │   ├── security.py      # Security utilities
│   │   └── database.py      # Database connection
│   └── .env                 # Environment variables
├── public/
│   ├── index.html           # Landing page
│   ├── signup.html          # Signup page
│   ├── login.html           # Login page
│   ├── dashboard.html       # Protected dashboard
│   ├── css/
│   │   ├── theme.css        # CSS variables
│   │   └── style.css        # Main styles
│   └── js/
│       ├── auth.js          # Authentication utilities
│       └── guard.js         # Route protection
└── requirements.txt         # Python dependencies
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

**⚠️ IMPORTANT:** You must configure your database connection before running the app.

Copy the example environment file:

```bash
# Windows PowerShell
Copy-Item backend\env.template backend\.env

# Linux/Mac
cp backend/env.template backend/.env
```

Edit `backend/.env` and set your Supabase connection details. See **[SETUP_DATABASE.md](SETUP_DATABASE.md)** for detailed instructions.

**Quick Setup:**
1. Go to your Supabase Dashboard → Settings → Database
2. Copy the **Connection string** (Transaction mode)
3. Paste it into `backend/.env` as `DATABASE_URL`
4. Replace `[PASSWORD]` with your actual database password

**Example:**
```env
DATABASE_URL=postgresql://postgres.[PROJECT_REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres?sslmode=require
JWT_SECRET=your-secret-key-change-in-production
```

**💡 Tip:** If you're using the same database as GeniusLaw, copy the `DATABASE_URL` from the GeniusLaw project's `.env` file!

### 3. Run the Application

**Important:** Always run from the project root directory (`RA automator/`)

**Option 1: Using the run script (Recommended)**
```bash
cd "RA automator"
python run.py
```

**Option 2: Using uvicorn directly**
```bash
cd "RA automator"
# On Windows PowerShell:
$env:PYTHONPATH = (Get-Location).Path
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# On Linux/Mac:
export PYTHONPATH=$(pwd)
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at:
- **http://localhost:8000** (use this in your browser)
- **http://127.0.0.1:8000** (alternative)

**Note:** Even though the server binds to `0.0.0.0:8000`, you should access it via `localhost` or `127.0.0.1` in your browser.

## API Endpoints

### Authentication

- `POST /api/signup` - Register a new user
- `POST /api/login` - Authenticate and get JWT token
- `GET /api/me` - Get current user information (protected)
- `POST /api/logout` - Logout (client-side token removal)

### Health Check

- `GET /api/health` - Health check endpoint

## Database

RA Automator uses the same Supabase database as GeniusLaw. It connects to the existing `users` table:

- **Email**: Unique identifier
- **Password Hash**: Bcrypt hashed password
- **Role**: User role (default: "client")

The application does NOT modify the database schema - it only reads from and writes to the existing `users` table.

## Security

- Passwords are hashed using bcrypt (cost factor: 10)
- JWT tokens are used for authentication
- Tokens are stored in localStorage (client-side)
- Protected routes automatically redirect to login if unauthenticated
- CORS is configurable via environment variables

## Development

### Frontend Development

The frontend uses vanilla JavaScript with no build step required. Simply edit the HTML, CSS, and JS files in the `public/` directory.

### Backend Development

The backend uses FastAPI with hot-reload enabled. Changes to Python files will automatically reload the server.

## License

This project is part of the GeniusLaw ecosystem.
