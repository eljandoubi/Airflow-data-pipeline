# Project: Data Pipeline with Airflow

## Overview

A music streaming company, Sparkify, has decided that it is time to introduce more automation and monitoring to their data warehouse ETL pipelines and come to the conclusion that the best tool to achieve this is Apache Airflow.
They have decided to bring you into the project and expect you to create high grade data pipelines that are dynamic and built from reusable tasks, can be monitored, and allow easy backfills. They have also noted that the data quality plays a big part when analyses are executed on top the data warehouse and want to run tests against their datasets after the ETL steps have been executed to catch any discrepancies in the datasets.

## Data
The source data resides in S3 and needs to be processed in Sparkify's data warehouse in Amazon Redshift. The source datasets consist of JSON logs that tell about user activity in the application and JSON metadata about the songs the users listen to.# Datasets
For this project, you'll be working with two datasets. Here are the s3 links for each:
- Log data: `s3://udacity-dend/log_data`
- Song data: `s3://udacity-dend/song_data`

#### Copy S3 Data

The data for the next few exercises is stored in Udacity's S3 bucket. This bucket is in the US West AWS Region. To simplify things, we are going to copy the data to your own bucket, so Redshift can access the bucket.

<br data-md>

**If you haven't already**, create your own S3 bucket using the AWS Cloudshell **(this is just an example - buckets need to be unique across all AWS accounts**): `aws s3 mb s3://bean-murdock/`

<br data-md>

Copy the data from the udacity bucket to **your own** bucket -- **this is only an example**:  ```

```
aws s3 cp s3://udacity-dend/log-data/ s3://bean-murdock/log-data/  --recursive
aws s3 cp s3://udacity-dend/song-data/ s3://bean-murdock/song-data/ --recursive
```


<br data-md>

List the data **in your own bucket** to be sure it copied over -- **this is only an example**: 

```
aws s3 ls s3://bean-murdock/log-data/
aws s3 ls s3://bean-murdock/song-data/
```

<br data-md>


## Setup

You need to create a serverless Redshift cluster and run the queries in `create_tables.sql` in order to create tables needed for the data pipeline.


## Building the operators

All of the operators and task instances will run SQL statements against the Redshift database. However, using parameters wisely will allow you to build flexible, reusable, and configurable operators you can later apply to many kinds of data pipelines with Redshift and with other databases.

### Stage Operator

The stage operator is expected to be able to load any JSON formatted files from S3 to Amazon Redshift. The operator creates and runs a SQL COPY statement based on the parameters provided. The operator's parameters should specify where in S3 the file is loaded and what is the target table. 

The parameters should be used to distinguish between JSON file. Another important requirement of the stage operator is containing a templated field that allows it to load timestamped files from S3 based on the execution time and run backfills.

### Fact and Dimension Operators

With dimension and fact operators, you can utilize the provided SQL helper class to run data transformations. Most of the logic is within the SQL transformations and the operator is expected to take as input a SQL statement and target database on which to run the query against. You can also define a target table that will contain the results of the transformation.

Dimension loads are often done with the truncate-insert pattern where the target table is emptied before the load. Thus, you could also have a parameter that allows switching between insert modes when loading dimensions. Fact tables are usually so massive that they should only allow append type functionality.

### Data Quality Operator

The final operator to create is the data quality operator, which is used to run checks on the data itself. The operator's main functionality is to receive one or more SQL based test cases along with the expected results and execute the tests. For each the test, the test result and expected result needs to be checked and if there is no match, the operator should raise an exception and the task should retry and fail eventually. 

For example one test could be a SQL statement that checks if certain column contains NULL values by counting all the rows that have NULL in the column. We do not want to have any NULLs so expected result would be 0 and the test would compare the SQL statement's outcome to the expected result.
