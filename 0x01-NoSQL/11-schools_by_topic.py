#!/usr/bin/env python3
"""MongoDB Find"""


def schools_by_topic(mongo_collection, topic):
    """
    Search the school based in school

        Args:
            mongo_collection: Collection
            topic: Content

        Return:
            List of schoo
    """
    return [i for i in mongo_collection.find({"topics": topic})]
