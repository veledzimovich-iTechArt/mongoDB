## MongoDB

#### [MongoDB Python Developer Path](https://learn.mongodb.com/learn/learning-path/mongodb-python-developer-path)


# Accessed together - stored together

# Content

[Overview](#Overview)

[Features](#Features)

[Data Model](#Data-Model)

[Relationship](#Relationship)

[Optimization](#Optimization)

[Connections](#Connections)

[Insert](#Insert)

[Find](#Find)

[Replace](#Replace)

[Update](#Update)

[Delete](#Delete)

[Query](#Query)

[Count](#Count)

[Aggregation](#Aggregation)

[Database Indexes](#Database-Indexes)

[ACID Transactions](#ACID-Transactions)

[Atlas Search](#Atlas-Search)

### Overview

Atlas - Replica Set (Group servers)

Shared Cluster (Free)
Serverless Instances (scale on demand)
Dedicated Cluster

General Purpouse Document Database (like JSON)

```bash
db.help()
db.getName()
```

### Features

Document (16MB)
Collection of Documents
Database container for Collections

MongoDB is a Core of Atlas
Atlas (Visualization, Full Text Search)

Displayed JSON
Stored BSON (dates, numbers, Object, ObjectID)

Every document has ObjectID (unique identifier)
```js
{
  "_id": 1,
  "name": "AC3 Phone",
  "colors" : ["black", "silver"],
  "price" : 200,
  "available" : true
}
```
Flexible Schema (diff structure for docs)
Polymorphic data
Schema Validation (optional)


### Data Model

Data Model (stored, query and use resources optimally)
- easy to manage
- faster queries
- less memory
- less CPU
- reduce costs

Embeding 16 MB
+ single read query, sinlge update/delete
- duplicates, large/unbounded documents, no paggination

Linking (referencies)
+ no duplicates, small documents
- complex query, many read queries


### Relationship

#### one-to-one 1:1

In the one to one relationship Embedding is the preferred way to model the relationship as it’s more efficient to retrieve the document.

- embeding
```js
{
  name: "Peter Wilkinson",
  age: 27,
  address: {
    street: "100 some road",
    city: "Nevermore"
  }
}
```
- linking
```js
{
  _id: 1,
  name: "Peter Wilkinson",
  age: 27
}
// foreign key
{
  user_id: 1,
  street: "100 some road",
  city: "Nevermore"
}

```
#### one-to-many 1:N
- embeding
```js
{
  title: "An awesome blog",
  url: "http://awesomeblog.com",
  text: "This is an awesome blog we have just started",
  comments: [{
    name: "Peter Critic",
    created_on: ISODate("2014-01-01T10:01:22Z"),
    comment: "Awesome blog post"
  }, {
    name: "John Page",
    created_on: ISODate("2014-01-01T11:01:22Z"),
    comment: "Not so awesome blog"
  }]
}
```
- linking
```js
{
  _id: 1,
  title: "An awesome blog",
  url: "http://awesomeblog.com",
  text: "This is an awesome blog we have just started"
}
// foreign key
{
  blog_entry_id: 1,
  name: "Peter Critic",
  created_on: ISODate("2014-01-01T10:01:22Z"),
  comment: "Awesome blog post"
}
// foreign key
{
  blog_entry_id: 1,
  name: "John Page",
  created_on: ISODate("2014-01-01T11:01:22Z"),
  comment: "Not so awesome blog"
}
```
- bucketing

The main benefit of using buckets in this case is that we can perform a single read to fetch 50 comments at a time, allowing for efficient pagination.

Bucketing data by hours, days or number of entries on a page.
```js
{
  _id: 1,
  title: "An awesome blog",
  url: "http://awesomeblog.com",
  text: "This is an awesome blog we have just started"
}
// foreign key
{
  blog_entry_id: 1,
  page: 1,
  count: 50,
  comments: [{
    name: "Peter Critic",
    created_on: ISODate("2014-01-01T10:01:22Z"),
    comment: "Awesome blog post"
  }, ...]
}
{
  blog_entry_id: 1,
  page: 2,
  count: 1,
  comments: [{
    name: "John Page",
    created_on: ISODate("2014-01-01T11:01:22Z"),
    comment: "Not so awesome blog"
  }]
}
```
#### many-to-many N:M

Establish the maximum size of N and the size of M. For example if N is a maximum of 3 categories for a book and M is a maximum of 500000 books in a category you should pick One Way Embedding. If N is a maximum of 3 and M is a maximum of 5 then Two Way Embedding might work well.

- embeding (two way)
```js
// authors
{
  _id: 1,
  name: "Peter Standford",
  books: [1, 2]
}
{
  _id: 2,
  name: "Georg Peterson",
  books: [2]
}
// books
{
  _id: 1,
  title: "A tale of two people",
  categories: ["drama"],
  authors: [1, 2]
}
{
  _id: 2,
  title: "A tale of two space ships",
  categories: ["scifi"],
  authors: [1]
}
```
- embeding (one way)
```js
// category
{
  _id: 1,
  name: "drama"
}
// books
{
  _id: 1,
  title: "A tale of two people",
  categories: [1],
  authors: [1, 2]
}
```

### Optimization

Scalable
- avoid unbounded
- use projections
- $match as early as possible (use indexes)
- indexes

Anti-patterns
- massive arrays
- massive number of collections
- queries without indexes
- unnecessary indexes
- data that accesed together but stored in diff collections

Data Explorer
Indexes
Schema Anti-Patterns
Perfomance Advisor (> M10)


### Connections

MongoDB drivers connect our app to our database using a connection string

Connection string (Shell, Compas, Any App)
- Standart (standalone cluster, replica sets, shader cluster)
- DNS Seed list (change servers without reconfiguration)

Connect your Application
```bash
mongodb+srv://admin:<password>@<cluster>/?retryWrites=true&w=majority
```

Connect with MongoDB Shell (install mongosh)
```bash
mongosh --help
mongosh --host
# Default DB myFirstDatabase
mongosh "mongodb+srv://<cluster>/games" --apiVersion 1 --username admin
```
```js
const gteetingArray = ["hello", "world", "welcome"];
const loopArray = (array) => array.forEach(el => console.log(el));
loopArray(gteetingArray);
```

MongoDB Compass (GUI)
- Query Data
- Compose Aggregation Pipeline
- Analyze Data
```bash
mongodb+srv://admin:<password>@<cluster>/test
```
MongoDB VSCode
```bash
mongodb+srv://admin:<password>@<cluster>/test
```

Common Errors
Network Access
- check ip address (Network Access -> Add IP address)

User authentication
- password


### Collections
```js
// list
show collections
// rename
db.sales_cloned.renameCollection('sales_indexed')
```

### Insert

insertOne()
```js
db.sales.insertOne({
  Name: 'Example',
  Platform: 'New',
  Year_of_Release: '2023',
  Genre: 'Example',
  Publisher: 'I',
  NA_Sales: 1.0,
  EU_Sales: 1.0,
  JP_Sales: 1.0,
  Other_Sales: 1.0,
  Global_Sales: 4.0,
  Critic_Score: 0.0,
  Critic_Count: 0,
  User_Score: 1.0,
  User_Count: 1,
  Developer: 'Me',
  Reviews: [
    {
        Web_Page: 'www.webpage.com',
        Author: 'Author',
        Year: 2012
    },
    {
        Web_Pag: 'www.page.com',
        Author: 'Other Author',
        Year: 2013
    }
  ],
  Stores: ['NA']
})
```
insertMany()
```js
db.sales.insertMany([
  {
    Name: 'Example1',
    Platform: 'New',
    Year_of_Release: '2023',
    Genre: 'Example',
    Publisher: 'I',
    NA_Sales: 1.0,
    EU_Sales: 1.0,
    JP_Sales: 1.0,
    Other_Sales: 1.0,
    Global_Sales: 4.0,
    Critic_Score: 0.0,
    Critic_Count: 0,
    User_Score: 1.0,
    User_Count: 1,
    Developer: 'Me',
    Reviews: [
      {
          Web_Page: 'www.webpage.com',
          Author: 'Author',
          Year: 2013
      },
      {
          Web_Page: 'www.page.com',
          Author: 'Other Author',
          Year: 2014
      }
    ],
    Stores: ['NA', 'JP']
  },
  {
    Name: 'Example2',
    Platform: 'New',
    Year_of_Release: '2023',
    Genre: 'Example',
    Publisher: 'I',
    NA_Sales: 1.0,
    EU_Sales: 1.0,
    JP_Sales: 1.0,
    Other_Sales: 1.0,
    Global_Sales: 4.0,
    Critic_Score: 0.0,
    Critic_Count: 0,
    User_Score: 1.0,
    User_Count: 1,
    Developer: 'Me',
    Reviews: [
      {
          Web_Page: 'www.webpage.com',
          Author: 'Author',
          Year: 2022
      },
      {
          Web_Page: 'www.page.com',
          Author: 'Other Author',
          Year: 2033
      }
    ],
    Stores: ['NA', 'JP', 'EU']
  }
])
```

### Find
```js
db.sales.findOne()
db.sales.find()
# it
db.sales.find().toArray()
```

$eq
```js
db.sales.find( {Genre: "Shooter"})
db.sales.find( {Genre: {$eq: "Shooter"}})
db.sales.find({_id: ObjectId("6413248b9a3bb8e8856e9c87")})
```
$in select all documents that have field value specify in array
```js
db.sales.find({ Publisher: { $in: ["Electronic Arts", "Activision"] } })
```
$gt
```js
db.sales.find({"Global_Sales": {$gt: 50}})
```
$lt
```js
db.sales.find({"Global_Sales": {$lt: 0.01}})
```
$lte
```js
db.sales.find({"User_Score": {$lte: 2}})
```
$gte
```js
db.sales.find({"User_Score": {$gte: 9.6}})
```
$elemMatch
find in Array of objects
```js
db.sales.find({
    Stores: {
        $elemMatch: {$eq: "NA"}
    }
})
# find in Array
db.sales.find({ Stores: "EU" })
```
```js
db.sales.find({
    Reviews: {
        $elemMatch: {
            Web_Page: "www.webpage.com",
            Year: {$gte: 2014},
            Author: {$eq: 'Author'},
        }
    }
})
```
$and
```js
db.sales.find({
    $and: [
        { "Reviews.Author": "Other Author", User_Count: { $gte: 1 } }
    ]
})
# implicit $and
db.sales.find(
    { "Reviews.Author": "Other Author", User_Count: { $gte: 1 } }
)
```
$or
```js
db.sales.find({
  $or: [{ Publisher: "Nintendo" }, { Publisher: "Sega" }],
})
```
$and $or
```js
db.sales.find({
  $and: [
    { $or: [{ Publisher: "I" }, { Developer: "Me" }] },
    { $or: [
        { "Reviews.Web_Page": "www.webpage.com" },
        { Year_of_Release: '2023' }] },
  ]
})
```

### Replace

replaceOne
```js
// first
db.sales.replaceOne(
  {},
  {"Name":"Wii Sports Modified","Platform":"Wii","Year_of_Release":"2006","Genre":"Sports","Publisher":"Nintendo","NA_Sales":{"$numberDecimal":"41.36"},"EU_Sales":{"$numberDecimal":"28.96"},"JP_Sales":{"$numberDecimal":"3.77"},"Other_Sales":{"$numberDecimal":"8.45"},"Global_Sales":{"$numberDecimal":"82.53"},"Critic_Score":{"$numberDouble":"76.0"},"Critic_Count":{"$numberInt":"51"},"User_Score":{"$numberDouble":"8.0"},"User_Count":{"$numberInt":"322"},"Developer":"Nintendo"}
)
// by _id
db.sales.replaceOne(
  {
    _id: ObjectId("641829b1cf6764ccb159a248"),
  },
  {
    Name: 'Example2 Modified',
    Platform: 'New',
    Year_of_Release: '2023',
    Genre: 'Example',
    Publisher: 'I',
    NA_Sales: 1.0,
    EU_Sales: 1.0,
    JP_Sales: 1.0,
    Other_Sales: 1.0,
    Global_Sales: 4.0,
    Critic_Score: 0.0,
    Critic_Count: 0,
    User_Score: 1.0,
    User_Count: 1,
    Developer: 'Me',
    Reviews: [
      {
          Web_Page: 'www.webpage.com',
          Author: 'Author',
          Year: 2022
      },
      {
          Web_Page: 'www.page.com',
          Author: 'Other Author',
          Year: 2033
      }
    ],
    Stores: ['NA', 'JP', 'EU']
  }
)
db.sales.findOne({_id: ObjectId("641829b1cf6764ccb159a248")})
```

### Update

updateOne

$set adds new field and values or replace value
```js
db.sales.updateOne(
  {
    _id: ObjectId("641829b1cf6764ccb159a247"),
  },

  {
    $set: {
      Name: 'Example1 Modified',
    },
  }
)
```
$push appends value to an array or adds the array field with value
```js
db.sales.updateOne(
  { _id: ObjectId("641829b1cf6764ccb159a247") },
  { $push: { Stores: "EU" } }
)
```
upsert insert a document with provided information if matching don't exist
```js
db.sales.updateOne(
  { Name: "Example2" },
  { $set: {
    Name: 'Example2',
    Platform: 'New',
    Year_of_Release: '2023',
    Genre: 'Example',
    Publisher: 'I',
    NA_Sales: 1.0,
    EU_Sales: 1.0,
    JP_Sales: 1.0,
    Other_Sales: 1.0,
    Global_Sales: 4.0,
    Critic_Score: 0.0,
    Critic_Count: 0,
    User_Score: 1.0,
    User_Count: 1,
    Developer: 'Me',
    Reviews: [
      {
          Web_Page: 'www.webpage.com',
          Author: 'Author',
          Year: 2022
      },
      {
          Web_Page: 'www.page.com',
          Author: 'Other Author',
          Year: 2033
      }
    ],
    Stores: []
    },
  },
  { upsert: true }
)
```

$each
```js
db.sales.updateOne(
  {
    _id: ObjectId("64182999cf6764ccb159a246")
  },
  {
    $push: {
      Stores: {$each: ["JP", "EU"]}
    }
  }
)
```
$inc
```js
db.sales.updateOne(
  {
    Name: "Example2"
  },
  {
    $set: {
      last_updated: new Date()
    },
    $inc: {User_Score: 1}
  },
  { upsert: true }
)
```
$unset
```js
db.sales.updateOne(
  {
    Name: "Example2"
  },
  {
    $unset: {
      last_updated: new Date()
    }
  }
)
```
updateMany
- could update some
- no roll back
- not for transactions
```js
db.sales.updateMany(
  { "Reviews.Year": { $gte: 2022 } },
  { $set: { User_Score: 3 } }
)
db.sales.updateMany(
  {
    Name: { $in: [
      "Example", "Example1 Modified", "Example2 Modified", "Example2"] }
  },
  {
    $set: {last_seen: ISODate("2022-01-01")}
  },
  {upsert: true}
)
```
findAndModify
```js
db.sales.findAndModify(
  {
    query: { _id: ObjectId("64182999cf6764ccb159a246") },
    update: { $inc: { User_Score: 5 } },
    // new returns modified document
    new: true,
    upsert: true
  }
)
```

### Delete
deleteOne
```js
// delete first
db.sales.deleteOne({})
db.sales.findOneAndDelete(
  {_id: ObjectId("64182e69c229c5d3972721d0")}
)
db.sales.deleteOne({_id: ObjectId("64182e69c229c5d3972721d0")})
```
deleteMany
```js
db.sales.insertOne({
  Name: 'Example to Delete',
  Platform: 'New',
  Year_of_Release: '2023',
  Genre: 'Delete',
  Publisher: 'I',
  NA_Sales: 1.0,
  EU_Sales: 1.0,
  JP_Sales: 1.0,
  Other_Sales: 1.0,
  Global_Sales: 4.0,
  Critic_Score: 0.0,
  Critic_Count: 0,
  User_Score: 1.0,
  User_Count: 1,
  Developer: 'Me',
  Reviews: [
    {
        Web_Page: 'www.webpage.com',
        Author: 'Author',
        Year: 2010
    },
    {
        Web_Pag: 'www.page.com',
        Author: 'Other Author',
        Year: 2013
    }
  ],
  Stores: ['NA']
});
// delete all
db.sales.deleteMany({});
db.sales.deleteMany({'Reviews.Year': {$lte: 2010}});
db.sales.deleteMany({Genre: 'Delete'});
```

### Query
cursor is a pointer to the result of a query
find() returns cursor
cursor.sort()
```js
// asc 1
db.sales.find({Genre: "Strategy"}).sort({Name: 1});
// desc -1
// _id 1 include a field that contains unique values in the sort
db.sales.find(
  {Publisher: "Microsoft Game Studios"}
).sort({Genre: 1, _id: 1});
```
cursor.limit()
```js
db.sales.find(
  { Genre: "Strategy" }
).sort({ Global_Sales: -1, _id: 1 }).limit(3);
db.sales.find(
    {
      Platform: {$in: ["PC", "XB"]},
      Year_of_Release: {$gt: "2000"}
    }
  ).sort({Global_Sales: -1}).limit(3);
```

projection
```js
// include 1
db.sales.find({}, {Global_Sales: 1}).sort({Global_Sales: 1})
db.sales.find(
    {
      Platform: "NES"
    },
    { Name: 1, Global_Sales: 1, Publisher: 1}
);
// exclude 0
db.sales.find({
      Platform: {$in: ["NES","NES64"]}
    },
    {
      NA_Sales: 0,
      JP_Sales: 0,
      EU_Sales: 0,
      Other_Sales: 0,
      Developer: 0
    }
);
// force exclude _id
db.sales.find({
      Year_of_Release: {$gt: '2010'},
      Critic_Score: {$gt: 80}
    },
    {
      _id: 0,
      Name: 1,
      Genre: 1,
      Year_of_Release: 1,
      Critic_Score: 1,
      Publisher: 1
    }
);
```

### Count
```js
// all
db.sales.countDocuments({});
db.sales.countDocuments({ Genre: "Strategy", Platform: "PC" });
db.sales.countDocuments(
  {
    Reviews: {
      $elemMatch: {
        Author: "Author",
        Year: {$gt: 2013}
      }
    }
  }
);
```

### Aggregation
Aggregate (collect and summary data)
Stage (built-in methods that can be completed on the data)
$match $group $sort $limit
Pipeline (series of stages completed on the data in order)

$match (as early as possible)
```js
db.sales.aggregate(
  [
    {$match: {
      Publisher: "Nintendo"}
    }
  ]
);
```
match not null
```js
db.sales.aggregate(
  [
    {
      $match: {$and: [
          {User_Score: {$ne: null}},
          {Critic_Score: {$ne: null}}
        ]
      }
    }
  ]
)
````
$group
```js
db.sales.aggregate(
  [
    {$match: {
      Publisher: "Nintendo"}
    },
    {
      $group: {
        // alias
        _id: "$Genre",
        number_of_games: {$count: {}}
      }
    }
  ]
);
```
$sort (order of stages is important)
```js
db.sales.aggregate(
  [
    {$match: {
      Publisher: "Nintendo"}
    },
    {
      $group: {
        // alias
        _id: "$Genre",
        number_of_games: {$count: {}}
      }
    },
    // {$sort: {number_of_games: -1}}
    {$sort: {_id: -1}}
  ]
)
```
$limit
```js
db.sales.aggregate(
  [
    {$match: {
      Genre: "Example"}
    },
    {$sort: {
        "Stores.0": -1, User_Score: -1
      }
    },
    {$limit:  3}
  ]
);
```
$project (specify output, create or change the value of fields)
```js
db.sales.aggregate(
  [
    {
      $project: {
          _id: 0,
          clone_name: "$Name",
          Year_of_Release: 1,
          Publisher: 1,
          new_field: "new_field",
      }
    }
  ]
);

```
$set (new fields or changes the value of existing fields)
```js
db.sales.aggregate(
  [
    {$match: {
      Year_of_Release: {$lte: '2000'}}
    },
    {
      $set: {
        class: "XX century game"
      }
    }
  ]
);
db.sales.aggregate(
  [
    {$match: {$and: [
          {User_Score: {$gte: 1}},
          {Critic_Score: {$gte: 1}}
        ]
      }
    },
    {
      $set: {
          Web_Title: {
              $concat: ["$Name","|","$Year_of_Release", "|", "$Genre"]
          }
       }
    },
    {
      $project: {
        Web_Title: 1,
        User_Score: 1,
        Critic_Score: 1,
        Total_Score: {
          $divide: [
            {
              $add: [
                  '$User_Score',
                  {
                      $divide: ['$Critic_Score', 10]
                  }
              ]
            },
            2
          ]
        }
      }
    }
  ]
);
```
$count (creates a new document)
```js
db.sales.aggregate(
  [
    {
      $match: {
        Publisher: "Nintendo",
        Year_of_Release: {
          $gte: "2016",
          $lte: "2018"
        }
      }
    },
    {
      $count: "nintendo_sales_2017"
    }
  ]
);
```
$out (!!!new collection or replace existing!!!)
```js
db.sales.aggregate(
  [
    {
      $match: {
        Publisher: "Sega",
        Year_of_Release: {
          $gte: "2017",
          $lte: "2019"
        }
      },
    },
    {
      $out: "sega_sales_2018"
    }
  ]
);
```

### Database Indexes (imporve query performance at the cost of write perfomance cost)
- special data structure
- store small portion of data
- ordered and easy to search efficiently
- euqlity and range based query
- sorted result

- hide index before delete

Index types
- single field
- compound (avoid in memmory sort)
- multikey (include one array field)

single field
```js
db.sales.createIndex(
  {
    Name: 1
  }
)
```
```js
db.sales.getIndexes()
```
Use explain() in a collection when running a query to see the Execution plan. A winningPlan is a document that contains information about the query and the method that was used to execute the query.

- The IXSCAN stage indicates the query is using an index and what index is being selected.
- The COLLSCAN stage indicates a collection scan is perform, not using any indexes.
- The FETCH stage indicates documents are being read from the collection.
- The SORT stage indicates documents are being sorted in memory.
```js
db.sales.explain().find(
  {
    Year_of_Release: {
        $gt: "2000"
    }
  }
).sort(
  {
    Name:1
  }
)
```
compound
Prefix field!

Order matter: Equality, Sort, and Range!
- Equality: field/s that matches on a single field value in a query
- Sort: field/s that orders the results by in a query
- Range: field/s that the query filter in a range of valid values

Cover queries!
```js
// query
db.sales.explain().find(
  {
    Year_of_Release: {$gt: "2000"},
    Platform: 'PC'
  }
).sort({
    Year_of_Release:-1,
    Name:1
  }
)
// index
// unique
db.sales.createIndex(
  {
    Platform: 1, Year_of_Release: 1, Name: 1
  },
  // {
    // unique:true
  // }
)

// An Index covers a query when MongoDB does not need to fetch the data from memory since all the required data is already returned by the index.
// By adding the projection {name:1,birthdate:1,_id:0} in the previous query, we can limit the returned fields to only name and birthdate.
// The execution plan shows only two stages:
// IXSCAN - Index scan using the compound index
// PROJECTION_COVERED - All the information needed is returned by the index, no need to fetch from memory
db.sales.explain().find(
  {
    Year_of_Release: {$gt: "2000"},
    Platform: 'PC'
  },
  {Name: 1, Year_of_Release: 1, Platform: 1, _id: 0}
).sort({
    Year_of_Release:-1,
    Name:1
  }
);
```

multikey (one array per index)
```js
// create a multikey index on the `transfers_complete` field:
db.sales.createIndex({ Stores: 1 })
db.sales.explain().find(
  { Stores: { $in: ["NA", "EU"] } }
)
```

hide indexes
```js
db.sales.getIndexes()
db.sales.hideIndex('Stores_1')
```
delete unused indexes
```js
db.sales.dropIndex({
  Publisher:1,
  Name:1
})
// one
db.sales.dropIndex('Stores_1')
// some
db.sales.dropIndexes(['Stores_1', 'Name_1'])
// all
db.sales.dropIndexes()
```


### ACID Transactions (group of DB operations that will completed as unit or not at all)
A - all operations will either succeed or fail together
C - all changes made by operations are consistent with DB constraints
I - multiple transactions can happen at the same time without affecting the outcome of the other transactions
D - all the changes are made by operations in transactions will persist, no matter what happened.

Exchange curency
Adding item to the shopping cart

- Single-document (atomic by default)

- Multi-document (wrapped as transaction, locks all documents)

Open session (1 minute)
```js
const session = db.getMongo().startSession()
session.startTransaction()
const sales = session.getDatabase('games').getCollection('sales')
sales.updateOne(
  {Name: "Example"}, {$inc: {Global_Sales: -1}}
)
sales.updateOne(
  {Name: "Example1 Modified"}, {$inc: {Global_Sales: 1}}
)
session.commitTransaction()
// abort
session.startTransaction()
sales.updateOne(
  {Name: "Example"}, {$inc: {Global_Sales: 30}}
)
session.abortTransaction()
```


### Atlas Search

Relevance-Based Search (lucene.standart)
Search indexes (how search should perform)

Search Index with Dynamic mapping (all field indexed except: booleans, objectIDs, timestamps)

Dynamic field mapping (field with equal weight)

Create manually
```js
//search_index.json
{
    "name": "game-dynamic",
    "searchAnalyzer": "lucene.standard",
    "analyzer": "lucene.standard",
    "collectionName": "sales_indexed",
    "database": "games",
    "mappings": {
        "dynamic": true
    }
}
```
```bash
atlas clusters search indexes create --clusterName Cluster0 -f /app/search_index.json
atlas clusters search indexes list --clusterName Cluster0 --db games --collection sales_indexed
mongosh -u admin -p <password> 'mongodb+srv://<cluster>/games'
```

```js
// no output because index created for collection sales_indexed
db.sales.aggregate(
  [
    {$search: {
        index: "game-dynamic",
        text: {query: "Civilization", path: { "wildcard": "*" }}
      }
    },
    {
      $set: {score: { $meta: "searchScore" }}
    }
  ]
)
db.sales_indexed.aggregate(
  [
    {$search: {
        index: "game-dynamic",
        text: {query: "Civilization", path: { "wildcard": "*" }}
      }
    },
    {
      $set: {score: { $meta: "searchScore" }}
    }
  ]
)
```
Static field mapping (field with equal weight)
Search only for mapped fields

Create manually
```json
{
  "name": "game-name-publisher-static",
  "searchAnalyzer": "lucene.standard",
  "analyzer": "lucene.standard",
  "collectionName": "sales",
  "database": "games",
  "mappings": {
    "dynamic": false,
    "fields": {
      "Name": {
        "type": "string"
      },
      "Publisher": {
        "type": "string"
      }
    }
  }
}
```
```js
db.sales.aggregate(
  [
    {$search: {
        index: "game-name-publisher-static",
        text: {query: "Action", path: { "wildcard": "*" }}
      }
    },
    {
      $set: {score: { $meta: "searchScore" }}
    }
  ]
)
// no search by Genre but search in Name
db.sales.aggregate(
  [
    {$search: {
        index: "game-name-publisher-static",
        text: {query: "Role-Playing", path: { "wildcard": "*" }}
      }
    },
    {
      $set: {score: { $meta: "searchScore" }}
    }
  ]
)
```
compound
The compound operator combines multiple search clauses to return the most relevant results and assigns weights to documents with qualities that you want to appear higher in search results.
- must
- mustNot
- should
- filter (does not impact the score given to the results)

```js
db.sales_indexed.aggregate(
  [
    {
      $search: {
        index: "game-dynamic",
        "compound": {
          "filter": [
            {
              "text": {
                "query": "Nintendo",
                "path": "Publisher"
              }
            }
          ],
          "mustNot": [
            {
              "text": {
                "query": [
                    "GB", "GBA", "WiiU", "Wii", "GC", "DS", "3DS"
                ],
                "path": "Platform"
              }
            }
          ],
          "must": [
              {
              "text": {
                "query": "Mario",
                "path": "Name",
                // The use of a constant score overwrites the calculated score search value to the define constant ('4') which can be desirable when you only care about matches for a particular clause.
                "score": {"constant": { "value": 4 } }
              }
            }
          ],
          "should": [
            {
              "text": {
                "query": "Bros",
                "path": "Name"
              }
            }
          ]
        }
      }
    },
    {
      $project: {
          "Name": 1,
          "Publisher": 1,
          "Platform": 1,
          "score": {$meta: "searchScore"}
      }
    }
  ]
)
```
facets
buckets that we group our search results

- numbers, dates, strings

```js
{
  "name": "game-genre-facet",
  "searchAnalyzer": "lucene.standard",
  "analyzer": "lucene.standard",
  "collectionName": "sales",
  "database": "games",
  "mappings": {
    "dynamic": false,
    "fields": {
      "Genre": {
        "type": "stringFacet"
      },
      "Publisher": {
        "type": "string"
      }
    }
  }
}
```

- aggregation with @searchMeta
```js
db.sales.aggregate(
  [
    {
      $searchMeta: {
        index: "game-genre-facet",
        "facet": {
          "operator": {
            "text": {
                "query": ["Nintendo"],
                "path": "Publisher"
            }
          },
          "facets": {
              "genreFacet": {
                  "type": "string",
                  "path": "Genre",
              }
          }
        }
      }
    }
  ]
)
```
