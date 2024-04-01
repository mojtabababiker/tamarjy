#!/usr/bin/env python
"""the database storage module, which is hold the DatabaseStorage class
"""
from os import environ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class DatabaseStorage:
    """The DatabaseStorage class, which is responsible for all the
    database operations, such as connecting to the database, inserting
    data, updating data, deleting data, and querying the database
    """
    def __init__(self):
        """Initiate the DatabaseStorage class"""
        self.__engine = None
        self.__session = None
        url = "mysql://{}:{}@{}/{}".format(
            environ['MYSQL_USER'],
            environ['MYSQL_PWD'],
            environ['MYSQL_HOST'],
            environ['MYSQL_DB']
        )
        self.__engine = create_engine(url, pool_pre_ping=True)

    def reload(self):
        """Create all the Base model models and Reload
        the data from the database"""
        from models.base_model import Base
        from models.user import User
        from models.clinic import Clinic
        from models.disease import Disease
        from models.appointment import Appointment

        # self.classes will be used by the rest of the methods
        self.classes = {'User': User, 'Clinic': Clinic, 'Disease': Disease,
                        'Appointment': Appointment}

        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def rollback(self):
        """Rollback the session"""
        self.__session.rollback()

    def close(self):
        """Close the current session"""
        self.__session.close()

    def new(self, obj):
        """Add the object to the database
        parameters:
        -------------
        obj: the object to add to the database
        """
        self.__session.add(obj)

    def save(self):
        """Save and commit the changes to the database"""
        self.__session.commit()

    def delete(self, obj):
        """Delete data from the database
        parameters:
        -------------
        obj: the object to delete from the database
        """
        self.__session.delete(obj)

    def get(self, cls, filters: dict={}):
        """Get the data from the database according to the filters
        parameters:
        -------------
        cls: the class of the object
        filters: the filters to apply to the query
        return:
        -------------
        result: the result of the query
        """
        if isinstance(cls, str):
            cls = self.classes[cls]
        if filters:
            return self.__session.query(cls).filter_by(**filters).all()
        return self.__session.query(cls).all()
