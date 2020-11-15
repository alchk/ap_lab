#AP PET PROJECT

##Description
  Actually, i don`t like python and pyenv or venv
  I like Java, Docker and docker-compose up

##How to run
  ```bash
pip install --requirement requirements.txt
```
```bash

gunicorn --bind 0.0.0.0:8080 app:app
```
##HealthCheck
http://localhost:8080/api/v1/hello-world-1

  