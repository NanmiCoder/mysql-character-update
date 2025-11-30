# MySQL 字符集批量修改工具

一个用于批量修改 MySQL 数据库中表和字段字符集的高效工具。支持异步操作，可以快速将数据库中的表和字段统一转换为指定的字符集和排序规则。

## 功能特点

- 批量修改数据库中所有表的字符集
- 自动识别并修改需要更新字符集的字段
- 异步处理，提高执行效率
- 自动过滤视图，只处理实际的数据表
- **DRY-RUN 模式**：预览变更而不实际执行
- **执行统计**：运行完成后输出详细统计摘要
- **连接验证**：运行前自动验证数据库连接
- 详细的日志输出，方便追踪进度

## 环境要求

- Python 3.12+
- MySQL/MariaDB 数据库

## 安装说明

### 使用 uv 安装（推荐）

```bash
# 克隆仓库
git clone https://github.com/yourusername/mysql-character-update.git
cd mysql-character-update

# 使用 uv 同步依赖
uv sync

# 复制环境变量配置文件
cp .env.example .env

# 编辑 .env 文件，填入数据库连接信息
vim .env

# 运行程序
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
pip install aiomysql python-dotenv

# 复制并编辑配置文件
cp .env.example .env
```

## 配置说明

所有配置通过 `.env` 文件管理，复制 `.env.example` 并修改：

```bash
cp .env.example .env
```

### 配置项说明

```bash
# 数据库连接配置
DB_HOST=127.0.0.1          # 数据库主机地址
DB_PORT=3306               # 数据库端口
DB_USER=root               # 数据库用户名
DB_NAME=your_database_name # 数据库名称
DB_PASSWORD=your_password  # 数据库密码

# 字符集配置
DB_CHARSET=utf8mb4                    # 目标字符集
DB_COLLATION=utf8mb4_general_ci       # 目标排序规则
DB_ROW_FORMAT=Dynamic                 # 表行格式

# 过滤配置
VIEW_PREFIX=v_                        # 视图前缀（以此开头的表将被跳过）

# 字段类型配置（需要更新字符集的字段类型，逗号分隔）
FIELD_TYPES_TO_UPDATE=longtext,text,tinytext,char,varchar,json,mediumtext

# 执行模式
DRY_RUN=false                         # 设置为 true 时仅预览变更，不实际执行
```

## 使用方法

### 预览模式（推荐先执行）

在实际执行前，建议先使用预览模式查看将要执行的操作：

```bash
# 设置 DRY_RUN=true 或使用环境变量
DRY_RUN=true uv run main.py
```

预览模式下：
- 会显示所有将要执行的 SQL 语句
- 不会对数据库做任何实际修改
- 结束时会自动回滚事务

### 实际执行

确认预览结果无误后，执行实际修改：

```bash
uv run main.py
```

### 执行输出示例

```
2024-07-29 10:30:00 INFO main.py:59 Database connection validated: 127.0.0.1:3306/mydb
2024-07-29 10:30:00 INFO main.py:169 Found 50 tables to process
2024-07-29 10:30:00 INFO main.py:87 Table: users - start modify charset to utf8mb4
...
2024-07-29 10:30:15 INFO main.py:144 ==================================================
2024-07-29 10:30:15 INFO main.py:145 Execution Summary:
2024-07-29 10:30:15 INFO main.py:146   Mode: LIVE
2024-07-29 10:30:15 INFO main.py:147   Character Set: utf8mb4
2024-07-29 10:30:15 INFO main.py:148   Collation: utf8mb4_general_ci
2024-07-29 10:30:15 INFO main.py:149   Tables processed: 50
2024-07-29 10:30:15 INFO main.py:150   Tables skipped (views): 3
2024-07-29 10:30:15 INFO main.py:151   Fields updated: 120
2024-07-29 10:30:15 INFO main.py:152   Fields failed: 0
2024-07-29 10:30:15 INFO main.py:153 ==================================================
```

## 项目结构

```
mysql-character-update/
├── main.py          # 主程序入口，字符集修改逻辑
├── async_db.py      # 异步数据库事务层
├── config.py        # 配置管理（从 .env 读取）
├── .env.example     # 环境变量配置示例
├── .env             # 实际配置文件（不提交到 git）
├── pyproject.toml   # 项目依赖配置
└── README.md        # 项目文档
```

## 注意事项

- **执行前务必备份数据库**
- 确保数据库用户具有 ALTER TABLE 权限
- 对于大型数据库，执行时间可能较长
- 建议先使用 `DRY_RUN=true` 预览变更
- 表名和字段名已使用反引号处理，支持特殊字符

## 常见问题

**Q: 如何只修改特定类型的字段？**

修改 `.env` 中的 `FIELD_TYPES_TO_UPDATE` 配置项。

**Q: 如何跳过某些表？**

目前支持通过 `VIEW_PREFIX` 跳过以特定前缀开头的表。如需更复杂的过滤规则，可修改 `main.py` 中的 `fetch_tables` 方法。

**Q: 执行失败怎么办？**

程序使用事务处理，如果执行失败会自动回滚。查看日志中的错误信息，修复问题后重新执行即可。

**Q: 如何使用其他字符集？**

修改 `.env` 中的 `DB_CHARSET` 和 `DB_COLLATION` 配置项。

## License

MIT
