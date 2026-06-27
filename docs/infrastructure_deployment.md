# NYC Fivetran Medallion Lakehouse Architecture

## 1. Project Overview

This project implements an enterprise-style Azure Databricks Medallion Lakehouse architecture using Azure Data Lake Storage Gen2 (ADLS Gen2) and Unity Catalog.

The project simulates a Fivetran ingestion pipeline that lands parquet files into ADLS. Databricks Auto Loader ingests the files into Bronze Delta tables, followed by Silver and Gold transformations.

---

# 2. High-Level Architecture

                    HVFHV Source Dataset
                            │
                            ▼
                  Fivetran Simulator (Python)
                            │
                            ▼
                ADLS Gen2 Landing Zone
                            │
                            ▼
               Databricks Auto Loader
                            │
                            ▼
                  Bronze Delta Tables
                            │
                            ▼
                  Silver Delta Tables
                            │
                            ▼
                   Gold Delta Tables
                            │
                            ▼
                  Power BI / Analytics

---

# 3. Unity Catalog Design

Each environment has its own Unity Catalog.

Development

Catalog

    nyc_lakehouse_dev

Schemas

    bronze
    silver
    gold
    metadata
    audit

---

Test

Catalog

    nyc_lakehouse_test

Schemas

    bronze
    silver
    gold
    metadata
    audit

---

Production

Catalog

    nyc_lakehouse_prod

Schemas

    bronze
    silver
    gold
    metadata
    audit

---

# 4. Table Naming Convention

Bronze

    bronze.hvfhv

Silver

    silver.hvfhv

Gold

    gold.trip_summary

    gold.daily_trip_metrics

    gold.zone_statistics

---

# 5. Storage Strategy

This project uses External Delta Tables.

Landing files remain in ADLS Gen2.

Bronze, Silver and Gold tables are implemented as External Delta Tables with data stored in explicitly defined ADLS locations.

Advantages

• Complete control of storage layout

• Enterprise deployment pattern

• Easier backup and disaster recovery

• Data remains accessible outside Databricks if required

---

# 6. ADLS Directory Structure

Storage Account

    azdbaimlstorage01

Container

    lakehouse01

landing/
    hvfhv/
        initial/
        incremental/
            year=2024/
                month=12/
                    day=01/
                        hour=00/
                        ...
                    day=31/
                        hour=23/

bronze/
    dev/
        hvfhv/

    test/
        hvfhv/

    prod/
        hvfhv/

silver/
    dev/
        hvfhv/

    test/
        hvfhv/

    prod/
        hvfhv/

gold/
    dev/
        hvfhv/

    test/
        hvfhv/

    prod/
        hvfhv/

checkpoints/
    dev/
        bronze/
            hvfhv/

    test/
        bronze/
            hvfhv/

    prod/
        bronze/
            hvfhv/

audit/

schemas/

---

# 7. Bronze Ingestion Strategy

Bronze ingestion is implemented using Databricks Auto Loader.

Source

    landing/hvfhv/

Auto Loader performs

• Initial historical ingestion

• Continuous incremental ingestion

• Schema inference

• Checkpoint tracking

Destination

    bronze.hvfhv

Checkpoint

    checkpoints/<environment>/bronze/hvfhv/

---

# 8. Initial Load Strategy

Historical dataset

    landing/hvfhv/initial/

        hvfhv_2024-11.parquet

During the first execution, Auto Loader processes every file located in the landing directory.

After successful ingestion, Auto Loader creates a checkpoint that records processed files.

No separate initial-load notebook is required.

---

# 9. Incremental Load Strategy

New files arrive continuously under

landing/hvfhv/incremental/

Example

year=2024/
    month=12/
        day=01/
            hour=00/
            hour=01/
            ...
            hour=23/

Future years

year=2025/
year=2026/

Auto Loader detects only files that have not previously been processed.

---

# 10. Checkpoint Strategy

Each environment maintains its own checkpoint location.

Development

    checkpoints/dev/bronze/hvfhv/

Test

    checkpoints/test/bronze/hvfhv/

Production

    checkpoints/prod/bronze/hvfhv/

Purpose

• Exactly-once file ingestion

• Recovery after failures

• Incremental processing

---

# 11. Partitioning Strategy

Landing

Source system controls directory partitioning.

Current structure

year
month
day
hour

Bronze

External Delta Table

Initially unpartitioned to simplify ingestion and support schema evolution.

Silver

Partition by business date (to be finalized during Silver implementation).

Gold

Partition strategy determined by reporting and analytical requirements.

---

# 12. Environment Strategy

A single Landing Zone is shared across all environments.

Environment isolation is achieved through separate Unity Catalogs, schemas, checkpoint locations and external table storage.

Development

Catalog

    nyc_lakehouse_dev

Bronze Storage

    bronze/dev/

Checkpoint

    checkpoints/dev/

---

Test

Catalog

    nyc_lakehouse_test

Bronze Storage

    bronze/test/

Checkpoint

    checkpoints/test/

---

Production

Catalog

    nyc_lakehouse_prod

Bronze Storage

    bronze/prod/

Checkpoint

    checkpoints/prod/

---

# 13. Design Principles

• Single source of truth for landing data.

• Independent DEV, TEST and PROD processing.

• Environment-specific Bronze, Silver and Gold storage.

• Environment-specific checkpoints.

• External Delta Tables managed through Unity Catalog.

• Auto Loader provides incremental ingestion and exactly-once processing.

• Medallion Architecture separates raw, cleansed and business-ready data.