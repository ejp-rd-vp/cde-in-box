# cde-in-box
This repository contains software to create and deploy CDEs

To use CDE in box solutions clone this repository to your machine.

```sh
git clone https://github.com/ejp-rd-vp/cde-in-box
```

## Instructions
### Configuring configuration and data folders 

**Step 1:** Create the following folder structure, relative to where you plan to keep your pre and post-transformed data:

```
        .
        ./data/   
        ./data/mydataX.csv  (input csv files, e.g. "height.csv")
        ./data/mydataY.csv...
        ./data/triples/  (output FAIR data ends up here)
        ./config/
        ./config/XXXX_yarrrml_template.yaml (XXXX is a one-word tag of the "type" of data, e.g. "height")
```

### Configuring docker setup
#### GraphDB
To run CDE in a box docker-compose you need graphDB triple store free edition. Follow the steps below to get free edition of graphdb.
<br></br>
**Step 1:** GO to this [url](https://www.ontotext.com/products/graphdb/graphdb-free/) and registry to download GraphDB free edition.
<br></br>
**Step 2:** The download will be sent to your email. From the email follow link to download page and `click` on "Download as a stand-alone server". This step will download "graphdb-free-{version}-dist.zip" file to your machine.
<br></br>
**Step 3:** Move "graphdb-free-{version}-dist.zip" file to the following location

```sh
mv graphdb-free-{version}-dist.zip cde-in-box/graph-db
```
**Step 4:** Execute:

```
docker volume create graphdb-data
```

**Step 5:** If your `graphdb version` is different from `9.7.0` then change the version number of graph DB in the docker-compose file.

```
version: '3'

services:
  #  Graph DB service. BEFORE you start running docker-compose file please make sure that you have downloaded free edition of graphDB zip files	
  graphdb:
    image: graph-db:9.7.0
    build:
      context: ./graph-db
      dockerfile: Dockerfile        
      args:
        version: 9.7.0
        edition: free
    restart: always
    hostname: graphdb
    ports:
      - 7200:7200
    volumes:
      - graphdb-data:/opt/graphdb/home
    
  #  This service create's `cde` and `fdp` repositories in graphdb	
  graph_db_repo_manager:
    build: ./graph-db-repo-manager
    depends_on:
      - graphdb
    environment:
      - "GRAPH_DB_URL=http://graphdb:7200"

volumes:
  graphdb-data:
    external: true

```


**Step 6:** Then execute a docker-compose up.   Let it go through the initialization process, and then stop everything.

```sh
docker-compose up -d
```

You now have a docker container 'graph-db:9.7.0' that we will call in this new docker-compose.yml file:

```
version: "3"
services:
  
  graphdb:
    image: graph-db:9.7.0
    restart: always
    hostname: graphdb
    ports:
      - 7200:7200
    volumes:
      - graphdb-data:/opt/graphdb/home

  cde-box-daemon: 
    image: markw/cde-box-daemon:latest
    container_name: cde-box-daemon
    depends_on:
      - yarrrml_transform
      - rdfizer
      - graphdb
    ports:
      - 4567:4567
    volumes:
        - ./data:/data
        - ./config:/config
        
        
  yarrrml_transform: 
    image: markw/yarrrml-parser-ejp:latest
    container_name: yarrrml_transform
    ports:
      - "3000:3000"
    volumes:
      - ./data:/data
  
  
  rdfizer: 
    image: markw/sdmrdfizer_ejp:0.1.0
    container_name: rdfizer
    ports:
      - "4000:4000"
    volumes:
      - ./data:/data
      - ./config:/config

    
volumes:
  graphdb-data:
    external: true

```

**Step 7:**  Running CDE in a Box docker-compose

Once you have done the above configurations you can run `cde-in-a-box` setup by running docker-compose using the above docker-compose.yml,
**IN THE FOLDER THAT CONTAINS THE ./data/triples and ./config and subfolders**

```sh
docker-compose up -d
```

**Step 8:**  Executing transformations

Put an appropriately columned XXXX.csv into the ./data folder

Put a matching YARRRML template file called XXXX_yarrrml_template.yaml into the ./config folder

call the url:  http://localhost:4567 to trigger the transformation of each CSV file, and auto-load into graphDB (this will over-write what is currrently loaded!  We will make this behaviour more flexible later)

**There is sample data in the "sample_data" folder that can be used to test your installation.**
