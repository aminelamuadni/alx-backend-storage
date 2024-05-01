#!/usr/bin/env python3
""" Module to find top students by average score in MongoDB """

from pymongo import MongoClient


def top_students(mongo_collection):
    """ Returns all students sorted by average score.
    Args:
        mongo_collection: A PyMongo collection instance.
    Returns:
        A list of students with their average scores, sorted from highest to
        lowest.
    """
    pipeline = [
        {
            "$unwind": "$topics"
        },
        {
            "$group": {
                "_id": "$_id",
                "name": {"$first": "$name"},
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {
            "$sort": {"averageScore": -1}
        }
    ]
    results = list(mongo_collection.aggregate(pipeline))
    return results


if __name__ == "__main__":
    # Example usage
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.my_db
    students_collection = db.students
    top_students_list = top_students(students_collection)
    for student in top_students_list:
        print("[{}] {} => {}".format(student.get('_id'), student.get('name'),
                                     student.get('averageScore')))
