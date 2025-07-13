# Python Generators Project
This project focuses on advanced usage of **Python generators** to process large datasets efficiently, implement batch and lazy loading, and perform memory-efficient computations with real-world data.
## 📚 Learning Objectives

- Create and utilize Python generators using `yield`.
- Work with SQL databases using Python (`mysql-connector-python`).
- Efficiently process large datasets in batches.
- Perform lazy pagination using generators.
- Compute aggregate functions (like average) using streaming.
- Integrate SQL queries into Python applications.

## 🗂️ Project Structure

| File | Description |
|------|-------------|
| `seed.py` | Creates and seeds MySQL database `ALX_prodev` with table `user_data`. |
| `user_data.csv` | Sample dataset containing user_id, name, email, and age. |
| `0-stream_users.py` | Streams all rows from `user_data` one by one using a generator. |
| `1-batch_processing.py` | Processes data in batches and filters users over age 25. |
| `2-lazy_paginate.py` | Lazily paginates users with a generator and fetches page by page. |
| `4-stream_ages.py` | Calculates average user age using a generator. |

## ✅ Setup Instructions

1. Install MySQL and ensure it's running.
2. Create a MySQL user with access privileges, or use `root`.
3. Update the credentials in `seed.py` (`user`, `password`) if needed.
4. Install dependencies:

```bash
pip install mysql-connector-python
