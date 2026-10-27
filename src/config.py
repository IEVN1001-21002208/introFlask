class DevelopmentConfig:
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'admin_utl'
    MYSQL_PASSWORD = 'password123'
    MYSQL_DB = 'api_utl'
    MYSQL_CURSORCLASS = 'Cursor'

config = {
    'development': DevelopmentConfig
}