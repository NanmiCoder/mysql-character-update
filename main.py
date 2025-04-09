# -*- coding: utf-8 -*-
# Author        ：   程序员阿江-Relakkes
# Email         :    relakkes@gmail.com
# CreatedTime   ：   2024/07/29 02:41
# Desc          :    批量修改Mysql一个数据库中表、表字段的字符集

import asyncio
import logging
from typing import Dict, List, NoReturn

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

    def __init__(
        self, character_set: str = "utf8mb4", collate: str = "utf8mb4_general_ci"
    ):
        """
        初始化
        :param character_set: 字符集
        :param collate: 字符串比较和排序规则的
        """
        self.character_set = character_set
        self.collate = collate
        self.db: AsyncDbTransaction = AsyncDbTransaction(DB_CONFIG)
        self._need_update_field_type = [
            "longtext",
            "text",
            "tinytext",
            "char",
            "varchar",
            "json",
            "mediumtext",
        ]
        self.all_tables: List[str] = []

    async def fetch_tables(self):
        """
        查询数据库中所有的表名列表
        :return:
        """
        table_key = f"Tables_in_{config.DB_NAME}"
        records: List[Dict] = await self.db.query("show tables;")
        for item in records:
            table_name: str = item.get(table_key)
            if table_name.startswith("v_"):
                # 过滤掉视图
                continue
            self.all_tables.append(table_name)

    async def modify_table_charset(self) -> NoReturn:
        """
        修改数据库中所有tables的字符集
        :return:
        """
        for table_name in self.all_tables:
            logger.info(f"Table：{table_name} start modify charset")
            await self.db.execute(f"alter table `{table_name}` row_format=Dynamic;")
            sql: str = (
                f"ALTER TABLE `{table_name}` CONVERT TO CHARACTER SET {self.character_set} COLLATE {self.collate}"
            )
            await self.db.execute(sql)
            await self.modify_fields_charset(table_name)

    async def modify_fields_charset(self, table_name: str) -> NoReturn:
        """
        修改数据库中一张表字段的字符集
        :param table_name:
        :return:
        """
        fileds_list = await self.db.query(f"desc `{table_name}`;")
        fileds_name_list = [i.get("Field") for i in fileds_list]
        fileds_type_list = [i.get("Type") for i in fileds_list]
        for fname, ftype in zip(fileds_name_list, fileds_type_list):
            is_need_update: bool = self.check_current_filed_is_need_update(ftype)
            if is_need_update:
                sql: str = (
                    f"ALTER TABLE `{table_name}` CHANGE `{fname}` `{fname}` {ftype} CHARACTER SET {self.character_set} COLLATE {self.collate};"
                )
                try:
                    await self.db.execute(sql)
                except Exception as e:
                    logger.error(
                        f"failed sql:{sql}, err:{e}",
                    )

    def check_current_filed_is_need_update(self, current_filed: str) -> bool:
        """
        检查一个字段是否需要改变字符集
        :param current_filed:
        :return:
        """
        for need_filed_type in self._need_update_field_type:
            if need_filed_type.lower() == current_filed.lower():
                return True
        return False

    async def db_init(self) -> NoReturn:
        await self.db.begin()

    async def db_commit(self) -> NoReturn:
        await self.db.commit()

    async def run(self):
        await self.fetch_tables()
        await self.modify_table_charset()


async def main():
    mucs = MysqlUpdateCharacterSet(
        character_set="utf8mb4", collate="utf8mb4_general_ci"
    )
    await mucs.db_init()
    await mucs.run()
    await mucs.db_commit()


if __name__ == "__main__":
    # 替换旧的运行方式，Python 3.12中推荐直接使用asyncio.run()
    asyncio.run(main())
