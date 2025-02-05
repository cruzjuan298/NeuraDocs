# Define Python virtual environment path
VENV = venv

# Define the name of the Docker container
CONTAINER_NAME = fastapi-backend

# Run the FastAPI application
run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Install dependencies inside virtual environment
install:
	python -m venv $(VENV)
	$(VENV)/bin/pip install -r requirements.txt

# Format Python code with black
format:
	$(VENV)/bin/black .

# Run the app using Docker
docker-build:
	docker build -t $(CONTAINER_NAME) .

docker-run:
	docker run -p 8000:8000 $(CONTAINER_NAME)

# Stop the running container
docker-stop:
	docker stop $(CONTAINER_NAME) || true
