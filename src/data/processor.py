import json
from typing import List, Dict, Any, Optional
from pathlib import Path
from loguru import logger
from models.item import Item


class JsonProcessor:
    """JSON数据处理器"""
    
    @staticmethod
    def read_json_file(file_path: str) -> Optional[Dict[str, Any]]:
        """读取JSON文件
        
        Args:
            file_path: JSON文件路径
            
        Returns:
            解析后的JSON数据,如果出错则返回None
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                logger.error(f"File not found: {file_path}")
                return None
                
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                logger.info(f"Successfully read JSON file: {file_path}")
                return data
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON file {file_path}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {str(e)}")
            return None

    @staticmethod
    def process_items(data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """处理闲鱼商品数据
        
        Args:
            data: 原始JSON数据
            
        Returns:
            处理后的商品列表
        """
        try:
            # 提取搜索关键词
            keyword = data.get('data', {}).get('resultInfo', {}).get('sqiControlFields', {}).get(
                'userInputOriginalSearchKeywords', '')

            # 提取商品数据
            items = data.get('data', {}).get('resultList', {})
            if not items:
                logger.warning("No items found in data")
                return []

            processed_items = []
            for item in items:
                try:
                    item_main = item.get('data', {}).get('item', {}).get('main', {})
                    ex_content = item_main.get('exContent', {})
                    click_param = item_main.get('clickParam', {}).get('args', {})

                    # 提取价格信息
                    price_info = ex_content.get('price', [{'text': '0'}, {'text': '0'}])
                    price = float(price_info[1].get('text', '0'))

                    # 提取评价信息
                    user_fish_shop_label = ex_content.get('userFishShopLabel', {}).get('tagList', [])
                    reviews_count = user_fish_shop_label[0].get('data', {}).get('content', '0条评价').replace('条评价',
                                                                                                           '') if user_fish_shop_label else '0'
                    good_rating = user_fish_shop_label[1].get('data', {}).get('content', '0%').replace('好评率', '') if len(
                        user_fish_shop_label) > 1 else '0%'
                    
                    # 提取想要人数
                    want_count_content = ex_content.get('fishTags', {}).get('r3', {}).get('tagList', [{}])[0].get('data', {}).get('content', '0')

                    # 创建Item对象
                    item_obj = Item(
                        item_id=ex_content.get('itemId'),
                        title=ex_content.get('title'),
                        price=price,
                        description='',
                        url=ex_content.get('picUrl')
                    )

                    # 更新所有额外属性
                    item_obj.update(
                        # 分类信息
                        category_id=click_param.get('cCatId'),
                        tb_category_id=click_param.get('tbCatId'),
                        item_type=click_param.get('item_type'),

                        # 卖家信息
                        seller_id=click_param.get('seller_id'),
                        seller_nick=ex_content.get('userNickName'),
                        seller_avatar=ex_content.get('userAvatarUrl'),
                        seller_reviews_count=int(reviews_count) if reviews_count.isdigit() else 0,
                        seller_good_rating=good_rating,

                        # 想要人数
                        want_count=want_count_content.replace('人想要', '') if '人想要' in want_count_content else '0',

                        # 商品状态
                        is_free_shipping='freeship' in (click_param.get('tag', '') or ''),

                        # 图片信息
                        pic_url=ex_content.get('picUrl'),

                        # 位置信息
                        location=ex_content.get('area'),

                        # 价格信息
                        original_price=ex_content.get('oriPrice', '').replace('¥', ''),
                        current_price=price,

                        # 元数据
                        keyword=keyword,
                        search_id=click_param.get('search_id'),
                        biz_type=click_param.get('biz_type'),
                        publish_time=int(click_param.get('publishTime', 0))
                    )

                    # 将Item对象转换为字典并添加到列表
                    processed_items.append(item_obj.to_dict())
                except Exception as e:
                    logger.error(f"Error processing item: {str(e)}")
                    continue

            logger.info(f"Successfully processed {len(processed_items)} items")
            return processed_items
        except Exception as e:
            logger.error(f"Error processing items: {str(e)}")
            return []

    @classmethod
    def process_json_file(cls, file_path: str) -> List[Dict[str, Any]]:
        """处理JSON文件并返回商品列表
        
        Args:
            file_path: JSON文件路径
            
        Returns:
            处理后的商品列表
        """
        # 读取JSON文件
        data = cls.read_json_file(file_path)
        if not data:
            return []
            
        # 处理商品数据
        return cls.process_items(data) 