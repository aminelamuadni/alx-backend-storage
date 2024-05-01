#!/usr/bin/env python3
""" Module to insert a document in a MongoDB collection """

from pymongo import MongoClient


def insert_school(mongo_collection, **kwargs):
    """ Inserts a new document in a collection based on kwargs
    Args:
        mongo_collection: Reference to the MongoDB collection
        **kwargs: Arbitrary keyword arguments representing the document fields
    Returns:
        The new _id of the inserted document
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
