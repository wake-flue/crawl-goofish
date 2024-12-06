from typing import List, Dict, Any
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from loguru import logger
from matplotlib import font_manager


class DataVisualizer:
    def __init__(self, data: List[Dict[str, Any]], output_dir: str = "data/output"):
        """初始化数据可视化器
        
        Args:
            data: 要可视化的数据列表
            output_dir: 输出目录
        """
        self.df = pd.DataFrame(data)
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self._setup_plot_style()
        logger.info(f"Initialized visualizer, output directory: {output_dir}")
    
    def _setup_plot_style(self):
        """设置图表全局样式"""
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        plt.rcParams['axes.unicode_minus'] = False
        
    def _save_plot(self, filename: str, tight_layout: bool = True) -> str:
        """保存图表到文件
        
        Args:
            filename: 文件名
            tight_layout: 是否使用紧凑布局
            
        Returns:
            保存的文件路径
        """
        if tight_layout:
            plt.tight_layout()
        
        output_path = os.path.join(self.output_dir, filename)
        plt.savefig(output_path)
        plt.close()
        
        logger.info(f"Plot saved to {output_path}")
        return output_path

    def plot_price_distribution(self) -> str:
        """绘制价格分布图
        
        Returns:
            保存的文件路径
        """
        plt.figure(figsize=(12, 6))
        sns.histplot(data=self.df, x='price', bins=30)
        plt.title('商品价格分布')
        plt.xlabel('价格')
        plt.ylabel('数量')
        
        return self._save_plot('price_distribution.png')

    def plot_location_distribution(self) -> str:
        """绘制地理位置分布图
        
        Returns:
            保存的文件路径
        """
        plt.figure(figsize=(12, 6))
        location_counts = self.df['location'].value_counts().head(10)
        location_counts.plot(kind='bar')
        plt.title('Top 10 地区分布')
        plt.xlabel('地区')
        plt.ylabel('数量')
        plt.xticks(rotation=45)
        
        return self._save_plot('location_distribution.png')

    def plot_category_distribution(self) -> str:
        """绘制类别分布图
        
        Returns:
            保存的文件路径
        """
        plt.figure(figsize=(12, 6))
        category_counts = self.df['category'].value_counts().head(10)
        category_counts.plot(kind='bar')
        plt.title('Top 10 类别分布')
        plt.xlabel('类别')
        plt.ylabel('数量')
        plt.xticks(rotation=45)
        
        return self._save_plot('category_distribution.png')

    def plot_price_by_location(self) -> str:
        """绘制各地区价格分布图
        
        Returns:
            保存的文件路径
        """
        plt.figure(figsize=(12, 6))
        sns.boxplot(data=self.df, x='location', y='price')
        plt.title('各地区价格分布')
        plt.xlabel('地区')
        plt.ylabel('价格')
        plt.xticks(rotation=45)
        
        return self._save_plot('price_by_location.png')