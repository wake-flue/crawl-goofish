from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from datetime import datetime
import json

@dataclass
class Item:
    """商品基础类，用于存储和管理商品信息
    
    Attributes:
        item_id: 商品ID
        title: 商品标题
        price: 商品价格
        description: 商品描述
        url: 商品链接
        created_at: 创建时间
        updated_at: 更新时间
        
        # 基础商品信息
        category_id: 商品分类ID
        tb_category_id: 淘宝分类ID
        publish_time: 发布时间
        item_type: 商品类型
        
        # 卖家信息
        seller_id: 卖家ID
        seller_nick: 卖家昵称
        seller_avatar: 卖家头像
        seller_rating: 卖家评分
        seller_reviews_count: 卖家评价数
        seller_good_rating: 卖家好评率
        
        # 商品状态
        want_count: 想要人数
        is_free_shipping: 是否包邮
        
        # 图片信息
        pic_url: 主图URL
        
        # 位置信息
        location: 商品所在地
        
        # 价格信息
        original_price: 原价
        current_price: 当前价格
        
        # 其他元数据
        keyword: 搜索关键词
        search_id: 搜索ID
        biz_type: 业务类型
        
        extra_attributes: 额外的属性字典
    """
    # 必需的基础属性
    item_id: str
    title: str
    price: float
    
    # 可选的基础属性
    description: Optional[str] = None
    url: Optional[str] = None
    
    # 时间相关
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    publish_time: Optional[int] = None
    
    # 分类信息
    category_id: Optional[str] = None
    tb_category_id: Optional[str] = None
    item_type: Optional[str] = None
    
    # 卖家信息
    seller_id: Optional[str] = None
    seller_nick: Optional[str] = None
    seller_avatar: Optional[str] = None
    seller_rating: Optional[str] = None
    seller_reviews_count: Optional[int] = None
    seller_good_rating: Optional[str] = None
    
    # 商品状态
    want_count: Optional[int] = None
    is_free_shipping: bool = False
    
    # 图片信息
    pic_url: Optional[str] = None
    
    # 位置信息
    location: Optional[str] = None
    
    # 价格信息
    original_price: Optional[str] = None
    current_price: Optional[float] = None
    
    # 元数据
    keyword: Optional[str] = None
    search_id: Optional[str] = None
    biz_type: Optional[str] = None
    
    # 扩展属性
    extra_attributes: Dict[str, Any] = field(default_factory=dict)

    def update(self, **kwargs) -> None:
        """更新商品属性"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                self.extra_attributes[key] = value
        self.updated_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """将商品对象转换为字典"""
        base_dict = {
            'item_id': self.item_id,
            'title': self.title,
            'price': self.price,
            'description': self.description,
            'url': self.url,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'publish_time': self.publish_time,
            'category_id': self.category_id,
            'tb_category_id': self.tb_category_id,
            'item_type': self.item_type,
            'seller_id': self.seller_id,
            'seller_nick': self.seller_nick,
            'seller_avatar': self.seller_avatar,
            'seller_rating': self.seller_rating,
            'seller_reviews_count': self.seller_reviews_count,
            'seller_good_rating': self.seller_good_rating,
            'want_count': self.want_count,
            'is_free_shipping': self.is_free_shipping,
            'pic_url': self.pic_url,
            'location': self.location,
            'original_price': self.original_price,
            'current_price': self.current_price,
            'keyword': self.keyword,
            'search_id': self.search_id,
            'biz_type': self.biz_type
        }
        return {**base_dict, **self.extra_attributes}

    def to_json(self) -> str:
        """将商品对象转换为JSON字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Item':
        """从字典创建商品对象"""
        # 提取基本属性
        base_attrs = {
            'item_id': data.pop('item_id'),
            'title': data.pop('title'),
            'price': data.pop('price'),
            'description': data.pop('description', None),
            'url': data.pop('url', None),
            'publish_time': data.pop('publish_time', None),
            'category_id': data.pop('category_id', None),
            'tb_category_id': data.pop('tb_category_id', None),
            'item_type': data.pop('item_type', None),
            'seller_id': data.pop('seller_id', None),
            'seller_nick': data.pop('seller_nick', None),
            'seller_avatar': data.pop('seller_avatar', None),
            'seller_rating': data.pop('seller_rating', None),
            'seller_reviews_count': data.pop('seller_reviews_count', None),
            'seller_good_rating': data.pop('seller_good_rating', None),
            'want_count': data.pop('want_count', None),
            'is_free_shipping': data.pop('is_free_shipping', False),
            'pic_url': data.pop('pic_url', None),
            'location': data.pop('location', None),
            'original_price': data.pop('original_price', None),
            'current_price': data.pop('current_price', None),
            'keyword': data.pop('keyword', None),
            'search_id': data.pop('search_id', None),
            'biz_type': data.pop('biz_type', None)
        }
        
        # 处理时间字段
        if 'created_at' in data:
            base_attrs['created_at'] = datetime.fromisoformat(data.pop('created_at'))
        if 'updated_at' in data:
            base_attrs['updated_at'] = datetime.fromisoformat(data.pop('updated_at'))
            
        # 剩余的属性作为extra_attributes
        return cls(**base_attrs, extra_attributes=data)

    @classmethod
    def from_json(cls, json_str: str) -> 'Item':
        """从JSON字符串创建商品对象"""
        return cls.from_dict(json.loads(json_str)) 