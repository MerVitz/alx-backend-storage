#!/usr/bin/env python3
"""
Module to find schools by topic in MongoDB collection.
"""

def schools_by_topic(mongo_collection, topic):
    """
    Find schools having a specific topic.

    Args:
        mongo_collection: pymongo collection object.
        topic (str): Topic to search for.

    Returns:
        List of schools with the given topic.
    """
    return list(mongo_collection.find({ "topics": topic }))

