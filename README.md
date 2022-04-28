# Project Description

This project is Vending Machine challenge.
We have two application frontend and backend. 

* Frontend is made with **Next.js**. 

* Backend is made with **FastAPI**.

> I never used these programming languages before.

## Run application with docker
1) Make sure docker and docker-compose is configured in your machine.
2) Run following command
    ```bash
    docker-compose build
    docker-compose up -d
    ```

## Run application without docker
To run it without using docker you need to have following installed:

1. Backend
    * You have to have **Python 3.9** or above.
    * You need to install **poetry** globally for install package.
      ```bash
      pip install poetry
      ```
    * You have to have **mysql** up and running for database.
    
### Run backend project
1. Change directory to backend and install required packages:
    ```bash
    cd backend
    poetry install
    ```
2. Change [env](backend/.env) file according to your database environment.

3. Run application. To run it in dev mode:
    ```bash
    uvicorn app.main:app --port 8000 --reload   
    ```
4. If everything goes well and you have set your backend default running port as 8000, you can visit your application through [http://localhost:8000](http://localhost:8000)

5. To view swagger documentation visit [http://localhost:8000/docs](http://localhost:8000/docs)

   
### Run Frontend project
1. Change directory to frontend and install required dependencies:
    ```bash
    cd frontend
    yarn i
    ```
2. Set up environment. In .env file add:
    ```env
    NEXT_PUBLIC_API_URL=http://localhost:8000
    ```
3. Run your application:
    ```bash
    yarn dev
    ```
4. If everything goes well, you can visit your application through [http://localhost:3000](http://localhost:3000) 

## Prerequisite
### Migrations
Before use the application, run migration command for initial database

  * For Docker
    * Run following command for migrate database
      ```bash
      docker-compose run --rm backend alembic revision --autogenerate -m "init"

      docker-compose run --rm backend alembic upgrade head
      ```
  * Without Docker
    * Run following command for migrate database
      ```bash
      alembic revision --autogenerate -m "init"

      alembic upgrade head
      ```
### Prepare data
  * Use ```POST /api/v1/machine``` API to create machine configuration (name, number of coins or banknotes in machine). For Example:
    ```bash
    curl -X 'POST' \
      'http://localhost:8000/api/v1/machine' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{
      "name": "Vending Machine",
      "one_coin": 10,
      "five_coin": 10,
      "ten_coin": 10,
      "twenty_banknote": 10,
      "fifty_banknote": 10,
      "hundred_banknote": 0,
      "five_hundred_banknote": 0,
      "thousand_banknote": 0
    }'
    ```
  * Use ```POST /api/v1/coin``` API to initail customer coin (number of coins or banknotes). For Example:
    ```bash
    curl -X 'POST' \
      'http://localhost:8000/api/v1/coin' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{
      "one_coin": 0,
      "five_coin": 0,
      "ten_coin": 0,
      "twenty_banknote": 0,
      "fifty_banknote": 0,
      "hundred_banknote": 0,
      "five_hundred_banknote": 0,
      "thousand_banknote": 0
    }'
    ```
  * Use ```POST /api/v1/products``` API to create products. For Example:
    ```bash
    curl -X 'POST' \
      'http://localhost:8000/api/v1/products' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{
      "name": "Coca C",
      "price": 15,
      "stock": 10
    }'
    ```
  * See the [swagger documentation](http://localhost:8000/docs) for more API information.