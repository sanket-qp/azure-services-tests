CREATE SCHEMA test_schema;

CREATE TABLE test_schema.article (
    article_id bigserial primary key,
    article_name varchar(20) NOT NULL,
    article_desc text NOT NULL,
    date_added timestamp default NOW()
);

INSERT INTO test_schema.article (article_name, article_desc) 
    VALUES
    ('hello_postgres', 'article about testing postgres'),
    ('hello_redis', 'article about testing redis');
