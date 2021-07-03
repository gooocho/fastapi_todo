# fastapi_todo practice app

ToDo app made with FastAPI for practice

## how to run

```bash
docker-compose up -d
```

and visit

http://localhost:8080/docs

## how to run test

(docker-compose up -d) then

```bash
docker run --env-file .env --net=fastapi_todo_default fastapi_todo_app python3 -m pytest
```

## LICENSE

[MIT](https://choosealicense.com/licenses/mit/)
