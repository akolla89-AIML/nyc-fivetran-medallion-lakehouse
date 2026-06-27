# NYC Fivetran Medallion Lakehouse

## Project Overview

This project simulates a production-grade Azure Databricks Medallion Lakehouse pipeline using a realistic enterprise architecture.

The objective is to build an end-to-end Data Engineering solution that mirrors how SaaS data (Salesforce) is ingested, processed, and transformed into analytics-ready datasets using Azure Databricks.

Instead of connecting to Salesforce and Fivetran directly, this project simulates Fivetran by landing hourly Parquet files into Azure Data Lake Storage Gen2.

---

# Architecture

```
Salesforce
      │
      ▼
Fivetran (Simulated)
      │
      ▼
Azure Data Lake Storage Gen2 (Landing)
      │
      ▼
Databricks Bronze
      │
      ▼
Databricks Silver
      │
      ▼
Databricks Gold
      │
      ▼
Power BI
```

---

# Objectives

- Simulate production-grade ingestion
- Build a Medallion Architecture
- Implement incremental data processing
- Handle schema evolution
- Handle late arriving files
- Implement watermarking
- Support reprocessing
- Optimize Delta tables
- Deploy using Databricks Asset Bundles
- Build DEV / TEST / PROD environments

---

# Repository Structure

```text
src/
    ingestion/

simulator/

config/

ddl/

tests/

docs/

notebooks/

bundles/
```

---

# Technologies

- Azure Data Lake Storage Gen2
- Azure Databricks
- Unity Catalog
- Delta Lake
- Auto Loader
- Python
- PySpark
- Databricks Asset Bundles
- Git
- GitHub
- VS Code

---

# Current Progress

## Phase 1 ✅

- Azure resources created
- ADLS Gen2 configured
- Fivetran simulator built
- Initial load completed
- Incremental load simulator completed
- Git repository created

## Phase 2 🚧

- VS Code setup
- Python environment
- Repository structure
- Project documentation

---

# Future Enhancements

- Bronze pipeline
- Silver transformations
- Gold dimensional model
- CI/CD deployment
- Schema evolution
- Watermarking
- Late arriving data
- Duplicate handling
- Delta optimization
- Monitoring
- Unit testing

---

# Dataset

NYC High Volume For-Hire Vehicle Trip Records (Parquet)

Used as a realistic substitute for Salesforce transactional data.

---

# Author

Learning project focused on building enterprise-level Azure Databricks Data Engineering skills.