CREATE TABLE IF NOT EXISTS ${appfunc}_schema.article (
    id bigserial primary key,
    title varchar(20) NOT NULL,
    writeup text NOT NULL,
    date_added timestamp default NOW()
);

INSERT INTO ${appfunc}_schema.article (title, writeup) 
    VALUES
    ('hello_postgres', 'article about testing postgres'),
    ('hello_redis', 'article about testing redis');
