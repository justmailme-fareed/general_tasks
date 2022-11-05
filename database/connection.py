"""
FileName : connection.py
Description : Database Connectivity
Author : Tree Integrated services
Created Date : 30-9-2022
"""
from configuration.config import dbname
from pymongo import MongoClient
from mongoengine import *

#Mongoengine Connectivity
connect(dbname)
#Pymongo Connectivity
py_conn = MongoClient(f"mongodb://localhost:27017/{dbname}")
collection=py_conn[dbname]
