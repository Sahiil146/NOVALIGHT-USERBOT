# Light UserBot
# Copyright (C) 2021-2022 CodeWithTyagi
#
# This file is a part of < https://github.com/CodeWithTyagi/Light >
# Please read the GNU Affero General Public License in
# https://www.github.com/CodeWithTyagi/Light/blob/main/LICENSE

import os
import sys
from copy import deepcopy

from . import *


# ---------------------------------------------------------------------------------------------


Redis = MongoClient = psycopg2 = Database = None
if Var.REDIS_URI or Var.REDISHOST:
    try:
        from redis import Redis
    except ImportError:
        LOGS.info("Installing 'redis' for database.")
        os.system("pip3 install -q redis hiredis")
        from redis import Redis
elif Var.MONGO_URI:
    try:
        from pymongo import MongoClient
    except ImportError:
        LOGS.info("Installing 'pymongo' for database.")
        os.system("pip3 install -q pymongo[srv]")
        from pymongo import MongoClient
elif Var.DATABASE_URL:
    try:
        import psycopg2
    except ImportError:
        LOGS.info("Installing 'pyscopg2' for database.")
        os.system("pip3 install -q psycopg2-binary")
        import psycopg2
else:
    LOGS.critical(
        "No DB requirement fullfilled!\nPlease fill REDIS_URI or MONGO_URI in Var..."
    )
    exit()

# --------------------------------------------------------------------------------------------- #


class _BaseDatabase:
    def __init__(self, *args, **kwargs):
        self._cache = {}
        self.re_cache()

    def get_key(self, key):
        k = self._cache.get(key)
        return deepcopy(k) if bool(k) else k

    def re_cache(self):
        self._cache.clear()
        for key in self.keys():
            self._cache.update({key: self._get_data(key=key)})

    def ping(self):
        return 1

    @property
    def usage(self):
        return 0

    def keys(self):
        return []

    def del_key(self, key):
        if key in self._cache:
            del self._cache[key]
        return bool(self.delete(key))

    def _get_data(self, key=None, data=None):
        if key:
            try:
                data = self.get(str(key))
            except BaseException:
                return None
        if data:
            try:
                data = eval(data)
            except BaseException:
                pass
        return data

    def set_key(self, key, value):
        value = self._get_data(data=value)
        self._cache[key] = value
        return self.set(str(key), str(value))

    def rename(self, key1, key2):
        _ = self.get_key(key1)
        if _:
            self.del_key(key1)
            self.set_key(key2, _)
            return 0
        return 1


# ---------------------------------------------------------------------------------------------


class MongoDB(_BaseDatabase):
    def __init__(self, key, dbname="LightDB"):
        self.dB = MongoClient(key, serverSelectionTimeoutMS=6000)
        self.db = self.dB[dbname]
        super().__init__()

    def __repr__(self):
        return f"<light.MonGoDB\n -total_keys: {len(self.keys())}\n>"

    @property
    def name(self):
        return "Mongo"

    @property
    def usage(self):
        return self.db.command("dbstats")["dataSize"]

    def ping(self):
        if self.dB.server_info():
            return True

    def keys(self):
        return self.db.list_collection_names()

    def set_key(self, key, value):
        if key in self.keys():
            self.db[key].replace_one({"_id": key}, {"value": str(value)})
        else:
            self.db[key].insert_one({"_id": key, "value": str(value)})
        self._cache.update({key: value})
        return True

    def delete(self, key):
        self.db.drop_collection(key)

    def get(self, key):
        x = self.db[key].find_one({"_id": key})
        if x:
            return x["value"]

    def flushall(self):
        self.dB.drop_database("LightDB")
        self._cache.clear()
        return True


# --------------------------------------------------------------------------------------------- #

# Thanks to "Akash Pattnaik" / @BLUE-DEVIL1134
# for SQL Implementation in light.
#
# Please use https://elephantsql.com/ !


class SqlDB(_BaseDatabase):
    def __init__(self, url):
        self._url = url
        self._connection = None
        self._cursor = None
        try:
            self._connection = psycopg2.connect(dsn=url)
            self._connection.autocommit = True
            self._cursor = self._connection.cursor()
            self._cursor.execute(
                "CREATE TABLE IF NOT EXISTS light (lightCli varchar(70))"
            )
        except Exception as error:
            LOGS.exception(error)
            LOGS.info("Invaid SQL Database")
            if self._connection:
                self._connection.close()
            sys.exit()
        super().__init__()

    @property
    def name(self):
        return "SQL"

    @property
    def usage(self):
        self._cursor.execute("SELECT pg_size_pretty(pg_relation_size('light')) AS size")
        data = self._cursor.fetchall()
        return int(data[0][0].split()[0])

    def keys(self):
        self._cursor.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name  = 'light'"
        )  # case sensitive
        data = self._cursor.fetchall()
        return [_[0] for _ in data]

    def get(self, variable):
        try:
            self._cursor.execute(f"SELECT {variable} FROM light")
        except psycopg2.errors.UndefinedColumn:
            return None
        data = self._cursor.fetchall()
        if not data:
            return None
        if len(data) >= 1:
            for i in data:
                if i[0]:
                    return i[0]

    def set(self, key, value):
        try:
            self._cursor.execute(f"ALTER TABLE light DROP COLUMN IF EXISTS {key}")
        except (psycopg2.errors.UndefinedColumn, psycopg2.errors.SyntaxError):
            pass
        except BaseException as er:
            LOGS.exception(er)
        self._cache.update({key: value})
        self._cursor.execute(f"ALTER TABLE light ADD {key} TEXT")
        self._cursor.execute(f"INSERT INTO light ({key}) values (%s)", (str(value),))
        return True

    def delete(self, key):
        try:
            self._cursor.execute(f"ALTER TABLE light DROP COLUMN {key}")
        except psycopg2.errors.UndefinedColumn:
            return False
        return True

    def flushall(self):
        self._cache.clear()
        self._cursor.execute("DROP TABLE light")
        self._cursor.execute("CREATE TABLE IF NOT EXISTS light (lightCli varchar(70))")
        return True


# --------------------------------------------------------------------------------------------- #


class RedisDB(_BaseDatabase):
    def __init__(
        self,
        host,
        port,
        password,
        platform="",
        logger=LOGS,
        *args,
        **kwargs,
    ):
        if host and ":" in host:
            spli_ = host.split(":")
            host = spli_[0]
            port = int(spli_[-1])
            if host.startswith("http"):
                logger.error("Your REDIS_URI should not start with http !")
                import sys

                sys.exit()
        elif not host or not port:
            logger.error("Port Number not found")
            import sys

            sys.exit()
        kwargs["host"] = host
        kwargs["password"] = password
        kwargs["port"] = port

        if platform.lower() == "qovery" and not host:
            var, hash_, host, password = "", "", "", ""
            for vars_ in os.environ:
                if vars_.startswith("QOVERY_REDIS_") and vars.endswith("_HOST"):
                    var = vars_
            if var:
                hash_ = var.split("_", maxsplit=2)[1].split("_")[0]
            if hash:
                kwargs["host"] = os.environ(f"QOVERY_REDIS_{hash_}_HOST")
                kwargs["port"] = os.environ(f"QOVERY_REDIS_{hash_}_PORT")
                kwargs["password"] = os.environ(f"QOVERY_REDIS_{hash_}_PASSWORD")
        self.db = Redis(**kwargs)
        self.set = self.db.set
        self.get = self.db.get
        self.keys = self.db.keys
        self.delete = self.db.delete
        super().__init__()

    @property
    def name(self):
        return "Redis"

    @property
    def usage(self):
        return sum(self.db.memory_usage(x) for x in self.keys())


# --------------------------------------------------------------------------------------------- #


def LightDB():
    _er = False
    from .. import HOSTED_ON

    try:
        if Redis:
            LOGS.info("Connecting to Redis...")
            return RedisDB(
                host=Var.REDIS_URI or Var.REDISHOST,
                password=Var.REDIS_PASSWORD or Var.REDISPASSWORD,
                port=Var.REDISPORT,
                platform=HOSTED_ON,
                decode_responses=True,
                socket_timeout=6,
                retry_on_timeout=True,
            )
        if MongoClient:
            LOGS.info("Connecting to Mongo...")
            return MongoDB(Var.MONGO_URI)
        if psycopg2:
            LOGS.info("Connecting to SQL...")
            return SqlDB(Var.DATABASE_URL)
    except BaseException as err:
        LOGS.exception(err)
        _er = True
