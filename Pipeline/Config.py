import pymysql
import ssl

def get_conn():
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode    = ssl.CERT_NONE

    return pymysql.connect(
        host     = "live-exchange-pipeline.mysql.database.azure.com",
        port     = 3306,
        user     = "SahilJain",
        password = "Ireland@1008",
        database = "forex_pipeline",
        ssl      = ssl_ctx
    )