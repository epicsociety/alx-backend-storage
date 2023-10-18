#!/usr/bin/env python3
""" inserts a new document in a collection """


def insert_school(mongo_collection, **kwargs):
    """
    Args: mongo_collection - pymongo collection object
    Return: new _id
    """

    new_document = mongo_collection.insert_one(kwargs)
    return new_document.inserted_id
