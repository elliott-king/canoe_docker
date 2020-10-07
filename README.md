https://github.com/elliott-king/canoe_docker

Backend Docker creation:
```bash
docker build -t backend:latest backend
docker run -v $PWD/backend:/app/backend backend:latest django-admin startproject hello_world .
docker run -v $PWD/backend:/app/backend -p 8000:8000 backend:latest
```

Frontend Docker creation:
```bash
docker build -t frontend:latest frontend
docker run -v $PWD/frontend:/app frontend:latest npx create-react-app hello-world
mv frontend/hello-world/* frontend/hello-world/.gitignore frontend/ && rmdir frontend/hello-world
docker run -v $PWD/frontend:/app -p 3000:3000 frontend:latest npm start
```

Creating the migrations:
```bash
docker exec -it <container_id> python manage.py makemigrations
docker exec -it <container_id> python manage.py migrate
docker exec -it <container_id> python manage.py seed
```

Loading from tar:
```bash
docker load --input frontend.tar
docker load --input backend.tar
docker-compose up
```