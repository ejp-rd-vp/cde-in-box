# cde-in-box
This repository contains software to create and deploy CDEs

To use CDE in box solutions clone this repository to your machine.

```sh
git clone https://github.com/ejp-rd-vp/cde-in-box
```

## Instructions
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

**Step 4:** If your `graphdb version` is different from `9.7.0` then change the version number of graph DB in the docker-compose file.

```sh
graph_db:
    build:
      context: ./graph-db
      dockerfile: Dockerfile        
      args:
        version: 9.7.0
```
### Running cde in box docker setup
Once you have done above configurations you can run `cde-in-box` setup by running docker-compose file in this repository

```sh
docker-compose up -d
```