#!/usr/bin/env python3
"""Print a report of the books linked to selected authors in the bookstore database."""

import logging
import os
import sys

import pymongo
from pymongo.errors import PyMongoError

# Connection settings come from the environment (never hardcode credentials)
MONGODB_ATLAS_URL = os.getenv("MONGODB_ATLAS_URL")
MONGODB_ATLAS_USER = os.getenv("MONGODB_ATLAS_USER")
MONGODB_ATLAS_PWD = os.getenv("MONGODB_ATLAS_PWD")

# Authors to report on: two loaded authors (002, 003) and one I added (004)
AUTHOR_IDS = ["author_002", "author_003", "author_004"]

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def print_author_report(authors, books, author_ids):
    """Print the author count, then each author's name with their linked books."""
    # Count only the authors from my list that exist in the collection
    total = authors.count_documents({"_id": {"$in": author_ids}})
    print(f"Authors: {total}\n")

    for author_id in author_ids:
        # Look up the author document by its _id
        author = authors.find_one({"_id": author_id})
        if author is None:
            logging.warning("Author %s not found, skipping", author_id)
            continue

        print(author["name"])
        # Join: find every book whose author_ids list contains this author's _id
        for book in books.find({"author_ids": author["_id"]}):
            print(f"  {book['title']} ({book['published_year']})")
        print()


def main():
    """Connect to MongoDB Atlas, run the report, and always close the client."""
    # Fail early with a clear message if any setting is missing
    if not all([MONGODB_ATLAS_URL, MONGODB_ATLAS_USER, MONGODB_ATLAS_PWD]):
        logging.error("MONGODB_ATLAS_URL, MONGODB_ATLAS_USER and MONGODB_ATLAS_PWD must be set")
        sys.exit(1)

    client = None
    try:
        # Username and password are passed separately, so no URL encoding is needed
        client = pymongo.MongoClient(
            MONGODB_ATLAS_URL,
            username=MONGODB_ATLAS_USER,
            password=MONGODB_ATLAS_PWD,
            serverSelectionTimeoutMS=5000,
        )
        # Force a round trip so connection problems show up here
        client.admin.command("ping")
        logging.info("Connected to MongoDB Atlas")

        # Select the database and collections from Case Study 1
        db = client["bookstore"]
        print_author_report(db["authors"], db["books"], AUTHOR_IDS)
    except PyMongoError as err:
        logging.error("MongoDB error: %s", err)
        sys.exit(1)
    finally:
        # Close the client whether or not the report succeeded
        if client is not None:
            client.close()
            logging.info("Connection closed")


# Run main() only when this file is executed directly
if __name__ == "__main__":
    main()
