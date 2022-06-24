# ProjectVending

## Backend:

Python: 3.9.12

Auth: JWT

Web Server: Uvicorn

API Framework: FastAPI

Database: Sqlite3


## Frontend:

Vue.js 2.6.10

State: Vuex 3.1.2

Styling: Bootstrap-vue 2.22.0

Router: Vue-Router 3.1.3

Bundler: Webpack 4.41.2


# Database Schema
```
sqlite> .schema
CREATE TABLE users (
    id    INTEGER,
    username text,
    password text,
    deposit integer,
    role text,
    PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE UNIQUE INDEX unique_username on users(username);
CREATE TABLE products (
    amountAvailable integer,
    cost integer,
    productName text,
    sellerID integer,
    FOREIGN KEY(sellerID) REFERENCES users(id) ON DELETE CASCADE
);
```

## Populating Database:
:warning: **Do not forget to enable foreign keys** `PRAGMA foreign_keys = ON;`


:warning: **Do not forget to insert all fields, even AUTOINCREMENT ones**

```
insert into users values (NULL,"johndoe","$2a$04$p29EJ5B2laL/0GmeoLforOHIop2VsfGaspTGpFft.c6WmqZw/uWvq",0,"buyer");
insert into users values (NULL,"bestseller","$2a$04$F9QUdILE2wVO4u/dvnr.jORc6vdM5KuN.uvw9wuKKqP6pk2voS0im",0,"seller");
insert into users values (NULL,"competitorseller","$2a$04$OrkXInJMjYPaT0rumo1SP.ny9xUmEnGyyo3ky/uqUh6dyKm5yPqDO",0,"seller");

insert into products values (1,60,"Cola",2);
insert into products values (1,120,"Sprite",2);
insert into products values (1,5,"Water",2);
insert into products values (1,300,"Beer",2);
insert into products values (1,275,"BetterBeer",3);
```


# Running Backend

Start uvicorn on 5000 port.
 `uvicorn main:app --reload --port 5000`
 
 :warning: **For tests to work, server must be running**

 Run tests
 `pytest`
 
 Get Coverage report
 ```
 coverage run -m pytest
 
 coverage html
 
 open htmlcov/index.html
 ```
 
 ## Coverage Preview
![image](https://user-images.githubusercontent.com/39850379/175528633-5fde492d-2a30-4ba8-a207-a47f17cd76d0.png)


