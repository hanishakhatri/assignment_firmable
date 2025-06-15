CREATE TABLE IF NOT EXISTS raw_commoncrawl (
    url TEXT PRIMARY KEY,
    company_name TEXT,
    industry TEXT
);

CREATE TABLE IF NOT EXISTS raw_abr (
    abn TEXT PRIMARY KEY,
    company_name TEXT,
    entity_type TEXT,
    entity_status TEXT,
    entity_address TEXT,
    entity_state TEXT,
    entity_postcode TEXT,
    entity_start_date DATE
);

CREATE TABLE IF NOT EXISTS merged_company_data (
    abn TEXT,
    url TEXT,
    company_name TEXT,
    industry TEXT,
    source TEXT,
    match_confidence FLOAT,
    PRIMARY KEY (abn, url)
);

CREATE TABLE IF NOT EXISTS merged_company_data (
    abn TEXT,
    url TEXT,
    company_name TEXT,
    industry TEXT,
    source TEXT,
    match_confidence FLOAT,
    PRIMARY KEY (abn, url)
);