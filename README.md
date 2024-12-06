# 闲鱼数据分析工具

这是一个用于分析闲鱼搜索结果数据的工具。该工具可以将JSON格式的搜索结果数据存入MongoDB数据库，并进行数据分析和可视化。

## 功能特点

- 解析闲鱼搜索结果JSON数据
- 数据存储到MongoDB数据库
- 数据分析功能：
  - 基础统计分析
  - 价格分布分析
  - 地理位置分析
  - 商品分类分析
  - 评价数据分析
- 数据可视化：
  - 价格分布图
  - 地区分布图
  - 商品类别分布图
  - 价格-地区关系图

## 环境要求

- Python 3.8+
- MongoDB 4.0+
- 相关Python包（见requirements.txt）

## 安装

1. 克隆仓库：
```bash
git clone [repository-url]
cd crawl-goofish
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置：
- 创建并配置`.env`文件：
  ```
  MONGODB_URI=mongodb://localhost:27017/
  MONGODB_DB=goofish_data
  MONGODB_COLLECTION=search_results
  ```
- 配置文件`config/settings.py`会自动处理：
  - MongoDB连接信息
  - 数据和日志目录的创建
  - 日志轮转和保留策略

## 项目结构

```
.
├── README.md
├── requirements.txt
├── .env                      # 环境变量配置
├── src/
│   ├── main.py              # 主程序入口
│   ├── analysis/            
│   │   └── analyzer.py      # 数据分析模块
│   ├── visualization/
│   │   └── visualizer.py    # 数据可视化模块
│   └── database/
│       └── mongodb.py       # MongoDB数据库操作
├── config/
│   └── settings.py          # 配置文件
├── data/
│   ├── raw/                 # 原始数据目录
│   │   └── response.json    # 闲鱼搜索结果数据
│   └── output/              # 输出目录
│       ├── analysis_results.json
│       ├── price_distribution.png
│       ├── location_distribution.png
│       ├── category_distribution.png
│       └── price_by_location.png
└── logs/                    # 日志目录
    └── app.log             # 应用日志文件
```

## 使用方法

1. 准备数据：
- 将闲鱼搜索结果的JSON文件保存为`data/raw/response.json`

2. 运行程序：
```bash
python src/main.py
```

3. 查看结果：
- 分析结果将保存在`data/output/analysis_results.json`
- 可视化图表将保存在`data/output/`目录下
- 数据将同时保存到MongoDB数据库中
- 运行日志将保存在`logs/app.log`中

## 数据分析结果

程序会生成以下分析结果：

1. 基础统计信息：
   - 商品总数
   - 价格统计（平均价格、最高价、最低价等）
   - 商品评价数据统计
   - 好评率分析

2. 分布分析：
   - 价格分布
   - 地区分布
   - 商品类别分布
   - 价格与地区关系分析

3. 可视化图表：
   - price_distribution.png：价格分布图
   - location_distribution.png：地区分布图
   - category_distribution.png：类别分布图
   - price_by_location.png：价格-地区关系图

## 注意事项

1. 确保MongoDB服务已启动
2. 确保response.json文件格式正确
3. 必要的目录结构（data/raw、data/output、logs）会在程序首次运行时自动创建
4. 日志文件会自动按天轮转，默认保留最近7天的日志

## 许可证

MIT License