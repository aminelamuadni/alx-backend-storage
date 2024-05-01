#!/usr/bin/env python3
""" Module to update topics of a school document in a MongoDB collection """

from pymongo import MongoClient


def update_topics(mongo_collection, name, topics):
    """ Changes all topics of a school document based on the name
    Args:
        mongo_collection: Reference to the MongoDB collection
        name (str): The school name to update
        topics (list of str): List of topics approached in the school
    Returns:
        None
    """
    mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
