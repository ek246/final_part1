# 📎 Quick Links

https://hub.docker.com/repository/docker/edocidss22/final_part1/general
## Testing
Run Docker, open Bash in the project folder, and run the following commands:
- source venv/bin/activate
- pip install -r requirements.txt
- docker compose up -d db
- export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/fastapi_db"
- export TEST_DATABASE_URL="postgresql://postgres:postgres@localhost:5432/fastapi_test_db"
- pytest  
These commands assume that you already have the `fastapi_test_db` database created
## Documentation

documentation folder containing screenshots is included. It contains:

- Screenshot of successful GitHub Actions:
[Screenshot of successful GitHub Actions](documentation/GitHub_Actions.png)
[Screenshot of successful Docker Hub push](documentation/DockerHub.png)