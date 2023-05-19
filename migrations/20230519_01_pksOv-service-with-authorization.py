"""
Service with authorization
"""

from yoyo import step

__depends__ = {}

steps = [
    step("""create table service.auth
            (
                id          serial
                    primary key,
                name        varchar(54)  not null
                    unique,
                public_key  varchar(256) not null
                    unique,
                private_key varchar(512) not null
                    unique,
                url         varchar(256)
            );""",
         "DROP TABLE service.auth")
]
