import json
import os
from loguru import logger

from database.mongodb import MongoDB
from analysis.analyzer import DataAnalyzer
from visualization.visualizer import DataVisualizer
from data.processor import JsonProcessor
from config.settings import (
    MONGODB_URI,
    MONGODB_DB,
    MONGODB_COLLECTION,
    LOG_CONFIG,
    RAW_DATA_DIR,
    OUTPUT_DIR
)

# 配置日志
logger.configure(**LOG_CONFIG)

def main():
    """主程序"""
    # 初始化db为None
    db = None

    # 处理JSON文件
    json_file = os.path.join(RAW_DATA_DIR, 'response.json')
    if not os.path.exists(json_file):
        logger.error(f"File not found: {json_file}")
        return

    try:
        # 使用JsonProcessor处理数据
        processor = JsonProcessor()
        items = processor.process_json_file(json_file)
        if not items:
            logger.error("No items found in the JSON file")
            return

        # 存储到MongoDB
        db = MongoDB(MONGODB_URI, MONGODB_DB, MONGODB_COLLECTION)
        db.insert_many(items)

        # 数据分析
        analyzer = DataAnalyzer(items)
        basic_stats = analyzer.basic_statistics()
        price_dist = analyzer.price_distribution()
        location_stats = analyzer.location_analysis()

        # 保存分析结果
        analysis_file = os.path.join(OUTPUT_DIR, 'analysis_results.json')
        with open(analysis_file, 'w', encoding='utf-8') as f:
            json.dump({
                'basic_stats': basic_stats,
                'price_distribution': price_dist,
                'location_analysis': location_stats
            }, f, ensure_ascii=False, indent=2)

        # 数据可视化
        visualizer = DataVisualizer(items, OUTPUT_DIR)
        visualizer.plot_price_distribution()
        visualizer.plot_location_distribution()
        visualizer.plot_category_distribution()
        visualizer.plot_price_by_location()

        logger.info("Data processing completed successfully")

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
    finally:
        if db is not None:
            db.close()


if __name__ == "__main__":
    main()
