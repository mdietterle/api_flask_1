-- schema.sql
create table if not exists dados (
    id integer primary key autoincrement,
    nome text not null,
    idade integer not null,
    id_cidade integer not null
);

create table if not exists cidades (
    id_cidade integer primary key autoincrement,
    nome_cidade text not null,
    uf_cidade text not null)