#!/usr/bin/env python3
""" Module to list all documents in a MongoDB collection """

from pymongo import MongoClient


def list_all(mongo_collection):
    """ Lists all documents in a collection
    Args:
        mongo_collection: Reference to the MongoDB collection
    Returns:
        List of documents, or an empty list if the collection is empty
    """
    documents = []
    try:
        # Attempt to get all documents in the collection
        documents = list(mongo_collection.find())
    except Exception as e:
        print(f"Error accessing MongoDB: {e}")
    return documents
