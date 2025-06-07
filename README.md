# 民宿可视化系统

基于Django的民宿数据可视化系统，展示各种类型的可视化图表。

## 功能特点

- 类别比较型图表 - 区域民宿统计
- 数据关系型图表 - 收藏消费关系
- 数据分布型图表 - 价格分布
- 时间系列型图表 - 预订时间趋势
- 局部整体型图表 - 房间类型占比
- 高维数据型图表 - 多维数据分析
- 地理空间型图表 - 区域分布地图

## 技术栈

- 后端：Django
- 数据处理：Pandas, NumPy
- 前端可视化：ECharts
- 数据库：MySQL

## 安装与运行

1. 克隆项目
2. 安装依赖：`pip install -r requirements.txt`
3. 导入数据库：`mysql -u root -p < ana_homestay_db.sql`
4. 修改数据库配置：在`可视化大作业/settings.py`中配置数据库连接信息
5. 运行项目：`python manage.py runserver`
6. 访问：http://localhost:8000

## 项目结构

- `homestay/`: 主应用目录
  - `models.py`: 数据模型
  - `views.py`: 视图函数
- `templates/`: 模板文件
- `static/`: 静态文件
- `可视化大作业/`: 项目配置文件
- `ana_homestay_db.sql`: 数据库文件 
