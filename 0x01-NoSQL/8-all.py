#!/usr/bin/env python3

""" list documents from mongod"""


def list_all(mongo_collection):
    """
    Lists all documents in the collection
    Args: mongo_collection
    Return: [] if no document
    """
    documents_list = mongo_collection.find()
    return documents_list
