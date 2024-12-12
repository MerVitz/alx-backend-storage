#!/usr/bin/env python3
"""
Module to handle operations on student data in MongoDB.
"""

def top_students(mongo_collection):
    """
    Returns all students sorted by average score.
    
    Each document will include the key 'averageScore'.
    
    Args:
        mongo_collection: pymongo collection object
    
    Returns:
        List of student documents with 'averageScore' added and sorted in descending order.
    """
    pipeline = [
        {
            '$addFields': {
                'averageScore': {
                    '$avg': '$topics.score'
                }
            }
        },
        {
            '$sort': {
                'averageScore': -1
            }
        }
    ]
    return list(mongo_collection.aggregate(pipeline))


if __name__ == "__main__":
    # Example usage (remove or adapt based on testing needs)
    from pymongo import MongoClient
    
    client = MongoClient('mongodb://127.0.0.1:27017')
    students_collection = client.my_db.students
    
    for student in top_students(students_collection):
        print(f"{student.get('name')} => {student.get('averageScore')}")

