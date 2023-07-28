create table book (
    id serial,
    title varchar(128) not null,
    author varchar(32) not null,
    publisher varchar(32) not null,
    isbn varchar(64) not null,
    genre varchar(64) not null,
    primary key(id)
);

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(64),
  hashed_password VARCHAR(64),
  salt VARCHAR(30)
);

CREATE TABLE admin (
  id SERIAL PRIMARY KEY,
  name VARCHAR(64),
  hashed_password VARCHAR(64),
  salt VARCHAR(30)
);