# Define Python virtual environment path
VENV = venv

# Define the name of the Docker container
CONTAINER_NAME = fastapi-backend

# Detect OS and set appropriate Python executable
ifeq ($(OS),Windows_NT)
    PYTHON = python
    VENV_PYTHON = $(VENV)/Scripts/python
    VENV_PIP = $(VENV)/Scripts/pip
else
    PYTHON = python3
    VENV_PYTHON = $(VENV)/bin/python
    VENV_PIP = $(VENV)/bin/pip
endif

# Run the FastAPI application with hot reload
run-backend:
	cd backend && uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Build the frontend
build-frontend:
	cd frontend && npm run build	

# Run the frontend development server
run-frontend:
	cd frontend && npm run preview

# Install dependencies inside virtual environment
install:
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv $(VENV)
	@echo "Installing dependencies..."
	$(VENV_PIP) install -r requirements.txt
	@echo "Installation complete!"

# Format Python code with black
format:
	$(VENV_PYTHON) -m black .

# Run the app using Docker
docker-build:
	docker build -t $(CONTAINER_NAME) .

docker-run:
	docker run -p 8000:8000 $(CONTAINER_NAME)

# Stop the running container
docker-stop:
	docker stop $(CONTAINER_NAME) || true

# Start both frontend and backend with hot reloading
start:
	concurrently "make run-frontend" "make run-backend"

# Install all dependencies (both frontend and backend)
install-all:
	make install
	cd frontend && npm install

# Clean virtual environment
clean:
	rm -rf $(VENV)
	rm -rf frontend/node_modules
