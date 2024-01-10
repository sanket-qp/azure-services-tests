APP_NAME = "mysimpleblog"

def get_schema_name():
    return "%s_schema" % APP_NAME

def get_db_name():
    return "%s_db" % APP_NAME

def get_article_table_name():
    return "%s.article" % get_schema_name()
