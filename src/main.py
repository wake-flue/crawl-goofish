import json
import os
from loguru import logger

from database.mongodb import MongoDB
from analysis.analyzer import DataAnalyzer
from visualization.visualizer import DataVisualizer
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

def process_json_file(file_path: str) -> list:
    """处理JSON文件
    
    Args:
        file_path: JSON文件路径
        
    Returns:
        处理后的数据列表
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 提取搜索关键词
    keyword = data.get('data', {}).get('resultInfo', {}).get('sqiControlFields', {}).get('userInputOriginalSearchKeywords', '')
    
    # 提取商品数据
    items = data.get('data', {}).get('resultList', {})
    
    processed_items = []
    
    for item in items:

        item_main = item.get('data', {}).get('item', {}).get('main', {})
        # 从exContent中提取数据
        ex_content = item_main.get('exContent', {})
        
        processed_item = {
            'item_id': ex_content.get('itemId'),
            'title': ex_content.get('title'),
            'price': float(ex_content.get('price', [{'text': '0'}, {'text': '0'}])[1].get('text', '0')), # 获取价格数字部分
            'location': ex_content.get('area'),
            'description': ex_content.get('title'), # 由于数据结构中没有单独的description字段,使用title作为描述
            'seller_nick': ex_content.get('userNickName'),
            'category': item_main.get('clickParam', {}).get('args', {}).get('cCatId'), # 使用分类ID
            'keyword': keyword,
            # 额外的有用信息
            'want_count': ex_content.get('userFishShopLabel', {}).get('tagList', [{}])[0].get('data', {}).get('content', '0条评价').replace('条评价', ''),
            'good_rating': ex_content.get('userFishShopLabel', {}).get('tagList', [{}])[1].get('data', {}).get('content', '0%').replace('好评率', ''),
            'original_price': ex_content.get('oriPrice', '').replace('¥', ''),
            'pic_url': ex_content.get('picUrl')
        }
        processed_items.append(processed_item)
    
    return processed_items

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
        # 处理数据
        items = process_json_file(json_file)
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