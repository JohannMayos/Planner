from sqlalchemy import create_engine


db_connection_string = "mysql+pymysql://17zl1rrafh2ccae7kx92:pscale_pw_MNhjUbibXB9FNcpgSB4L6ID2Gwldsksj80ITa08fFcq@aws-sa-east-1.connect.psdb.cloud/plannerdb?charset=utf8mb4"

engine = create_engine(db_connection_string, connect_args={
    "ssl":{
        "ssl_ca": "/etc/ssl/cert.pem"
    }
})

