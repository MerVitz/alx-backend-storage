#!/usr/bin/env python3
"""
Module to insert a new document into a MongoDB collection.
"""

def insert_school(mongo_collection, **kwargs):
    """
    Insert a new document into the collection.

    Args:
        mongo_collection: pymongo collection object.
        **kwargs: key-value pairs representing the document's fields.

    Returns:
        The ID of the newly inserted document.
    """
    return mongo_collection.insert_one(kwargs).inserted_id

