GitOps with FastAPI
==============

***University of Amsterdam***

# 1. Introduction

In this tutorial, we use GitOps practices with FastAPI, including CI/CD pipelines, code quality tools, and automated testing.

## Resources
* FastAPI
  - [Official Documentation](https://fastapi.tiangolo.com/)
  - [Tutorial - User Guide](https://fastapi.tiangolo.com/tutorial/)

* GitOps
  - [GitOps Principles](https://www.gitops.tech/)
  - [GitHub Actions Documentation](https://docs.github.com/en/actions)

* Code Quality
  - [Ruff Documentation](https://docs.astral.sh/ruff/)
  - [Black Documentation](https://black.readthedocs.io/)
  - [Pre-commit Documentation](https://pre-commit.com/)

* Testing
  - [Pytest Documentation](https://docs.pytest.org/)

* Docker
  - [Docker Documentation](https://docs.docker.com/)

* Kubernetes & Helm
  - [Kubernetes Documentation](https://kubernetes.io/docs/home/)
  - [Helm Documentation](https://helm.sh/docs/)
  - [Minikube Documentation](https://minikube.sigs.k8s.io/docs/)




# 2. Tutorial

The steps of this tutorial are as follows:
- [Building REST APIs with FastAPI](#21-setting-up-the-project)
- [Testing](#22-testing)
- [Code Quality](#23-code-quality)
- [Pre-commit Hooks](#24-pre-commit-hooks)
- [Docker](#25-docker)
- [Minikube Setup](#26-minikube-setup)
- [Kubernetes Deployment with Helm](#27-kubernetes-deployment-with-helm)

Prerequisites:
- Python 3.11 or higher
- Git
- Docker (optional, for containerization)
- GitHub account

## 2.1 Setting Up the Project
* Clone the Repository:
   ```bash
   git clone https://github.com/DevOps-and-Cloud-based-Software/fastapi-gitops.git
   cd fastapi-gitops-starter
   ```

* Set Up the Python Environmentt:

   ```bash
   # Create a virtual environment
   python -m venv venv

   # Activate the virtual environment
   # On Linux/MacOS:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt
   ```

* Run the Application:
   ```bash
   uvicorn app.main:app --reload
   ```

* Visit http://localhost:8000 to verify that the API is running.

* Explore the API:
  - API Documentation: http://localhost:8000/GitOps-Starter/docs
  - Root endpoint: http://localhost:8000/GitOps-Starter
  - Health check: http://localhost:8000/GitOps-Starter/health
  - List items: http://localhost:8000/GitOps-Starter/api/items
  - Retrieve a specific item: http://localhost:8000/GitOps-Starter/api/items/1

## 2.2 Testing

* Run Tests:
   ```bash
   pytest
   ```

  * Run Tests with Coverage:
   ```bash
   pytest --cov=app --cov-report=html
   ```

* Open `htmlcov/index.html` in a browser to view the coverage report.

##  2.3 Code Quality

* Linting with Ruff:

   ```bash
   # Check for issues
   ruff check app/ tests/

   # Fix auto-fixable issues
   ruff check app/ tests/ --fix
   ```

* Code Formatting with Black

   ```bash
   # Check formatting
   black --check app/ tests/

   # Format code
   black app/ tests/
   ```

## 2.4 Pre-commit Hooks

Pre-commit hooks automatically run checks before each commit to ensure consistent code quality.

* Setup Pre-commit:

   ```bash
   # Install pre-commit
   pip install pre-commit

   # Install the git hooks
   pre-commit install
   ```

* Using Pre-commit:

   Pre-commit will now run automatically on `git commit`. You can also run it manually:

   ```bash
   # Run on all files
   pre-commit run --all-files

   # Run on staged files
   pre-commit run
   ```

* The pre-commit hooks include:
  - Trailing whitespace removal
  - End of file fixer

## 2.5 Docker

* Build the Docker Image:
   ```bash
   docker build -t fastapi-gitops-starter .
   ```

* Run the Container:

   ```bash
   docker run -p 8000:8000 fastapi-gitops-starter
   ```
* Access the API at http://localhost:8000/GitOps-Starter/

## 2.6 Minikube Setup

To test the Kubernetes deployment locally, use Minikube.

* Install Minikube: Follow the instructions at the [Minikube installation guide](https://minikube.sigs.k8s.io/docs/start/).

* Start Minikube with Ingress and Ingress-DNS Addons:
   ```bash
   minikube start --addons=ingress,ingress-dns
   ```

* Add Minikube IP to /etc/hosts:
* Get the Minikube IP:
   ```bash
   minikube ip
   ```
* Add the following line to your `/etc/hosts` file:
   ```
   <MINIKUBE_IP> minikube.test
   ```
   Replace `<MINIKUBE_IP>` with the IP address obtained from the previous command.


## 2.7 Kubernetes Deployment with Helm

This repository includes a Helm chart for deploying the application to Kubernetes.

* Prerequisites
  - Kubernetes 1.19+
  - Helm 3.0+

* Install the Helm Chart:

   ```bash
   helm install my-release ./helm/fastapi-gitops-starter
   ```

* Uninstall the Helm Chart:

   ```bash
   helm uninstall my-release
   ```

Refer to `helm/README.md` for additional configuration options.
Make sure you understand how to set up the Horizontal Pod Autoscaler (HPA) for
scaling based on load and ingress configuration for accessing the application
including host and paths.

# 3. Exercises

## 3.0 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
6. Ensure all tests pass and code quality checks are successful
7. Merge

## 3.1 Add pre-commit Hooks
1. Open `.pre-commit-config.yaml`
2. Add a new hook to check:
   * To prevent committing large files
   * To check YAML files for syntax errors (excluding Helm charts)
   * To sort imports in Python files
   * To check for security issues
   * To make sure we do not commit secrets
   * To check code style


## 3.2 Add a New Endpoint

1. Open `app/main.py`
2. Add a new endpoint to create an item:

```python
@app.post("/api/items")
async def create_item(name: str, description: str):
    """Create a new item."""
    return {
        "id": 999,
        "name": name,
        "description": description,
        "created": True
    }
```

3. Write a test in `tests/test_main.py`
4. Run tests to verify


## 3.3 Add a CI Pipeline

1. Open `.github/workflows/ci-cd.yml`
2. Add a step to lint the code using Ruff
3. Add a step to run tests with coverage. The pipeline should fail if coverage is below 80%
4. Add a step to build the Docker image if tests pass. If we do a release, tag the image appropriately (with its version and the tag 'latest') and push it to GitHub registry


## 3.4 Deploy on a K8s "production" Cluster

1. Set up a Kubernetes cluster (e.g., using Minikube or a cloud provider)
2. Deploy the application using the Helm chart
3. Set up the scaling parameters in `custom-values.yaml` to handle more load by enabling Horizontal Pod Autoscaler (HPA). Set targetCPUUtilizationPercentage to 10%
4. Perform a load test using `hey`
```commandline
hey -z 30s  http://minikube.test/GitOps-Starter/api/items
```
6. Monitor the scaling of pods in the cluster:
```bash
kubectl get hpa -n default -w
```
7. Note how much time it takes for the pods to scale up and down based on the load

## 3.5 Questions

1. The auto-scaling did not work as expected. What could be the possible reasons?
2. How does Horizontal Pod Autoscaling (HPA) work in Kubernetes?