#!/usr/bin/env python3
""" Insert document """
import pymongo


def insert_school(mongo_collection, **kwargs):
    
    new_school = mongo_collection.insert_one(kwargs)

    return (new_school.inserted_id)
