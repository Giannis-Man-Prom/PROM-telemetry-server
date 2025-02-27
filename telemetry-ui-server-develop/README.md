# telemetry-ui-server


## Docker

---

- ### Handling images
  - There are three different ways to name/tag local images, and build them
  
    - When Building an image -> ```docker build -t <hub-user>/<already-created-repo-name>[:<tag>]```
    - Re-taging a local image -> ```docker tag <existing-image> <hub-user>/<already-created-repo-name>[:<tag>]```
    - By committing changes -> ```docker tag <existing-container> <hub-user>/<already-created-repo-name>[:<tag>]```

- ### Development environment (Linux)

  - To start the server in a development environment  
  ```
  docker-compose -p <container_name> --env-file ../.env -f docker-compose.dev.yml up --build -d
  ```
  - To Stop and remove the containers 
  ```
  docker compose -p <servername> down 
  ```
  
- ### Development environment (Windows)

  - To start the server in a development environment  
  ```
  docker-compose -p <container_name> --env-file ../.env -f docker-compose.dev.yml up --build -d
  ```
  - To Stop and remove the containers 
  ```
  docker compose -p <servername> down 
  ```

