#!/usr/bin/env python3
"""
Module to provide statistics about Nginx logs stored in MongoDB with top IP
stats.

This script connects to the MongoDB, accesses the nginx collection within the
logs database, and displays various statistics including the number of logs,
method usage counts, count of GET requests to '/status', and the top 10 most
frequent IP addresses.
"""

from pymongo import MongoClient


def log_stats(nginx_collection):
    """
    Prints enhanced stats about Nginx logs stored in MongoDB, including top 10
    IPs.

    Args:
        nginx_collection (Collection): A PyMongo collection object from the
        'nginx' collection.

    Outputs:
        Prints total log count, counts by HTTP method, count of GET requests to
        '/status', and the top 10 most frequent IP addresses.
    """
    # Total logs count
    logs_count = nginx_collection.count_documents({})
    print('{} logs'.format(logs_count))

    # Counts by method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        count = len(list(nginx_collection.count_documents({"method": method})))
        print('\tmethod {}: {}'.format(method, count))

    # Count of GET requests to '/status'
    status_count = len(list(nginx_collection.count_documents({
        "method": "GET",
        "path": "/status"
        })))
    print('{} status check'.format(status_count))

    # Top 10 IPs
    ip_pipeline = [
            {
                '$group': {'_id': "$ip", 'count': {'$sum': 1}}
            },
            {
                '$sort': {'count': -1}
            },
            {
                '$limit': 10
            },
        ]
    top_ips = list(nginx_collection.aggregate(ip_pipeline))
    print("IPs:")
    for ip in top_ips:
        print('\t{}: {}'.format(ip['_id'], ip['count']))


if __name__ == "__main__":
    # Connect to the MongoDB instance
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    nginx_collection = db.nginx

    # Execute the statistics logging function
    log_stats(nginx_collection)
