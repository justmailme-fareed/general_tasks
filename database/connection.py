"""
FileName : connection.py
Description : Database Connectivity
Author : Tree Integrated services
Created Date : 30-9-2022
"""
from configuration.config import dbname

#Mongoengine Connectivity
from mongoengine import *
connect(dbname)

#Pymongo Connectivity
from pymongo import MongoClient
py_conn = MongoClient(f"mongodb://localhost:27017/{dbname}")

