#!/usr/bin/env python3
"""
Module to provide statistics about Nginx logs stored in MongoDB.

This script connects to a MongoDB database, accesses a collection of Nginx
logs, and prints statistics about the logs, including the total number of logs
and counts of different HTTP methods used. It also provides a count of logs
where the method is 'GET' and the path is '/status'.
"""

from pymongo import MongoClient


def log_stats(nginx_collection):
    """
    Print statistics about Nginx logs from a MongoDB collection.

    Args:
    nginx_collection (MongoClient): A PyMongo collection instance.

    Outputs:
    Prints the total number of logs, breakdowns by HTTP methods, and
    the number of logs accessing the '/status' path using GET.
    """
    # Total number of logs
    logs_count = nginx_collection.estimated_document_count()
    print(f"{logs_count} logs")

    # Counts by HTTP method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        count = nginx_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    # Count of GET requests to '/status'
    status_count = nginx_collection.count_documents({
        "method": "GET",
        "path": "/status"
        })
    print(f"{status_count} status check")


if __name__ == "__main__":
    # Connect to the MongoDB database
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    nginx_collection = db.nginx

    # Call the function to print log statistics
    log_stats(nginx_collection)
