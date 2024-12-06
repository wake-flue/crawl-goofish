from typing import List, Dict, Any
from pymongo import MongoClient
from loguru import logger


class MongoDB:
    def __init__(self, uri: str, db_name: str, collection_name: str):
        """初始化MongoDB连接
        
        Args:
            uri: MongoDB连接URI
            db_name: 数据库名称
            collection_name: 集合名称
        """
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        logger.info(f"Connected to MongoDB: {db_name}.{collection_name}")

    def insert_many(self, documents: List[Dict[str, Any]]) -> int:
        """批量插入文档
        
        Args:
            documents: 文档列表
            
        Returns:
            插入的文档数量
        """
        if not documents:
            logger.warning("No documents to insert")
            return 0
        
        result = self.collection.insert_many(documents)
        logger.info(f"Inserted {len(result.inserted_ids)} documents")
        return len(result.inserted_ids)

    def find_all(self) -> List[Dict[str, Any]]:
        """获取所有文档
        
        Returns:
            文档列表
        """
        return list(self.collection.find())

    def close(self):
        """关闭数据库连接"""
        self.client.close()
        logger.info("MongoDB connection closed") 