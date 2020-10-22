from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from models import db_base as base
import os
import json

__author__ = "zadjii"


class Comment(base):
    __tablename__ = "comment"
    """
    Represents a single comment
    """

    id = Column(Integer, primary_key=True)
    raw_data = Column(String)
    api_id = Column(Integer)
    issue_number = Column(Integer, ForeignKey("issue.number"))


    issue = relationship(
        "Issue",
        foreign_keys=[issue_number],
        backref=backref("comments", remote_side=[issue_number], lazy="dynamic"),
    )

    def __init__(self, issue_model, api_obj):
        self.api_id = api_obj.id
        self.issue_number = issue_model.number
        self.raw_data = json.dumps(api_obj._rawData)
