## HTML Page Analyzer

### Tests and linter status:
[![Actions Status](https://github.com/INafanya/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/INafanya/python-project-83/actions)
[![Python CI](https://github.com/INafanya/python-project-83/actions/workflows/pyci.yaml/badge.svg)](https://github.com/INafanya/python-project-83/actions/workflows/pyci.yaml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=INafanya_python-project-83&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=INafanya_python-project-83)

---

### **Project Overview**

This is a Flask web application for analyzing websites for accessibility and obtaining SEO data such as headers, descriptions, and h1 tags.
PostgresSQL is used for data storage.

### **Features**
- URL availability check.
- Analysis of title and description tags.
- Display of check results on the user interface.

### **Demo**

[Page Analyzer Demo](https://python-project-83-fvmx.onrender.com)

---

### **Technologies**

- Python
- Flask
- PostgreSQL
- HTML/CSS
- Bootstrap
---

### **Requirements**

- python 3.12+
- flask 3.1.2+
- psycopg2-binary 2.9.10+
- python-dotenv 1.1.1+
- requests 2.32.5+
- validators 0.35.0+
- bs4 0.0.2+
- gunicorn 23.0.0+

---

### **Installation**

```
git clone git@github.com:INafanya/python-project-83.git
```
```
cd python-project-83
```
```
make install
```
For migration add DATABASE_URL and SECRET_KEY in .env file or set in Environment Variables

.env
```
DATABASE_URL=postgresql://username:password@host:5432/database_name
SECRET_KEY='you_sectret_key'
```
Launch Options:

1. Run on local development
```
make dev
```
2. Run on production
```
make start
```
3. Run on PASS-service render.com
```
make build
```
```
make render-start
```
---
