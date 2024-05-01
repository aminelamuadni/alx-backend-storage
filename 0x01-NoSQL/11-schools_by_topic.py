#!/usr/bin/env python3
""" Module to find schools with a specific topic in a MongoDB collection """

from pymongo import MongoClient


def schools_by_topic(mongo_collection, topic):
    """ Returns the list of schools having a specific topic
    Args:
        mongo_collection: Reference to the MongoDB collection
        topic (str): The topic searched for
    Returns:
        List of schools that have the specified topic
    """
    return list(mongo_collection.find({"topics": topic}))
