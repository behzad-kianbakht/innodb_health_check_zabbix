# MySQL InnoDB Cluster Monitoring for Zabbix

A production-ready monitoring solution for **MySQL InnoDB Cluster** using **Python**, **mysqlsh**, and **Zabbix**.

This project automatically discovers cluster members, collects cluster health information, and integrates directly with Zabbix using a custom template.

---

# Features

- Automatic Cluster Discovery (LLD)
- Primary node detection
- Cluster health monitoring
- Node status monitoring
- Replication lag monitoring
- Member role monitoring
- Cluster topology monitoring
- Automatic failover detection
- Logging with rotating log files
- Multi-node connection support
- JSON output for native Zabbix preprocessing

---

# Components

| File | Description |
|------|-------------|
| InnoDB_Cluster_Monitoring.py | Python monitoring script |
| Innodb_python_monitoring.json | Zabbix 7.4 Template |

---

# Architecture

```text
           +----------------------+
           | MySQL InnoDB Cluster |
           +----------+-----------+
                      |
                  mysqlsh
                      |
          Python Monitoring Script
                      |
                JSON Output
                      |
              Zabbix External Script
                      |
             Zabbix Template (LLD)
                      |
           Dashboards & Triggers
```

---

# Monitored Information

## Cluster

- Cluster Name
- Cluster Status
- Primary Node
- SSL Status
- Cluster Errors
- Topology Mode

## Nodes

- Status
- Version
- Role
- Member Role
- Replication Lag
- Address
- Read Replicas
- Mode

---

# Trigger Examples

- Cluster Status is NOT OK
- Node Offline
- Primary Node Changed
- Role Changed
- Mode Changed
- No Data Received

---

# Requirements

- Python 3.12+
- mysqlsh
- Zabbix 7.4+
- MySQL InnoDB Cluster

---

# Usage

Value mode

```bash
python3 InnoDB_Cluster_Monitoring.py value USER PASSWORD [node1,node2,node3]
```

Discovery mode

```bash
python3 InnoDB_Cluster_Monitoring.py discovery USER PASSWORD [node1,node2,node3]
```

---

# Logging

Logs are automatically rotated and stored under

```
/var/log/zabbix/MysqlInnodb/
```

---

# Future Improvements

- Environment variables
- Docker image
- TLS authentication
- Prometheus exporter
- Unit tests
- GitHub Actions

---

# Author

**Behzad Kianbakht**

Senior Software and Automation Engineer

🌐 Portfolio

https://www.kianbakht.com

Specialized in

- Python Automation
- Site Reliability Engineering
- Monitoring & Observability
- MySQL Administration
- DevOps
- AI & Machine Learning
