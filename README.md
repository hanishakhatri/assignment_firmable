# assignment_firmable
DE Assignment by firmable

1. Design and implement a data pipeline that combines Australian company website data from Common Crawl with official business information from the Australian Business Register (ABR).

# clone git repo
git clone git@github.com:hanishakhatri/assignment_firmable.git

# Install dependencies
pip install -r requirements.txt

### Data Pipeline Architecture 
1. Data Pipeline Architecture for common crawl data using GCP to enhance the performance 
# URL : https://miro.com/app/board/uXjVIoP8NjA=/
![common_crawl](assignment_firmable/aus_common_crawl/scripts/aus_common_crawl/Screenshot 2025-06-16 at 1.18.19 AM.png)

#

## TASK 1. Common Crawl (https://commoncrawl.org/)
### Extract Australian company websites (minimum 200,000 websites)
### Dataset: Use March’25 Index
### Fields to extract: Website URL, Company Name, Industry (where available)


# STEP 1. Get Index file for MARCH 2025 from (https://commoncrawl.org/) using below command 
## use these command :  wget https://data.commoncrawl.org/crawl-data/CC-MAIN-2025-13/cc-index.paths.gz

# STEP 2. Unzip the .gz file to extract the data using the below command
## gunzip cc-index.paths.gz

# STEP 3. Download the cluster.idx using below command and you will get the following files as (cdx-000006.gz,cdx-000005.gz etc)
## wget https://data.commoncrawl.org/cc-index/collections/CC-MAIN-2025-13/indexes/cluster.idx

# STEP 4. Filter data based on (.au) Domains from Index using the 
## grep '^au,' cluster.idx | cut -f2 | uniq > au_files.txt

## while read file; do
##   wget https://data.commoncrawl.org/cc-index/collections/CC-MAIN-2025-13/indexes/$file
## done < au_files.txt


# STEP 5. Extract the data from common crawl index (cdx-000006.gz,cdx-000005.gz etc file using the below command)
## cd aus_common_crawl 
## python3 main.py 

# STEP 6. 

Folder structure 
ASSIGNMENT_FIRMABLE/
├── aus_common_crawl/
│   ├── setting.py
│   ├── utils.py
│   └── main.py
│
├── australian_business_register/
│   ├── setting.py
│   ├── utils.py
│   ├── main.py
│   ├── extract_bulk.py
│   ├── extract_zip_file.py
│   ├── extracted_abn_zip_files/
│   │   ├── public_split_1_10/
│   │   └── public_split_11_20/
│   ├── abn_bulk_extract/
│   │   ├── public_split_1_10.zip
│   │   └── public_split_2_10.zip
│   └── extracted_abn_files/
│       ├── public_split_1_10/
│       │   └── file1.xml
│       └── public_split_2_10/
│           └── file2.xml
│
└── requirement.txt

DDL STATEMENT for AUSTRALIAN Business register 

CREATE TABLE abn_entities (
    abn TEXT PRIMARY KEY,
    entity_name TEXT,
    entity_type TEXT,
    entity_status TEXT,
    entity_address TEXT,
    entity_postcode TEXT,
    entity_state TEXT,
    entity_start_date DATE
);

DDL STATEMENT for aus common crawl 
CREATE TABLE IF NOT EXISTS commoncrawl_companies (
    url TEXT PRIMARY KEY,
    company_name TEXT,
    industry TEXT
);



# TASK 2 : 

# Australian Business Register (https://data.gov.au/dataset/ds-dga-5bd7fcab-e315-42cb-8daf-50b7efc2027e/details?q=abn)
## Task: Process ABR bulk extract XML files
## Fields to extract: ABN (Australian Business Number), Entity Name, Entity Type, Entity Status, Entity Address, Entity Postcode, Entity State, Entity Start Date 

1. Extract the downloaded file url (extract_bulk.py)
2. extract the zip file to xml (extract_zip.py)
3. extract the data from xml file using (main.py)


