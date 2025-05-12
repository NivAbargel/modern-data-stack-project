# 🚀 Modern Data Stack Project

This project demonstrates an end-to-end data engineering pipeline using modern tools including **Airflow**, **DBT**, **Docker**, **PostgreSQL**, and **Metabase**. It's designed as a portfolio piece to showcase hands-on knowledge of the modern data engineering lifecycle using API ingestion, container orchestration, secure configuration, and modular pipeline development.

---

## 🛠️ Tools & Technologies

| Layer            | Tool              | Description |
|------------------|-------------------|-------------|
| Ingestion        | Python (custom)   | Pulls data from the GitHub API securely using personal access tokens |
| Orchestration    | Apache Airflow    | Manages and schedules data pipelines |
| Transformation   | DBT               | SQL modeling and data transformation (planned) |
| Storage          | PostgreSQL        | Raw and analytics tables stored relationally |
| Visualization    | Metabase          | Dashboarding layer connected to transformed PostgreSQL data |
| Containerization | Docker + Compose  | Isolated environments for each service, managed centrally |
| Secrets Handling | .env + .env.example | Secure handling of credentials using dotenv standards |

---

## 📁 Project Structure

```text
/modern-data-stack-project
├── ingestion/         # Python scripts and Dockerfile for GitHub API ingestion
│   ├── api_ingest.py
│   ├── requirements.txt
│   └── Dockerfile
├── airflow/           # Airflow DAGs, logs, and plugin folders
│   ├── dags/
│   ├── logs/
│   └── plugins/
├── dbt/               # DBT models and configs (placeholder)
│   └── models/
├── postgres/          # Placeholder for future database init or backup scripts
├── dashboards/        # Metabase setup or dashboard templates (placeholder)
├── docker/            # Reserved for Dockerfiles, build scripts if needed
├── .env               # Local-only secrets (gitignored)
├── .env.example       # Template for devs to create their own .env
├── .gitignore         # Git ignore rules for secrets, build artifacts, etc.
├── docker-compose.yaml # Central service orchestration config
└── README.md
```

---

✅ This project follows best practices for:
- Secure API access (GitHub token stored via `.env`)
- Modular container architecture (Docker Compose)
- Relational schema design (Postgres normalization with users & repos)
- Clear onboarding via `.env.example`

📌 Status:
- [x] Infrastructure and containerization complete
- [x] GitHub API token configured securely
- [ ] GitHub ingestion script in development
- [ ] dbt transformations and Metabase dashboards planned

---
