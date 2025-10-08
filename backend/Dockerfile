FROM python:3.12-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies globally (no venv needed in container)
RUN uv pip install --system -e .[dev]

# Copy project files
COPY . .

# Create data directory for SQLite
RUN mkdir -p /app/data

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
