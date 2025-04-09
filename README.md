# MySQL 字符集批量修改工具

一个用于批量修改 MySQL 数据库中表和字段字符集的高效工具。支持异步操作，可以快速将数据库中的表和字段统一转换为指定的字符集和排序规则。

## 功能特点

- 批量修改数据库中所有表的字符集
- 自动识别并修改需要更新字符集的字段
- 异步处理，提高执行效率
- 自动过滤视图，只处理实际的数据表
- 详细的日志输出，方便追踪进度

## 环境要求

- Python 3.9+（推荐 Python 3.12）
- MySQL/MariaDB 数据库

## 安装说明

### 使用 uv 安装（推荐）

```bash
# 克隆仓库
git clone https://github.com/yourusername/mysql-character-update.git
cd mysql-character-update

# 使用 uv 创建虚拟环境并安装依赖
uv init
uv pip install aiomysql
uv run main.py
```

### 使用 pip 安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/mysql-character-update.git
cd mysql-character-update

# 创建虚拟环境并安装依赖
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# 或 .venv\Scripts\activate  # Windows
pip install aiomysql
```

## 配置说明

修改 `config.py` 文件，配置数据库连接信息：

```python
import os

DB_HOST = "127.0.0.1"  # 数据库主机地址
DB_PORT = 3306         # 数据库端口
DB_USER = os.getenv("DB_USER", "root")  # 数据库用户名
DB_NAME = os.getenv("DB_NAME", "your_database_name")  # 数据库名称
DB_PASSWORD = os.getenv("DB_PASSWORD", "your_password")  # 数据库密码
```

您可以通过环境变量设置这些配置项，或直接修改默认值。

## 使用方法

1. 配置好数据库连接信息后，直接运行主程序：

```bash
python main.py
```

2. 程序将自动：
   - 连接到指定的数据库
   - 获取所有数据表（排除视图）
   - 将每个表的字符集修改为 `utf8mb4`
   - 将表中的文本类型字段字符集修改为 `utf8mb4`
   - 在控制台输出详细的执行日志

## 自定义字符集和排序规则

如果需要使用非默认的字符集和排序规则，可以修改 `main.py` 中的相关参数：

```python
mucs = MysqlUpdateCharacterSet(
    character_set="utf8mb4",  # 修改为您需要的字符集
    collate="utf8mb4_general_ci"  # 修改为您需要的排序规则
)
```

## 注意事项

- 执行前建议备份数据库
- 确保数据库用户具有修改表结构的权限
- 对于大型数据库，执行时间可能较长
- 表名中包含特殊字符的表已做处理，不会出现语法错误

## 常见问题

- 如果遇到权限问题，请检查数据库用户权限
- 如果遇到连接问题，请检查网络和数据库服务是否正常运行
- 程序会自动跳过处理视图，只处理实际的数据表