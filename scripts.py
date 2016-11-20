import json
import logging 
import os

from model import (
    Collection, 
    Configuration, 
    DisplayItem, 
    MediaResource, 
    production_session,
)


class Script(object):

    @property
    def _db(self):
        if not hasattr(self, "_session"):
            self._session = production_session()
        return self._session

    @property
    def log(self):
        if not hasattr(self, '_log'):
            logger_name = getattr(self, 'name', None)
            self._log = logging.getLogger(logger_name)
        return self._log        

    @property
    def data_directory(self):
        return Configuration.data_directory()

    @classmethod
    def parse_command_line(cls, _db=None, cmd_args=None):
        parser = cls.arg_parser()
        return parser.parse_known_args(cmd_args)[0]

    @classmethod
    def arg_parser(cls):
        raise NotImplementedError()

    @classmethod
    def parse_time(cls, time_string):
        """Try to pass the given string as a time."""
        if not time_string:
            return None
        for format in ('%Y-%m-%d', '%m/%d/%Y', '%Y%m%d'):
            for hours in ('', ' %H:%M:%S'):
                full_format = format + hours
                try:
                    parsed = datetime.datetime.strptime(
                        time_string, full_format
                    )
                    return parsed
                except ValueError, e:
                    continue
        raise ValueError("Could not parse time: %s" % time_string)

    def __init__(self, _db=None):
        """Basic constructor.

        :_db: A database session to be used instead of
        creating a new one. Useful in tests.
        """
        if _db:
            self._session = _db

    def run(self):
        self.load_configuration()
        try:
            self.preload_tables(self._db)
        except Exception, e:
            logging.error(
                "Fatal exception while running script: %s", e,
                exc_info=e
            )
            raise e

    def load_configuration(self):
        if not Configuration.instance:
            Configuration.load()


    def preload_tables(self, db):
        base_path = os.path.split(__file__)[0]
        #self.resource_path = os.path.join(base_path, "files", "oneclick")
        path = os.path.join(base_path, "example.json")
        data = open(path).read()
        dict_data = json.loads(data)

        collections = dict_data['collections']
        coll_1 = Collection()
        coll_1.name = collections[0]['name']
        coll_1.curator = collections[0]['curator']
        display_items = collections[0]['display_items']
        db.commit()

        print "hi"



