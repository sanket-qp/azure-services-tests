/**
Hack as psycopg2 is running in to issues while running multiple statements
Ref: http://tinyurl.com/stackoverflowpost
**/
DROP DATABASE IF EXISTS ${appname}_db; 