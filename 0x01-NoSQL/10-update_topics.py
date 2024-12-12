#!/usr/bin/env python3
"""
Module to update topics of a school in MongoDB collection.
"""

def update_topics(mongo_collection, name, topics):
    """
    Update all topics of a school document by name.

    Args:
        mongo_collection: pymongo collection object.
        name (str): School name to update.
        topics (list of str): List of topics to set.

    Returns:
        None
    """
    mongo_collection.update_many(
        { "name": name },
        { "$set": { "topics": topics } }
    )

