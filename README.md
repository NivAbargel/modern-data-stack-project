# 🚀 Modern Data Stack Project

This project demonstrates an end-to-end data engineering pipeline using modern tools including **Airflow**, **DBT**, **Docker**, **PostgreSQL**, and **Power BI/Streamlit**. It's designed as a portfolio piece to showcase hands-on knowledge of the modern data engineering lifecycle.

---

## 🛠️ Tools & Technologies

| Layer            | Tool              | Description |
|------------------|-------------------|-------------|
| Ingestion        | Python / Airbyte  | Pulls data from APIs or files |
| Orchestration    | Apache Airflow    | Manages and schedules data pipelines |
| Transformation   | DBT               | SQL modeling and data transformation |
| Storage          | PostgreSQL        | Raw, staging, and analytics layer |
| Visualization    | Streamlit / Power BI | Interactive dashboards |
| Containerization | Docker            | Environment isolation and deployment |

---

## 📁 Project Structure

```text
/modern-data-stack-project
├── ingestion/         # Python scripts for data ingestion
├── airflow/           # Airflow DAGs and config
├── dbt/               # DBT models and configs
├── postgres/          # Init scripts and schemas
├── dashboards/        # Streamlit or Power BI files
├── docker/            # Dockerfiles and docker-compose config
├── .gitignore
└── README.md
