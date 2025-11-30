# -*- coding: utf-8 -*-
# Author        ：   程序员阿江-Relakkes
# Email         :    relakkes@gmail.com
# CreatedTime   ：   2024/07/29 02:41
# Desc          :    批量修改Mysql一个数据库中表、表字段的字符集

import asyncio
import logging
from typing import Dict, List

import config
from async_db import AsyncDbTransaction

logging.basicConfig(
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s",
)
logger = logging.getLogger(__name__)

DB_CONFIG = dict(
    host=config.DB_HOST,
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    db=config.DB_NAME,
    port=config.DB_PORT,
)


class MysqlUpdateCharacterSet:

    def __init__(self):
        """
        初始化，从配置文件读取字符集设置
        """
        self.character_set = config.CHARSET
        self.collate = config.COLLATION
        self.row_format = config.ROW_FORMAT
        self.view_prefix = config.VIEW_PREFIX
        self.dry_run = config.DRY_RUN
        self.db: AsyncDbTransaction = AsyncDbTransaction(DB_CONFIG)
        self._need_update_field_type = config.FIELD_TYPES_TO_UPDATE
        self.all_tables: List[str] = []
        # Statistics
        self.stats = {
            "tables_processed": 0,
            "tables_skipped": 0,
            "fields_updated": 0,
            "fields_failed": 0,
        }

    async def validate_connection(self) -> bool:
        """
        验证数据库连接
        :return: 连接是否成功
        """
        try:
            await self.db.query("SELECT 1")
            logger.info(f"Database connection validated: {config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}")
            return True
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            return False

    async def fetch_tables(self):
        """
        查询数据库中所有的表名列表
        :return:
        """
        table_key = f"Tables_in_{config.DB_NAME}"
        records: List[Dict] = await self.db.query("show tables;")
        for item in records:
            table_name: str = item.get(table_key)
            if table_name.startswith(self.view_prefix):
                logger.debug(f"Skipping view: {table_name}")
                self.stats["tables_skipped"] += 1
                continue
            self.all_tables.append(table_name)

    async def modify_table_charset(self) -> None:
        """
        修改数据库中所有tables的字符集
        :return:
        """
        for table_name in self.all_tables:
            prefix = "[DRY-RUN] " if self.dry_run else ""
            logger.info(f"{prefix}Table: {table_name} - start modify charset to {self.character_set}")

            if not self.dry_run:
                try:
                    await self.db.execute(f"ALTER TABLE `{table_name}` ROW_FORMAT={self.row_format};")
                    sql: str = (
                        f"ALTER TABLE `{table_name}` CONVERT TO CHARACTER SET {self.character_set} COLLATE {self.collate}"
                    )
                    await self.db.execute(sql)
                except Exception as e:
                    logger.error(f"Failed to modify table {table_name}: {e}")
                    continue

            await self.modify_fields_charset(table_name)
            self.stats["tables_processed"] += 1

    async def modify_fields_charset(self, table_name: str) -> None:
        """
        修改数据库中一张表字段的字符集
        :param table_name:
        :return:
        """
        fields_list = await self.db.query(f"DESC `{table_name}`;")
        fields_name_list = [i.get("Field") for i in fields_list]
        fields_type_list = [i.get("Type") for i in fields_list]
        for fname, ftype in zip(fields_name_list, fields_type_list):
            is_need_update: bool = self.check_current_field_is_need_update(ftype)
            if is_need_update:
                sql: str = (
                    f"ALTER TABLE `{table_name}` CHANGE `{fname}` `{fname}` {ftype} "
                    f"CHARACTER SET {self.character_set} COLLATE {self.collate};"
                )
                if self.dry_run:
                    logger.info(f"[DRY-RUN] Would execute: {sql}")
                    self.stats["fields_updated"] += 1
                else:
                    try:
                        await self.db.execute(sql)
                        self.stats["fields_updated"] += 1
                    except Exception as e:
                        logger.error(f"Failed sql: {sql}, err: {e}")
                        self.stats["fields_failed"] += 1

    def check_current_field_is_need_update(self, current_field: str) -> bool:
        """
        检查一个字段是否需要改变字符集
        :param current_field:
        :return:
        """
        current_field_lower = current_field.lower()
        for need_field_type in self._need_update_field_type:
            if current_field_lower.startswith(need_field_type):
                return True
        return False

    def print_summary(self):
        """打印执行统计"""
        logger.info("=" * 50)
        logger.info("Execution Summary:")
        logger.info(f"  Mode: {'DRY-RUN' if self.dry_run else 'LIVE'}")
        logger.info(f"  Character Set: {self.character_set}")
        logger.info(f"  Collation: {self.collate}")
        logger.info(f"  Tables processed: {self.stats['tables_processed']}")
        logger.info(f"  Tables skipped (views): {self.stats['tables_skipped']}")
        logger.info(f"  Fields updated: {self.stats['fields_updated']}")
        logger.info(f"  Fields failed: {self.stats['fields_failed']}")
        logger.info("=" * 50)

    async def db_init(self) -> None:
        await self.db.begin()

    async def db_commit(self) -> None:
        if self.dry_run:
            logger.info("[DRY-RUN] Rolling back - no changes made")
            await self.db.rollback()
        else:
            await self.db.commit()

    async def run(self):
        if not await self.validate_connection():
            raise ConnectionError("Failed to connect to database")
        await self.fetch_tables()
        logger.info(f"Found {len(self.all_tables)} tables to process")
        await self.modify_table_charset()
        self.print_summary()


async def main():
    mucs = MysqlUpdateCharacterSet()
    await mucs.db_init()
    await mucs.run()
    await mucs.db_commit()


if __name__ == "__main__":
    asyncio.run(main())
