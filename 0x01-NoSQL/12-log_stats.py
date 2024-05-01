#!/usr/bin/env python3
""" Module to provide statistics about Nginx logs stored in MongoDB """

from pymongo import MongoClient


def log_stats():
    """ Prints stats about Nginx logs stored in MongoDB """
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    nginx_collection = db.nginx

    # Total logs count
    logs_count = nginx_collection.estimated_document_count({})
    print(f"{logs_count} logs")

    # Counts by method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        count = nginx_collection.count_documents({"method": method})
        print(f"    method {method}: {count}")

    # Count documents with method GET and path "/status"
    status_count = nginx_collection.count_documents({
        "method": "GET",
        "path": "/status"
        })
    print(f"{status_count} status check")


if __name__ == "__main__":
    log_stats()
