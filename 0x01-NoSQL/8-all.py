#!/usr/bin/env python3

'"""
 My comment

'"""


def list_all(mongo_collection):
    """List all documents in a MongoDB collection"""
    return list(mongo_collection.find()) if mongo_collection else []

