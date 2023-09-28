# Enumeration Tool

## Description
This tool sends requests to storage areas (AWS S3 Bucket, Azure Blob Storage, Google Cloud Storage) in AWS, Azure and GCP according to the input we enter and returns URLs as public, private or no-bucket.
This performs storage space control in all regions.

## Technologies
- Python

## Installation
Follow the steps below to run the project in your local.

--Clone the repo

```bash
  git clone https://github.com/mmustafabebek/enumeration-tool.git

```

--Go to the project directory

```bash
  cd enumeration-tool

```

--Docker compose

```bash
  docker-compose up

```
*If you don't know what docker is, you can [click](https://docs.docker.com/compose/install/) here.*


## Running the Tool
--Open your local command prompt and go to the project directory

```bash
  cd enumeration-tool

```

--Run program with arguments

```bash
  python main.py bucketname -k mykeyword

```

*When running this tool, the bucketname section is the storage name to be requested.*

*The -k argument will be used for similar searches of the entered bucket name.*

## Images

```bash
  python main.py mybucket1231231232342 -k mykeyword
```
![Tool Image1](https://i.imgur.com/3elgZTg.png)

![Tool Image2](https://i.imgur.com/3LDKi6D.png)

```bash
  python main.py babybucket2312312 -k mykeyword
```
![Tool Image3](https://i.imgur.com/ccAhyyA.png)

![Tool Image4](https://i.imgur.com/61Z9Dm3.png)

## To Do List
- As a result, the returned URLs can be returned to files with different extensions, such as txt, json, etc., depending on the arguments we enter.
- The tool will access not only the storages in the cloud, but also the files in those storages and present them to us in different ways.
- When -k is entered as an argument, the tool will send requests to the bucket name we entered and similar urls containing that bucket name at the same time.
- Many appearance and functional adjustments will be made. Tool will run faster and provide an easier interface.
