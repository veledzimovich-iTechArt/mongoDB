#!/usr/bin/env python3

# python3 -m venv venv-mongo
# . venv-mongo/bin/activate
# python3 -m pip install --upgrade pip
# python3 -m pip install pymongo python-dotenv

# useful packages
# PyMongoArrow
# Motor

import os
import pprint

import bson

from dotenv import load_dotenv

import pymongo


load_dotenv()

MONGO_DB_URI = os.environ['MONGO_DB_URI']

# set a 5-second connection timeout
client = pymongo.MongoClient(
    MONGO_DB_URI, serverSelectionTimeoutMS=5000
)

try:
    print(client.get_database())
    print(client.server_info())

    for db_name in client.list_database_names():
        print(db_name)
except Exception:
    print("Unable to connect to the server.")

db = client.games
sales_collection = db.sales

# BSON is dict
# ObjectID, Int64, Decimal128, regex
new_game = {
    'Name': 'Game',
    'Platform': 'New',
    'Year_of_Release': '2023',
    'Genre': 'Genre',
    'Publisher': 'I',
    'NA_Sales': 1.0,
    'EU_Sales': 1.0,
    'JP_Sales': 1.0,
    'Other_Sales': 1.0,
    'Global_Sales': 4.0,
    'Critic_Score': 0.0,
    'Critic_Count': 0,
    'User_Score': 1.0,
    'User_Count': 1,
    'Developer': 'Me'
}

# Insert

# insert_one

# auto generate ObjectID
# result = sales_collection.insert_one(new_game)
# document_id = result.inserted_id
# print(f'_id: {document_id}')


new_games = [
    {
        'Name': 'Game1',
        'Platform': 'New',
        'Year_of_Release': '2023',
        'Genre': 'Genre',
        'Publisher': 'I',
        'NA_Sales': 1.0,
        'EU_Sales': 1.0,
        'JP_Sales': 1.0,
        'Other_Sales': 1.0,
        'Global_Sales': 4.0,
        'Critic_Score': 0.0,
        'Critic_Count': 0,
        'User_Score': 1.0,
        'User_Count': 1,
        'Developer': 'Me'
    },
    {
        'Name': 'Game2',
        'Platform': 'New',
        'Year_of_Release': '2023',
        'Genre': 'Genre',
        'Publisher': 'I',
        'NA_Sales': 1.0,
        'EU_Sales': 1.0,
        'JP_Sales': 1.0,
        'Other_Sales': 1.0,
        'Global_Sales': 4.0,
        'Critic_Score': 0.0,
        'Critic_Count': 0,
        'User_Score': 1.0,
        'User_Count': 1,
        'Developer': 'Me'
    }
]

# insert_many

result = sales_collection.insert_many(new_games)
document_ids = result.inserted_ids
print(f'_ids: {document_ids}')


# Find

# find_one
document_to_find = {'_id': bson.ObjectId('6413335d450f4cc00c96ec29')}
result = sales_collection.find_one(document_to_find)
pprint.pprint(result)
print()

# find
documents_to_find = {'Global_Sales': {"$gt": bson.Decimal128('60')}}
# return cursor
cursor = sales_collection.find(documents_to_find)

num_docs = 0
for document in cursor:
    num_docs += 1
    pprint.pprint(document)
    print()
print(f'Documents: {num_docs}')

# Update

# update_one
document_to_update = {'_id': bson.ObjectId('64133f252966c4ed85a0288e')}

add_global_sales = {
    '$inc': {'Global_Sales': 1, 'NA_Sales': 1},
    '$set': {
        'Name': 'Game1 Updated',
    }
}
pprint.pprint(sales_collection.find_one(document_to_update))

result = sales_collection.update_one(
    document_to_update,
    add_global_sales
)

print(f'Documents modified: {result.modified_count}')


# update_many

documents_to_update = {'Name': {'$in': ['Game1', 'Game2']}}
add_global_sales = {
    '$inc': {'Global_Sales': 1, 'NA_Sales': 1},
    '$set': {
        'Name': 'Game2 Updated',
    }
}

result = sales_collection.update_many(
    documents_to_update,
    add_global_sales
)
print(f'Documents mathed: {result.matched_count}')
print(f'Documents updated: {result.modified_count}')

# Delete

# delete_one

# delete first
# delete_one({})
document_to_delete = {
    'Name': {'$in': ['Game2 Updated']}
}

pprint.pprint(sales_collection.find_one(document_to_delete))

result = sales_collection.delete_one(document_to_delete)

pprint.pprint(sales_collection.find_one(document_to_delete))

print(f'Document deleted: {result.deleted_count}')

# delete_many

# delete all
# delete_many({})
documents_to_delete = {
    'Name': {'$in': ['Game2 Updated']}
}
result = sales_collection.delete_many(documents_to_delete)

print(f'Documents deleted: {result.deleted_count}')

# Transactions


def callback(
    session,
    game_id_sender=None,
    game_id_receiver=None,
    amount=None
):
    sales_collection = session.client.games.sales

    sales_collection.update_one(
        {'_id': game_id_sender},
        {
            '$inc': {'Global_Sales': -amount, 'NA_Sales': -amount}
        },
        session=session
    )

    sales_collection.update_one(
        {'_id': game_id_receiver},
        {
            '$inc': {'Global_Sales': amount, 'NA_Sales': amount}
        },
        session=session
    )

    print('Transaction successful')

    return

# use lambda


def callback_wrapper(s):
    callback(
        s,
        game_id_sender=bson.ObjectId('64133f252966c4ed85a0288e'),
        game_id_receiver=bson.ObjectId('6413335d450f4cc00c96ec29'),
        amount=1
    )


# Update Game togehter with Game1 Updated
with client.start_session() as session:
    session.with_transaction(callback_wrapper)

print('Game')
pprint.pprint(sales_collection.find_one(document_to_find))
print('Game1 Updated')
pprint.pprint(sales_collection.find_one(document_to_update))
print()


# Aggregation

select_by_global_sales = {'$match': {'Global_Sales': {'$gt': 10}}}

separate_by_publisher_avg_global_sales = {
    '$group': {
        '_id': '$Publisher',
        'avg_global_sales': {'$avg': '$Global_Sales'}
    }
}
pipeline = [
    select_by_global_sales,
    separate_by_publisher_avg_global_sales
]

results = sales_collection.aggregate(pipeline)
print(
    'Average Global_Sales for Games with Global_Sales greater 10'
)

for document in results:
    pprint.pprint(document)
print()

select_by_critic_score = {
    '$match': {'Genre': 'Strategy', 'Critic_Score': {'$gt': 90}}
}

organize_by_critic_score = {'$sort': {'Critic_Score': -1}}

return_with_total_score = {
    '$project': {
        'Name': 1,
        'Genre': 1,
        'Critic_Score': 1,
        'User_Score': 1,
        'Total Score': {
            '$divide': [
                {
                    '$add': [
                        '$User_Score',
                        {
                            '$divide': ['$Critic_Score', 10]
                        }
                    ]
                },
                2
            ]
        }
    }
}

pipeline = [
    select_by_critic_score,
    organize_by_critic_score,
    return_with_total_score
]

results = sales_collection.aggregate(pipeline)
print('Total Score')
for document in results:
    pprint.pprint(document)
print()


# $unwind
# When the operand does not resolve to an array, but is not missing, null, or an empty array, $unwind treats the operand as a single element array.
results = sales_collection.aggregate(
    [
        {'$sort': {"Global_Sales": -1}},
        {'$limit': 2},
        {'$unwind': "$Publisher"},
    ]
)
for document in results:
    pprint.pprint(document)
print()
results = sales_collection.aggregate(
    [
        {'$sort': {"Global_Sales": -1}},
        {'$limit': 2},
        {'$set': {
            'Stores': ["NA", "JP", "EU"]
        }
        },
        {'$unwind': {
            'path': "$Stores",
            'includeArrayIndex': "arrayIndex"}
         },
    ]
)
for document in results:
    pprint.pprint(document)
print()

# $bucket limit of 100 megabytes of RAM
# Categorizes incoming documents into groups, called buckets, based on a specified expression and bucket boundaries and outputs a document per each bucket.
results = sales_collection.aggregate(
    [
        {
            '$bucket': {
                'groupBy': "$Year_of_Release",
                'boundaries': [
                    '1996', '2000', '2008', '2010', '2013', '2014', '2016', '2017'
                ],
                'default': "Other",
                'output': {
                    "count": {'$sum': 1},
                    "artists":
                    {
                        '$push': {
                            "name": {
                                '$concat': ["$Name", " ", "$Genre"]
                            },
                            "year_born": "$Year_of_Release"
                        }
                    }
                }
            }
        },
        {
            '$match': {'count': {'$gt': 1000}}
        },
    ]
)
for document in results:
    pprint.pprint(document)
print()

client.close()
