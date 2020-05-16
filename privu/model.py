#!/usr/bin/env python
#coding=utf-8

import os
from typing import List, Tuple

from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.sql.elements import TextClause

import flask_login


class DBAgent():
    def __init__(self):
        self.db_uri = ''
        self.db = None

    def setup_db(self, dbfilepath : str) -> None:
        self.db_uri = f"sqlite:///{dbfilepath}"
        self.db = create_engine(self.db_uri)

        with self.db.connect() as conn:
            try:
                conn.execute(text("""CREATE TABLE IF NOT EXISTS privu_files (
                                       filecode CHAR(6) PRIMARY KEY,
                                       filename TEXT NOT NULL UNIQUE
                                     ) """))
            except:
                raise

    def add_one_file(self, filecode : str, filename : str) -> None:
        with self.db.connect() as conn:
            try:
               conn.execute(text("""INSERT INTO privu_files (filecode, filename)
                                         VALUES (:filecode, :filename) """),
                            {"filecode": filecode,
                             "filename": filename})
            except:
                raise


    def check_one_code(self, filecode : str) -> str:
        with self.db.connect() as conn:
            try:
                rspxy = conn.execute(text("""SELECT filename
                                               FROM privu_files
                                              WHERE filecode = :filecode"""),
                                     {"filecode": filecode})

                rs = rspxy.fetchone()
                if rs is not None:
                    return rs[0]
                else:
                    return '-'
            except:
                raise

    def find_one_file(self, filename : str) -> str:
        with self.db.connect() as conn:
            try:
                rspxy = conn.execute(text("""SELECT filecode
                                               FROM privu_files
                                              WHERE filename = :filename"""),
                                     {"filename": filename})

                rs = rspxy.fetchone()
                if rs is not None:
                    return rs[0]
                else:
                    return '-'
            except:
                raise

    def find_files(self) -> List[Tuple[str, str]]:
        with self.db.connect() as conn:
            try:
                rspxy = conn.execute(text("""SELECT filecode
                                                  , filename
                                               FROM privu_files """))
                rs = rspxy.fetchall()
                if rs is not None:
                    return [ (e[0], e[1]) for e in rs ]
                else:
                    return []
            except:
                raise

    def delete_one_file(self, filecode : str) -> str:
        del_filename = self.check_one_code(filecode)

        with self.db.connect() as conn:
            try:
                conn.execute(text("""DELETE FROM privu_files
                                           WHERE filecode = :filecode """),
                             {"filecode": filecode})
            except:
                raise

        return del_filename



class User(flask_login.UserMixin):
    pass

