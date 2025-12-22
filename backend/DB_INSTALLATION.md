# Database Adapter Installation Guide

This project uses PostgreSQL as the database backend. Here are different installation approaches for the psycopg2 adapter:

## Option 1: Using psycopg2-binary (Recommended for development)

This is the easiest method as it uses pre-compiled binaries:

```
pip install psycopg2-binary
```

## Option 2: Using psycopg2 (For production)

If you encounter issues with psycopg2-binary, you can try installing the source version, but you'll need to have PostgreSQL development libraries installed first:

### For Windows:
1. Install PostgreSQL from https://www.postgresql.org/download/windows/
2. Make sure pg_config is in your PATH
3. Install using:
```
pip install psycopg2
```

### For Ubuntu/Debian:
```
sudo apt-get install python3-dev libpq-dev
pip install psycopg2
```

### For CentOS/RHEL/Fedora:
```
sudo yum install python3-devel postgresql-devel
# or for newer versions:
sudo dnf install python3-devel postgresql-devel
pip install psycopg2
```

## Troubleshooting Common Issues

### Issue: "pg_config executable not found"
- **Solution**: Install PostgreSQL development package or ensure pg_config is in your PATH

### Issue: "Failed building wheel for psycopg2"
- **Solution**: Use psycopg2-binary instead of psycopg2
- **Alternative**: Install build dependencies as mentioned above

### Issue: "Microsoft Visual C++ 14.0 is required" (Windows)
- **Solution**: Install psycopg2-binary instead, or install Microsoft C++ Build Tools

## Alternative: Using a Different Database

If you continue to have issues with PostgreSQL, you can modify the database configuration to use SQLite for development:

1. Replace `psycopg2-binary` with `sqlalchemy` in requirements
2. Change the database URL in your code to use SQLite:
   - From: `postgresql://user:password@host:port/database`
   - To: `sqlite:///./chatbot.db`

## Using asyncpg (Alternative PostgreSQL driver)

If you prefer an async driver, you can use asyncpg instead:

```
pip install asyncpg
```

Then modify your database connections to use asyncpg instead of psycopg2.