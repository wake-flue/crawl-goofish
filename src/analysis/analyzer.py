from typing import Dict, Any, List
import pandas as pd
import numpy as np
from loguru import logger


class DataAnalyzer:
    def __init__(self, data: List[Dict[str, Any]]):
        """初始化数据分析器
        
        Args:
            data: 要分析的数据列表
        """
        self.df = pd.DataFrame(data)
        logger.info(f"Loaded {len(self.df)} records for analysis")

    def basic_statistics(self) -> Dict[str, Any]:
        """计算基础统计信息
        
        Returns:
            包含统计信息的字典
        """
        if self.df.empty:
            logger.warning("No data available for analysis")
            return {"error": "No data available"}

        stats = {
            "total_items": len(self.df),
            "price_stats": {
                "mean": float(self.df['price'].mean()),
                "median": float(self.df['price'].median()),
                "min": float(self.df['price'].min()),
                "max": float(self.df['price'].max()),
                "std": float(self.df['price'].std())
            },
            "top_locations": self.df['location'].value_counts().head(5).to_dict(),
            "top_categories": self.df['category_id'].value_counts().head(5).to_dict(),
            "keywords_summary": self.df['keyword'].value_counts().to_dict()
        }

        logger.info("Basic statistics calculated successfully")
        return stats

    def price_distribution(self) -> Dict[str, Any]:
        """分析价格分布
        
        Returns:
            价格分布统计信息
        """
        if self.df.empty:
            return {"error": "No data available"}
            
        # 计算价格区间
        bins = pd.cut(self.df['price'], bins=10)
        price_ranges = bins.value_counts().sort_index()
        
        # 将Interval对象转换为字符串格式
        price_ranges_dict = {
            f"{interval.left:.2f}-{interval.right:.2f}": count 
            for interval, count in price_ranges.items()
        }

        price_dist = {
            "percentiles": {
                "25%": float(self.df['price'].quantile(0.25)),
                "50%": float(self.df['price'].quantile(0.50)),
                "75%": float(self.df['price'].quantile(0.75))
            },
            "price_ranges": price_ranges_dict
        }

        logger.info("Price distribution analysis completed")
        return price_dist

    def location_analysis(self) -> Dict[str, Any]:
        """分析地理位置分布
        
        Returns:
            地理位置分布统计信息
        """
        if self.df.empty:
            return {"error": "No data available"}

        location_stats = {
            "location_counts": self.df['location'].value_counts().to_dict(),
            "location_price_avg": self.df.groupby('location')['price'].mean().to_dict()
        }

        logger.info("Location analysis completed")
        return location_stats 