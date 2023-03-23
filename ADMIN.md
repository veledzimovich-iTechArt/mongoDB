## MongoDB Admin

#### [M103: Basic Cluster Administration](https://learn.mongodb.com/learn/course/m103-basic-cluster-administration)

# Content

[Install](#Install)

[Options](#Options)

[Run](#Run)

[Configuration file](#Configuration-file)

[Check](#Check)

[Interaction](#Interaction)

[Security](#Security)

[Tools](#Tools)

[Replication](#Replication)

[Replication Configuration Document](#Replication-Configuration-Document)

[Read Write Secondary](#Read-Write-Secondary)

[Read Preferences](#Read-Preferences)

[Write Concern Levels](#Write-Concern-Levels)

[Read Concern Levels](#Read-Concern-Levels)

[Sharding](#Sharding)


### Install
#### Intsall mongosh

```bash
curl https://downloads.mongodb.com/compass/mongosh-1.8.0-darwin-x64.zip --output mongosh-1.8.0-darwin-x64.zip
unzip mongosh-1.8.0-darwin-x64.zip
rm mongosh-1.8.0-darwin-x64.zip
sudo cp mongosh-1.8.0-darwin-x64/bin/mongosh /usr/local/bin
rm -rf mongosh-1.8.0-darwin-x64
```
#### Install mongod and mongos
```bash
curl https://fastdl.mongodb.org/osx/mongodb-macos-x86_64-6.0.5.tgz --output mongodb-macos-x86_64-6.0.5.tgz
tar xzf mongodb-macos-x86_64-6.0.5.tgz
rm mongodb-macos-x86_64-6.0.5.tgz
sudo cp mongodb-macos-x86_64-6.0.5/bin/mongod /usr/local/bin
sudo cp mongodb-macos-x86_64-6.0.5/bin/mongos /usr/local/bin
rm -rf mongodb-macos-x86_64-6.0.5
```
#### Install Server Tools
```bash
curl https://fastdl.mongodb.org/tools/db/mongodb-database-tools-macos-x86_64-100.7.0.zip --output mongodb-database-tools-macos-x86_64-100.7.0.zip
unzip mongodb-database-tools-macos-x86_64-100.7.0.zip
cd mongodb-database-tools-macos-x86_64-100.7.0/bin
sudo cp * /usr/local/bin/

cd ../../
rm -rf mongodb-database-tools-macos-x86_64-100.7.0
rm mongodb-database-tools-macos-x86_64-100.7.0.zip
```


### Options
```bash
mongod --help
# When auth is specified, all database clients who want to connect to mongod first need to authenticate.
mongod --auth
# The bind_ip option allows us to specify which IP addresses mongod should bind to. When mongod binds to an IP address, clients from that address are able to connect to mongod.
mongod --bind_ip 123.123.123.123
# To bind to multiple addresses and/or hosts, you can specify them in a comma-separated list.
mongod --bind_ip localhost, 123.123.123.123
# daemon mode
mongod --fork
# Replication mode with basic security and auth enabled
mongod --replSet
# Set different keyFiles for each machine in production
mongod --keyFile
# TSL transport ecryption
mondod --sslPEMKey
mondod --sslCAKey
mondod --sslMode
```


### Run
```bash
# To run a single server database
# create dir
sudo mkdir -p ~/.mongodb/data/db
sudo mkdir -p ~/.mongodb/data/log
sudo chown aliaksandr ~/.mongodb/data/db

# auth disabled by default
# run daemon port 27017
sudo mongod --dbpath ~/.mongodb/data/db --logpath ~/.mongodb/data/log/mongod.log --fork
# cmd+n
# The mongo javascript shell connects to localhost and test database by default
mongosh
# mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.8.0
```


### Configuration file
```yaml
# use relative path
storage:
  dbPath: ".mongodb/data/db"
systemLog:
  path: ".mongodb/data/log/mongo.log"
  destination: "file"
  logAppend: true
# auth and authorization
security:
  authorization: enabled
# replication:
#   replSetName: test-example
# net:
#   bindIp : "localhost,127.0.0.1,192.168.103.100"
# tls:
#   mode: "requireTLS"
#   certificateKeyFile: "/etc/tls/tls.pem"
#   CAFile: "/etc/tls/TLSCA.pem"
# security:
#   keyFile: "~/.mongodb/data/keyfile"
processManagement:
  fork: true
```
#### Run with mongod.conf
```bash
mkdir ~/.mongodb/conf
# add data above to the mongod.conf
touch ~/.mongodb/conf/mongod.conf
# run with config
sudo mongod --config ~/.mongodb/conf/mongod.conf
```
#### File structure
```bash
ll .mongodb/data/db
# file prevent second process started up
# WiredTiger.lock
# collection & index data
# *.wt
sudo ls .mongodb/data/db/diagnostic.data/
# diagnostic
# metrics.interim
sudo ls .mongodb/data/db/journal/
# restore data after failure
# 100MB
# WiredTigerLog.0000000007

# delete if something wrong with establishing connection
# mongod.lock

# use to create socket connection to interprocess communication
# allow to mongodb use port
# delete after crash if something wrong with startup
sudo ls /tmp/mongodb-27017.sock
```


### Check
```bash
# shell
ps -ef | grep mongosh
# server
# mongod - main daemon (connection, requests)
ps -ef | grep mongod
# sharded - cluster (query, router)
ps -ef | grep mongos
sudo kill -9 3837
killall mongod
```


### Interaction
#### Shutdown
```bash
show dbs
use admin
db.shutdownServer()
exit
# remove log
sudo rm ~/.mongodb/data/log/mongod.log
```
#### Shell helpers
```bash
# status
db.serverStatus()

# user
db.createUser()
db.dropUser()

# database
db.dropDatabase("test")
db.createCollection("employees")
db.getCollectionNames()

# collection
db.employees.renameCollection()
db.employees.createIndex()
db.employees.drop()

# run database command
db.runCommand(
    {
       "createIndexes": "employees",
           "indexes":[
              {
                 "key":{ "product": 1 },
                 "name": "name_index"
              }
           ]
    }
)

# Introspect shell helper
db.test.createIndex
```
#### Process Log
```bash
# -1 inherit from parent
# 1 info level
# 1 - 5 increase level
db.getLogComponents()
# set level
db.setLogLevel(1, "index")
# View the logs through the Mongo shell
db.adminCommand({ "getLog": "global" })
db.setLogLevel(0, "index")

# View the logs through the command line
sudo tail -f ~/.mongodb/data/log/mongod.log
# {"t":{"$date":"2023-03-21T11:44:57.352+01:00"},"s":"I",  "c":"COMMAND",  "id":23435,   "ctx":"conn2" ... }
# Log Messages Severenity Levels
# F - Fatal
# E - Error
# W - Warning
# I - informational (0)
# Debug (Verbosuty Level 1-5)
```
#### Profiler
```bash
# CRUD
# Adminstrative
# Configuration
# Levels
# 0 - off (default)
# 1 - slow operation > 100ms
# 2 - all operation
db.getProfilingStatus()
db.setProfilingLevel(1)
# show all collections including system
db.runCommand({listCollections: 1})
# system.profile

# change value for slow operation to 0
db.setProfilingLevel( 1, { slowms: 0 } )

db.createCollection("new_collection")
db.new_collection.insert( { "a": 1 } )

# planSummary execStats
db.system.profile.find().pretty()

db.new_collection.find( { "a": 1 } )

# planSummary execStats
db.system.profile.find().pretty()
# clean up
db.new_collection.drop()
```


### Security
#### Client Authentication (verify Identity)
- SCRAM (solted challenge response auth mechanism)
- X.509
- LDAP (enterprise only)
- Kerberos (enterprise only)

#### Intercluster Authentication (handshake)

#### Authorization (verify Privileges)
- Each user has one or more Roles
- Each Role has one or more Priviliges (Resources, Actions)
- Resources (database, collection, set of collections, cluster)
- Actions (read, write, readWrite, shutdown)

- Inherit Roles
- Network Auth Restrictions (Client Source, Server Address)

#### Build-in Roles

PER DATABASE LEVEL
- Database User (read, readWrite)
- Database Administration (dbAdmin, userAdmin, dbOwner)
- Cluster Administration (clusterAdmin, clusterManager, clusterMonitor, hostManager)
- Backup/Restore (backup, restore)
- Super User (root)

ALL DATABASE LEVEL
- Database User (readAnyDatabase, readWriteAnyDatabase)
- Database Administration (dbAdmin, userAdmin, dbOwner)
- Super User (root)

#### Superuser
- Localhost Exception (closes after you create first user)
- ALWAYS create user with admin privileges first!
- ALWAYS create superuser with strong PASSWORD

```bash
# switch to admin database
# All users should be created in admin db
use admin
db.stats()
# MongoServerError: not authorized on admin to execute command

# create root user for admin db use "root" build-in role
db.createUser({
  user: "root",
  pwd: "root123",
  roles : [ "root" ]
})
# same
mongosh localhost:27017/admin --eval '
   db.createUser({
     user: "root",
     pwd: "root123",
     roles: [
       {role: "root", db: "admin"}
     ]
   })
 '
 # verify
mongosh localhost:27017/admin -u 'root' -p 'root123' --eval 'db.hello()'
mongosh localhost:27017/admin -u 'root' -p 'root123' --eval 'db.shutdownServer()'

# Localhost Exception
db.createUser({
  user: "TomAtkins",
  pwd: "tom123",
  roles : [ "readWrite" ]
})
# MongoServerError: command createUser requires authentication

# connect with user root to admin db
mongosh --username root --password root123 --authenticationDatabase admin
db.stats()

# Create security officer (create to manage users)
db.createUser(
  { user: "security_officer",
    pwd: "h3ll0th3r3",
    roles: [ { db: "admin", role: "userAdmin" } ]
  }
)

# Create database administrator (DDL - allowed, DML - not allowed)
# Can not access to the user data
db.createUser(
  { user: "dba",
    pwd: "c1lynd3rs",
    roles: [ { db: "admin", role: "dbAdmin" } ]
  }
)
mongosh --username dba --password c1lynd3rs --authenticationDatabase admin
db.stats()
use test
# MongoServerError: not authorized on test to execute command { dbStats: 1, scale: 1, lsid: { id: UUID("98ebbe4d-21f1-4b43-8efe-89a50e309005") }, $db: "test" }

# create user for test db
use admin
db.createUser(
  { user: "test_dba",
    pwd: "dba123",
    roles: [ { db: "test", role: "dbAdmin" } ]
  }
)
# grant role
db.grantRolesToUser("test_dba", [{db: "playground", role: "dbOwner"}])
# show privileges
db.runCommand( { rolesInfo: { role: "dbOwner", db: "playground" }, showPrivileges: true} )
mongosh --username test_dba --password dba123 --authenticationDatabase admin
use playground
db.stats()
db.shutdownServer()
# MongoServerError: not authorized on admin to execute command { shutdown: 1, lsid: { id: UUID("d55512fe-1cb1-4805-aff0-549c56c7afbe") }, $db: "admin" }
exit
```


### Tools
```bash
# close connection
mongosh --username root --password root123 --authenticationDatabase admin
use test
db.employees.insertOne( { "fn": "Tom", "ln": "Atkins" } )

# mongostat
mongostat --port 27017 --username root --password root123 --authenticationDatabase admin
# mongodump (bson)
mongodump --port 27017 -u root -p root123 --authenticationDatabase admin --db test --collection employees
cat dump/applicationData/products.metadata.json
# mongorestore (bson)
mongorestore --port 27017 -u root -p root123 --authenticationDatabase admin --drop dump/
# mongoexport
# stdout
mongoexport --port 27017 -u root -p root123 --authenticationDatabase admin --db test --collection employees
mongoexport --port 27017 -u root -p root123 --authenticationDatabase admin --db test --collection employees -o employees.json
tail employees.json
# mongoimport
mongoimport --port 27017 -u root -p root123 --authenticationDatabase admin employees.json --drop
# mongofiles
# bsondump
# mongotop
mongosh -u m103-admin -p m103-pass --authenticationDatabase admin
```


### Replication
#### Nodes
- Primary Node (Read Write)
- Secondary Node (Replicate Primary and Restore in case of Failure)
- Arbiter (no data, vote in election, never become primary) (avoid!)
- Hidden (copies of data hidden from application)
- Delayed (recover accidently deleted collections, hot-backups)

#### Async Replication
- Protocol Version 1 PV1 (default) (idempotent info)
- PV0

#### Failure
- >= 7 nodes (use odd number of nodes)
- vote for elect Primary from Secondary (majority)

#### Create Replica Set
add node1.conf
```yaml
storage:
  dbPath: ".mongodb/data/db/node1"
systemLog:
  destination: file
  path: ".mongodb/data/log/node1/mongod.log"
  logAppend: true
net:
  bindIp: localhost
  port: 27011
security:
  authorization: enabled
  keyFile: ".mongodb/pki/test-keyfile"
processManagement:
  fork: true
replication:
  replSetName: test-example
```

```bash
touch ~/.mondodb/conf/node1.conf
# dir for key file
mkdir -p ~/.mongodb/data/db/node1
mkdir -p ~/.mongodb/data/log/node1
mkdir -p ~/.mongodb/pki
openssl rand -base64 741 > ~/.mongodb/pki/test-keyfile
chmod 400 ~/.mongodb/pki/test-keyfile

# run node1
sudo mongod --config ~/.mongodb/conf/node1.conf

cd .mongodb/conf
cp node1.conf node2.conf
cp node2.conf node3.conf

# Edit node2.conf (change paths and port 27012)
# Edit node3.conf (change paths and port 27013)
# Use same keyFile
mkdir ~/.mongodb/data/db/{node2,node3}
mkdir ~/.mongodb/data/log/{node2,node3}

sudo mongod --config ~/.mongodb/conf/node2.conf
sudo mongod --config ~/.mongodb/conf/node3.conf

# Enable communication
# Connect first node
mongosh --port 27011
rs.initiate()
db.createUser({
  user: "root",
  pwd: "root123",
  roles : [ {role: "root", db: "admin"} ]
})

# current primary 27011
mongosh --host "localhost:27011" -u "root" -p "root123" --authenticationDatabase "admin"
# heartbeatIntervalMillis: Long("2000"),
rs.status()

rs.add("localhost:27012")
rs.add("localhost:27013")

rs.isMaster()
# election of primary
rs.stepDown()
# primary: 'localhost:27012'
rs.isMaster()
# check command
rs.isMaster

db.serverStatus()['repl']
# rbid: 2 number of rollback
```


### Replication Configuration Document
```bash
rs.conf()
```
Useful fields
```txt
- _id: test-example # replSetName
- version: 1 # number of changes in Replica Set
- members: [
  {
    _id: 1,
    host: localhost:27011,
    arbiterOnly: false,
    hidden: false,
    # set zero if arbiterOnly or hidden equal true
    # priority: 0 exclude member from primary
    priority: 1,
    # default 0 set for Delayed node
    # if secondaryDelaySecs > 3600 set priority: 0
    secondaryDelaySecs: 3600,
    votes: 1
  }
]
```


### Local DB
```bash
mongosh --username root --password root123 --authenticationDatabase admin
show dbs
# admin contains all administrative data
use admin
# system.keys
# system.users
# system.version
use local
# startup_log
show collections

mongosh --host "localhost:27011" -u "root" -p "root123" --authenticationDatabase "admin"
use local
# more collections with config data
show collections

# center point of replocation mechaism oplog.rs
# oplog.rs rotation set
# operation log (save excuted operations)
# one operation (many) may result in many oplog.rs entries
db.oplog.rs.findOne()
var stats = db.oplog.rs.stats()
# capped collection (it will grow to a pre-configured size before it starts to overwrite the oldest entries with newer ones)
stats.capped
stats.size
# var stats = db.oplog.rs.stats(1024*1024)
# max size
# 5% of HD
stats.maxSize
# actual oplog size
rs.printReplicationInfo()

# Check replication process
# create db replica
use replica
db.createCollection('messages')
show collections
use local
db.oplog.rs.find( { "o.msg": { $ne: "periodic noop" } } ).sort( { $natural: -1 } ).limit(1).pretty()
use replica
for ( i=1; i< 100; i++) { db.messages.insertOne( { 'msg': 'not yet', _id: i } ) }
use local
db.oplog.rs.find({"ns": "replica.messages"}).sort({$natural: -1})
use replica
# one operation
db.messages.updateMany( {}, {$set: { author: 'whoami' } })
use local
# but in oplog several operation
db.oplog.rs.find( { "ns": "replica.messages" } ).sort({ $natural: -1})

# try to write to local
db.mylocalcollection.insertOne({"msg": "can't touch this"})
show collections
db.oplog.rs.find( { "ns": "local.mylocalcollection" } ).sort({ $natural: -1})
```


### Reconfiguration replication set
```bash
rs.isMaster()

# create node4
cd ~/.mongodb/conf
cp node3.conf node4.conf
# Edit node4.conf (change path and port)
# Use same keyFile
mkdir ~/.mongodb/data/db/node4
mkdir ~/.mongodb/data/log/node4

# create arbiter
cp node4.conf arbiter.conf
# Edit arbiter.conf (change path and port: 28000)
mkdir ~/.mongodb/data/db/arbiter
mkdir ~/.mongodb/data/log/arbiter

sudo mongod --config ~/.mongodb/conf/node4.conf
sudo mongod --config ~/.mongodb/conf/arbiter.conf

rs.add("localhost:27014")
# arbiter
rs.addArb("localhost:28000")
rs.isMaster()

# kill arbiter
rs.remove("localhost:28000")

# now we have even number of nodes and we need to hide one
cfg = rs.conf()
# Editing our new variable cfg to change topology
cfg.members[3].votes = 0
cfg.members[3].hidden = true
cfg.members[3].priority = 0
# reconfig set
rs.reconfig(cfg)
# now only odd number could vote
```


### Read Write Secondary
```bash
mongosh --host "localhost:27011" -u "root" -p "root123" --authenticationDatabase "admin"
rs.isMaster()
use rw
db.students.insertOne(
  { "first_name": "Tom", "last_name": "Atkins", "grade": "A+" }
)
exit
mongosh --host "localhost:27012" -u "root" -p "root123" --authenticationDatabase "admin"

show dbs
use db
show collections
db.students.find()
# MongoServerError: not primary and secondaryOk=false - consider using db.getMongo().setReadPref() or readPreference in the connection string
# Enabling read commands on a secondary node
db.getMongo().setReadPref("primaryPreferred")
db.students.find()
# Attempting to write data directly to a secondary node (this should fail, because we cannot write data directly to a secondary)
db.students.insertOne(
  { "first_name": "Who", "last_name": "Ami", "grade": "A+" }
)
# MongoServerError: not primary

# Shutdown node2
use admin
db.shutdownServer()
# MongoNetworkError: connection 3 to 127.0.0.1:27012 closed
exit

# Check that node not reachable
mongosh --host "localhost:27011" -u "root" -p "root123" --authenticationDatabase "admin"
rs.status()
# stateStr: '(not reachable/healthy)',

# Shutdown node3
mongosh --host "localhost:27013" -u "root" -p "root123" --authenticationDatabase "admin"
use admin
db.shutdownServer()

# One node1 left
# Verifying that the last node stepped down to become a secondary when a majority of nodes in the set were not available
rs.isMaster()

# We cannot write to node1.
# It is an other mechanism for fail safety
```


### Read Prefernces
```bash
db.getMongo().setReadPref("primary")
# possible to read old data
db.getMongo().setReadPref("primaryPreferred")
db.getMongo().setReadPref("secondary")
db.getMongo().setReadPref("primarySecondary")
# geo local reads
db.getMongo().setReadPref("nearest")
```

### Failover and Elections
```bash
# Upgrade secondary first srvers
# Set new primary
rs.stepDown()

# Wait when primary elected so we need odd number of nodes

# Setting the priority of a node to 0, so it cannot become primary (making the node "passive")
cfg = rs.conf()
cfg.members[2].priority = 0
rs.reconfig(cfg)
rs.isMaster()
# passives: [ 'localhost:27013' ],

# Forcing an election in this replica set (although in this case, we rigged the election so only one node could become primary)
rs.stepDown()
# primary: 'localhost:27012'
rs.isMaster()
```


### Write Concern Levels (provides a level of durability)
- 0: Don't wait for acknowledgement
- 1: wait for acknowledgement from primary (default)
- >=2: wait for acknowledgement from primary and one secondary
- "majority": wait for majority acknowledgement ceil(Replica Sets / 2) (by default j: true)

wtimeout: <int> the time to wait for the requested write before failed

j: <true/false> - requires the node to commit the write operation to the journal before returning an acknowledgement

### Read Concern Levels
- local: fast and latest data for primary
- available (sharded clusters): fast data from secondary
- "majority": safe and fast
- linearizable-majority: safe and latest (single document, slow)

### Sharding
- Horizontal scaling
- Shard Replica Set
- Mongos (many processes use metadata from config server)
- Config Servers Replica Set

#### When
- Check that Vertical Scale is economically reasonable
- Impact of Network how 20 TB backuped, restored, resync
- Operation Workload (15x Larger Dataset > 15x Larger Indexes 15x RAM)
- Geographically Distributed Data
- Analyze aggregation pipeline

#### Architecture
- Any number of shards
- Mongos connect to shard using metadata from config servers(CSRS)
- Data in shards saved proprotionally and update data in config servers
- Mongos split chuncks
- Primary shard
- Shard merges (if data spread across shards)


#### Setup Shard Cluster

Run Replica Set node1 node2

```yaml
sharding:
  clusterRole: configsvr
storage:
  dbPath: ".mongodb/data/db/csrs1"
systemLog:
  destination: file
  path: ".mongodb/data/log/csrs1/mongod.log"
  logAppend: true
net:
  bindIp: localhost
  port: 26001
security:
  keyFile: ".mongodb/pki/test-keyfile"
processManagement:
  fork: true
replication:
  replSetName: test-example-csrs
```
```bash
touch ~/.mongodb/conf/csrs1.conf
mkdir -p ~/.mongodb/data/db/csrs1
mkdir -p ~/.mongodb/data/log/csrs1
# Create csrs2.conf change paths and set port 26002
cp ~/.mongodb/conf/csrs1.conf ~/.mongodb/conf/csrs2.conf
# Create csrs3.conf change paths and set port 26003
cp ~/.mongodb/conf/csrs1.conf ~/.mongodb/conf/csrs3.conf
mkdir ~/.mongodb/data/db/{csrs2,csrs3}
mkdir ~/.mongodb/data/log/{csrs2, csrs3}
# run
sudo mongod --config ~/.mongodb/conf/csrs1.conf
sudo mongod --config ~/.mongodb/conf/csrs2.conf
sudo mongod --config ~/.mongodb/conf/csrs3.conf

mongosh --port 26001
rs.initiate()
# create admin
db.createUser({
  user: "root",
  pwd: "root123",
  roles : [ {role: "root", db: "admin"} ]
})
db.auth("root", "root123")
rs.add("localhost:26002")
rs.add("localhost:26003")
rs.isMaster()
```

#### Mongos Configuration File
```yaml
sharding:
  configDB: test-example-csrs/localhost:26001,localhost:26002,localhost:26003
systemLog:
  destination: file
  path: ".mongodb/data/log/mongos.log"
  logAppend: true
net:
  bindIp: localhost
  port: 26000
security:
  keyFile: ".mongodb/pki/test-keyfile"
processManagement:
  fork: true
```
```bash
touch ~/.mongodb/conf/mongos.conf
# we use data from Replica Set
# log saved in ~/.mongodb/data/log/mongos.log
# run
sudo mongos --config ~/.mongodb/conf/mongos.conf
# inherit users
mongosh --port 26000 --username root --password root123 --authenticationDatabase admin
# check status
sh.status()
```

#### Setup Sharding
Update node1.conf, node2.conf, node3.conf
```yaml
# for shrading
sharding:
  clusterRole: shardsvr
```
```bash
# connect secondary node2 and node3 to apply rolling update
# shutdown node2
mongosh --host "localhost:27012" -u "root" -p "root123" --authenticationDatabase "admin"
use admin
db.shutdownServer()
exit
# restart node2
sudo mongod --config ~/.mongodb/conf/node2.conf

# shutdown node3
mongosh --host "localhost:27013" -u "root" -p "root123" --authenticationDatabase "admin"
use admin
db.shutdownServer()
exit
# restart node3
sudo mongod --config ~/.mongodb/conf/node3.conf

# shutdown node1 (primary)
mongosh --host "localhost:27011" -u "root" -p "root123" --authenticationDatabase "admin"
rs.stepDown()
# wait for election
use admin
db.shutdownServer()
exit
# restart node1
sudo mongod --config ~/.mongodb/conf/node1.conf

# back to mongos
mongosh --port 26000 --username root --password root123 --authenticationDatabase admin
sh.addShard("test-example/localhost:27012")
sh.status()
```

### Config DB
Never write data to Config DB

```bash
use config
show collections
db.databases.find().pretty()
# partitioned: false
db.collections.find().pretty()

db.shards.find().pretty()
db.chunks.find().pretty()

db.mongos.find().pretty()

```

### Shard Keys
Data distribution in a shared cluster
- index field in collection
- immutable _id
- mutable refineCollectionShardKey
- permanent

``` bash
sh.enableSharding("replica")
db.messages.findOne()
db.messages.createIndex( { "author": 1 } )
sh.shardCollection( "replica.messages", { "author": 1 } )
# shardKey: { author: 1 },
# chunkMetadata: [ { shard: 'test-example', nChunks: 1 } ],

db.products.createIndex({ "msg" : 1})
sh.reshardCollection("replica.messages", { "msg": 1 })
```

#### Good Shard Key
- High Cardianlity (number of uniq key values)
- Low Frequency
- Non-Monotonic Changes (avoid dates)
- Read isolation (use combine index to check only specific chunk)

Test ShardKey in staging before Production

Unsharding Hard!

#### Hashed Shard Key

Use hashing function for monotonic shard keys
- No fast sorts
- No geographical workloads
- No support array
```bash
sh.enableSharding("replica")
# not-array field
db.messages.createIndex( { "date": "hashed" } )
sh.shardCollection( "replica.messages", { "date": "hashed" } )
```

#### Chunks

Mapping chunks in shards

```bash
show dbs
use config
show collections
db.chunks.findOne()
# min max bounds

db.getSiblingDB("config").chunks.find(
  { $expr: { $and: [
    { $gte: [21572585, "$min.sku"] },
    { $lt: [21572585, "$max.sku"] }
  ] } } )
```

Different values of Shard Key is our Key Space

All documents from the same chunk live in the same shard
1 chunk 1 shard

ChunkSuze = 64 MB (default)
```bash
# change settings
db.settings.updateOne(
   { _id: "chunksize" },
   { $set: { _id: "chunksize", value: 2 } },
   { upsert: true }
)
# still same
sh.status()
use replica
for ( i=100; i < 200; i++) { db.messages.insertOne(
    { 'msg': 'not yet', 'author': 'unknown', _id: i }
  )
}
```

Jumbo Chunks(same Shard Key) > greater than ChunkSize


#### Balancing
- Run on Primary member of Config Server Replica Set
- Try to attempt evenly number of chuncs in sharded cluster
- Automatic

```bash
# timeout, interval
sh.startBalancer(60000, 60000)
sh.stopBalancer(60000, 60000)
# Enable/disable the balancer
sh.setBalancerState(true)
```

#### Queries
- mongos handles all queries in the cluster
- mongos builds a list of shards to target a query (opens cursor accros each shard)
- mongos merge results together
- sort() for each shard in cluster and merge-sorts the results
- limit() for each shard in cluster and re-applies the limit to the merged set of results
- skip() performs the skip against the merged set of results

Targeted Query contains ShardKey
- Opens cursor against query predicat
- Fast

Scatter Gather no ShardKey in Query or Range Query (hashed)
- Opens cursor agains each shard (scattered)
- Slow
