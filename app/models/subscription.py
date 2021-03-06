# Import Column and types directly from sqlalchemy because pylint
# doesn't detect them if we imported them via the "db" object
from sqlalchemy.sql.schema import Column, ForeignKey
import sqlalchemy.sql.sqltypes as st

from app import db



class Subscription(db.Model):
    id = Column(st.Integer, primary_key=True, autoincrement=True)

    subscriber_id = Column(st.Integer, ForeignKey('user.id'), nullable=False)
    subscribed_id =  Column(st.Integer, ForeignKey('user.id'), nullable=False)

    """
    @returns Subscriber object, representing subscription between two users
    """
    def __init__(self, subscriber_id: int, subscribed_id: int):
        
        self.subscriber_id = subscriber_id
        self.subscribed_id = subscribed_id