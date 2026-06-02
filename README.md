# Docker with python web app
Docker Hub: https://hub.docker.com/r/guanadoo/web-python 

CI/CD testing: ```.github\workflows\docker-image.yml ```

* Create token in Docker Hub (rw/del)
* Create secrets in __Repository secrets__ (Secrets and var/Actions/Repo secrets)
```
DOCKERHUB_USERNAME with your docker-hub username
DOCKERHUB_TOCKEN with the secret
```


RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*
