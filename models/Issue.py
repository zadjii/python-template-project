from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from models import db_base as base
import os
import json

__author__ = "zadjii"


class Issue(base):
    __tablename__ = "issue"
    """
    Represents a single issue
    """

    id = Column(Integer, primary_key=True)
    raw_data = Column(String)
    number = Column(Integer)

    def __init__(self, api_obj):
        self.number = api_obj.number
        self.raw_data = json.dumps(api_obj._rawData)
