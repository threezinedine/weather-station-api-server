from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Table,
)

from database.base import Base


StationUser = Table("stations_users", Base.metadata, 
            Column("userId", Integer, ForeignKey("users.userId")),
            Column("stationId", Integer, ForeignKey("stations.stationId")))
