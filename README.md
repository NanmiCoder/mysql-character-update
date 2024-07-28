## Overview
This project is designed to batch modify the character set of tables and table fields in a MySQL database. The project is written in Python and uses the `aiomysql` library for asynchronous database operations.

## File Structure
- `config.py`: Configuration file containing database connection settings.
- `main.py`: Main program file containing the primary logic for character set modification.
- `async_db.py`: Asynchronous database operation class, encapsulating common database operation methods.

## Dependencies Installation
Before running the project, ensure the following dependencies are installed:
```bash
pip install aiomysql
```
Python version 3.7 or higher is required.

## Usage
1. Configure the database connection information in `config.py`.
2. Execute the following command:
    ```bash
    python main.py
    ```
    
    The program will output the results of the character set modification operations.
    ```plaintext
    2024-07-29 03:03:27 INFO main.py:70 Table：xxx_table1_name start modify charset
    2024-07-29 03:03:27 INFO main.py:70 Table：xxx_table2_name start modify charset
    2024-07-29 03:03:27 INFO main.py:70 Table：xxx_table3_name start modify charset
    2024-07-29 03:03:27 INFO main.py:70 Table：xxx_table4_name start modify charset
    2024-07-29 03:03:27 INFO main.py:70 Table：xxx_table5_name start modify charset
    ...
    ```
   