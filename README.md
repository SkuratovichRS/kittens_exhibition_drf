# Kitten Exhibition API

## To run the project, follow these steps:

1. Clone the repository: `git clone git@github.com:SkuratovichRS/kittens_exhibition_drf.git`
2. Create a `.env` file with variables from `.env.example`
3. Build the Docker image: `docker build -t api:latest .`
4. Execute `docker compose up -d`
5. Swagger is available at `http://localhost:8000/docs/`

### Tests:

1. Create a virtual environment: `python -m venv venv`
2. Activate the virtual environment: `source venv/bin/activate` (On Windows, use `venv\Scripts\activate`)
3. Install dependencies: `pip install -r requirements-dev.txt`
4. Start the database: `docker compose up db -d`
5. Execute tests with `pytest`

**P.S.** This is a simple deployment version; for production, consider deploying with Gunicorn and Nginx.