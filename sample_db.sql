DROP SCHEMA IF EXISTS sample CASCADE;
CREATE SCHEMA sample;

--User table
DROP TABLE IF EXISTS sample.users CASCADE;
CREATE TABLE sample.users (
  id serial PRIMARY KEY,
  first_name VARCHAR(80) DEFAULT NULL,
  last_name VARCHAR(80) DEFAULT NULL,
  email VARCHAR(80) DEFAULT NULL
);

INSERT INTO sample.users (id, first_name, last_name, email) VALUES(nextval('sample.users_id_seq'), 'John', 'Doe', 'john.doe@xyzcompany.com');
INSERT INTO sample.users (id, first_name, last_name, email) VALUES(nextval('sample.users_id_seq'), 'Jane', 'Doe', 'wane.doe@xyzcompany.com');
INSERT INTO sample.users (id, first_name, last_name, email) VALUES(nextval('sample.users_id_seq'), 'William', 'Smith', 'william.smith@abccompany.com');
INSERT INTO sample.users (id, first_name, last_name, email) VALUES(nextval('sample.users_id_seq'), 'Mary', 'Smith', 'mary.smith@abccompany.com');
