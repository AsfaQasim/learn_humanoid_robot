To run the backend, navigate to the `backend` directory and execute the following command:

```bash
cd backend
poetry run uvicorn src.main:app --reload
```

You will need to ensure you have the necessary environment variables set up as described in `backend/README.md` (OPENAI_API_KEY, QDRANT_HOST, QDRANT_API_KEY, NEON_DATABASE_URL).