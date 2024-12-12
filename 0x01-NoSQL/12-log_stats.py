#!/usr/bin/env python3
"""
Script to provide stats about Nginx logs stored in MongoDB.
"""
from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    collection = client.logs.nginx

    log_count = collection.count_documents({})
    print(f"{log_count} logs")

    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = collection.count_documents({'method': method})
        print(f"\tmethod {method}: {count}")

    status_check = collection.count_documents({'method': 'GET', 'path': '/status'})
    print(f"{status_check} status check")

    print("IPs:")
    top_ips = collection.aggregate([
        {
            '$group': {
                '_id': '$ip',
                'count': {'$sum': 1}
            }
        },
        {
            '$sort': {'count': -1}
        },
        {
            '$limit': 10
        }
    ])
    for ip in top_ips:
        print(f"\t{ip['_id']}: {ip['count']}")

