!! NOT READY FOR PRODUCTION

# Startup replica set mongodb

1. start the mongo databases
```bash
docker-compose up
or
docker-compose up -d
```
2. exec into one of the mongos:
```bash
docker exec -it localmongo1 /bin/bash
```

3. access mongo console
```bash
mongo
```

4. configure replica set by pasting the following
```js
rs.initiate(
  {
    _id : 'rs0',
    members: [
      { _id : 0, host : "mongo1:27017" },
      { _id : 1, host : "mongo2:27017" },
      { _id : 2, host : "mongo3:27017" }
    ]
  }
)
```