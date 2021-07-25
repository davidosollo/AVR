.open avr_users.sqlite

drop table if exists users;
    create table users (
    id integer primary key autoincrement,
    username text not null,
    password text not null
);

INSERT INTO users (username,password) VALUES ('dosollo','palmi4708');
INSERT INTO users (username,password) VALUES ('rflores','start123');
INSERT INTO users (username,password) VALUES ('jrodas','starttreck');

drop table if exists proyecto_avr;
    create table proyecto_avr (
    id integer primary key autoincrement,
    proyecto text not null
);
