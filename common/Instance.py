import os
import imp
import _thread
import signal
import configparser
import json
from migrate.versioning import api
from common.SimpleDB import SimpleDB
from common.ResultAndData import *
from models import db_base
import time

APP_NAME = 'my-app'

def get_from_conf(config, key, default):
    return config.get("root", key) if config.has_option("root", key) else default


class Instance(object):
    def __init__(self):
        """
        Creates a Instance which can track database and authentication state
        """

        # This section is all needed by Instance itself
        # app_root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        self._working_dir = os.path.join(".localdata")
        self._db = None
        self._db_name = f"{APP_NAME}.db"
        self._conf_file_name = f"{APP_NAME}.conf"
        self._db_models = db_base
        self._db_map = {}

        ########################################################################
        # These properties should be consumed as part of the configuration.
        #
        # If you need to log into an API, you could store that in the instance
        # as instance.session as an example (ms-cli does this with the graph
        # session.)
        self.session = None
        self._current_user_guid = None
        ########################################################################
        # Finally, call init_dir, which will create or load the database, and
        # load the config file.
        self.init_dir()

    def init_dir(self):
        """
        1. creates the WD if it doesn't exist
        2. Reads data from the working dir
        3. creates the db if it doesn't exist
        """

        # 1.
        exists = os.path.exists(self._working_dir)
        if not exists:
            os.makedirs(self._working_dir)
        else:
            # 2.
            self.load_conf()

        # 3.
        exists = os.path.exists(self._db_path())
        # print("The db does not exist" if not exists else "The db already exists")
        self._db = self.make_db_session()
        self._db.engine.echo = False
        if not exists:
            print("Creating db...")
            self._db.create_all_and_repo(self._db_migrate_repo())
            print(
                "The database ({}) should have been created here".format(
                    self._db_path()
                )
            )
            print("The migration repo should have been created here")

    def _db_uri(self):
        return "sqlite:///" + self._db_path()

    def _db_migrate_repo(self):
        return os.path.join(self._working_dir, "db_repository")

    def get_db(self):
        thread_id = _thread.get_ident()

        if not (thread_id in list(self._db_map.keys())):
            db = self.make_db_session()
            self._db_map[thread_id] = db

        return self._db_map[thread_id]

    def make_db_session(self):
        db = SimpleDB(self._db_uri(), self._db_models)
        db.engine.echo = False
        return db

    def _db_path(self):
        return os.path.join(self._working_dir, self._db_name)

    def migrate(self):
        repo = self._db_migrate_repo()
        uri = self._db_uri()
        db = self.get_db()
        migration_name = "%04d_migration.py" % (api.db_version(uri, repo) + 1)
        migration = repo + "/versions/" + migration_name
        tmp_module = imp.new_module("old_model")
        old_model = api.create_model(uri, repo)
        exec(old_model, tmp_module.__dict__)
        script = api.make_update_script_for_model(
            uri, repo, tmp_module.meta, db.Base.metadata
        )
        open(migration, "wt").write(script)
        api.upgrade(uri, repo)
        print("New migration saved as " + migration)
        print("Current database version: " + str(api.db_version(uri, repo)))
        api.upgrade(uri, repo)
        print("New database version: " + str(api.db_version(uri, repo)))

    def _parse_config(self, config=None):
        # TODO: Load user configuration from the file. You can do this however
        # you like.
        #
        # For example:
        # self._current_user_name = get_from_conf(
        #     config, "user_name", self._current_user_name
        # )
        # self.api_toked = get_from_conf(
        #     config, "API_TOKEN", self.api_token
        # )
        pass

    def load_conf(self):
        conf_file = self.get_config_file_path()
        if not os.path.exists(conf_file):
            return

        config = configparser.RawConfigParser()
        with open(conf_file) as stream:
            config.readfp(stream)
            self._config = config
        self._parse_config(self._config)
