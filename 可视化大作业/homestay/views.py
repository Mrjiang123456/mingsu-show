from django.shortcuts import render
import json
from django.http import JsonResponse
from .models import *
import pandas as pd
import numpy as np
from django.core.cache import cache
from django.db.models import Count, Avg, Sum
from django.views.decorators.cache import cache_page

# 缓存时间（秒）
CACHE_TIMEOUT = 60 * 15  # 15分钟

# Create your views here.

# 首页
def index(request):
    return render(request, 'index.html')

# 类别比较型图表可视化 - 区域民宿数量统计
@cache_page(CACHE_TIMEOUT)
def area_count(request):
    cache_key = 'area_count_data'
    data_list = cache.get(cache_key)
    
    if not data_list:
        # 如果缓存中没有数据，则从数据库获取
        data = AdsAreaCount.objects.all().values('district_name', 'count')
        data_list = list(data)
        
        # 将数据存入缓存
        cache.set(cache_key, data_list, CACHE_TIMEOUT)
    
    return render(request, 'area_count.html', {'data': json.dumps(data_list)})

# 数据关系型图表可视化 - 收藏与消费关系
@cache_page(CACHE_TIMEOUT)
def fav_consume_relation(request):
    cache_key = 'fav_consume_relation_data'
    data_list = cache.get(cache_key)
    
    if not data_list:
        # 优化查询，限制数据量
        data = AdsFavUseCount.objects.all().values('fav_count', 'consume_count')
        data_list = list(data)
        
        # 将数据存入缓存
        cache.set(cache_key, data_list, CACHE_TIMEOUT)
    
    return render(request, 'fav_consume_relation.html', {'data': json.dumps(data_list)})

# 数据分布型图表可视化 - 价格分布
@cache_page(CACHE_TIMEOUT)
def price_distribution(request):
    cache_key = 'price_distribution_data'
    data_list = cache.get(cache_key)
    
    if not data_list:
        data = AdsCostUseCount.objects.all().values('price', 'consume_count')
        data_list = list(data)
        cache.set(cache_key, data_list, CACHE_TIMEOUT)
    
    return render(request, 'price_distribution.html', {'data': json.dumps(data_list)})

# 时间系列型图表可视化 - 预订时间趋势
@cache_page(CACHE_TIMEOUT)
def booking_trend(request):
    cache_key = 'booking_trend_data'
    trend_list = cache.get(cache_key)
    
    if not trend_list:
        # 从日志信息中获取时间数据，限制数据量以提高性能
        logs = LogInfo.objects.all().values('create_time')[:5000]  # 限制查询数量
        
        # 转换为DataFrame进行时间序列分析
        df = pd.DataFrame(list(logs))
        if not df.empty and 'create_time' in df.columns:
            df['create_time'] = pd.to_datetime(df['create_time'])
            df['date'] = df['create_time'].dt.date
            # 按日期分组计数
            trend_data = df.groupby('date').size().reset_index()
            trend_data.columns = ['date', 'count']
            # 转换为列表
            trend_list = trend_data.to_dict('records')
            # 转换日期为字符串
            for item in trend_list:
                item['date'] = item['date'].strftime('%Y-%m-%d')
            
            # 将数据存入缓存
            cache.set(cache_key, trend_list, CACHE_TIMEOUT)
        else:
            trend_list = []
    
    return render(request, 'booking_trend.html', {'data': json.dumps(trend_list)})

# 局部整体型图表可视化 - 房间类型占比
@cache_page(CACHE_TIMEOUT)
def room_type_proportion(request):
    cache_key = 'room_type_proportion_data'
    data_list = cache.get(cache_key)
    
    if not data_list:
        # 修改字段名称
        data = AdsTypeCount.objects.all().values('layout_desc', 'count')
        # 转换字段名称以保持前端兼容性
        data_list = [{'room_type': item['layout_desc'], 'count': item['count']} for item in data]
        cache.set(cache_key, data_list, CACHE_TIMEOUT)
    
    return render(request, 'room_type_proportion.html', {'data': json.dumps(data_list)})

# 高维数据型图表可视化 - 标签、价格、评分多维分析
@cache_page(CACHE_TIMEOUT)
def multi_dimension_analysis(request):
    # 使用缓存提高性能
    tags_key = 'multi_dimension_tags'
    prices_key = 'multi_dimension_prices'
    rates_key = 'multi_dimension_rates'
    
    tags_list = cache.get(tags_key)
    prices_list = cache.get(prices_key)
    rates_list = cache.get(rates_key)
    
    if not tags_list:
        # 获取标签数据，限制数量提高性能，修改字段名
        tags = AdsTagMapCount.objects.all().order_by('-count')[:20].values('tag', 'count')
        # 转换字段名称以保持前端兼容性
        tags_list = [{'tag_name': item['tag'], 'count': item['count']} for item in tags]
        cache.set(tags_key, tags_list, CACHE_TIMEOUT)
    
    if not prices_list:
        # 获取价格数据
        prices = AdsCostUseCount.objects.all().values('price', 'consume_count')
        prices_list = list(prices)
        cache.set(prices_key, prices_list, CACHE_TIMEOUT)
    
    if not rates_list:
        # 获取评分数据
        rates = AdsRateUseCount.objects.all().values('star_rating', 'consume_count')
        # 转换字段名称以保持前端兼容性
        rates_list = [{'rate': item['star_rating'], 'consume_count': item['consume_count']} for item in rates]
        cache.set(rates_key, rates_list, CACHE_TIMEOUT)
    
    context = {
        'tags': json.dumps(tags_list),
        'prices': json.dumps(prices_list),
        'rates': json.dumps(rates_list)
    }
    
    return render(request, 'multi_dimension.html', context)

# 地理空间型图表可视化 - 区域分布地图
@cache_page(CACHE_TIMEOUT)
def geo_distribution(request):
    cache_key = 'geo_distribution_data'
    map_data = cache.get(cache_key)
    
    if not map_data:
        # 获取区域数据
        areas = AdsAreaCount.objects.all().values('district_name', 'count')
        
        # 广州各区域的大致经纬度（实际应用中应该从地理数据库获取）
        geo_data = {
            '越秀区': {'lat': 23.1289, 'lng': 113.2644},
            '天河区': {'lat': 23.1248, 'lng': 113.3619},
            '海珠区': {'lat': 23.0838, 'lng': 113.3172},
            '荔湾区': {'lat': 23.1259, 'lng': 113.2192},
            '白云区': {'lat': 23.1579, 'lng': 113.2632},
            '黄埔区': {'lat': 23.1039, 'lng': 113.4588},
            '番禺区': {'lat': 22.9394, 'lng': 113.3836},
            '花都区': {'lat': 23.4036, 'lng': 113.2203},
            '南沙区': {'lat': 22.8016, 'lng': 113.5257},
            '从化区': {'lat': 23.5485, 'lng': 113.5869},
            '增城区': {'lat': 23.2905, 'lng': 113.8295}
        }
        
        # 合并区域数据和地理位置
        map_data = []
        for area in areas:
            district = area['district_name']
            if district in geo_data:
                map_data.append({
                    'name': district,
                    'value': area['count'],
                    'lat': geo_data[district]['lat'],
                    'lng': geo_data[district]['lng']
                })
        
        cache.set(cache_key, map_data, CACHE_TIMEOUT)
    
    return render(request, 'geo_distribution.html', {'data': json.dumps(map_data)})

# API接口，返回JSON数据
@cache_page(CACHE_TIMEOUT)
def api_area_count(request):
    cache_key = 'api_area_count_data'
    data_list = cache.get(cache_key)
    
    if not data_list:
        data = AdsAreaCount.objects.all().values('district_name', 'count')
        data_list = list(data)
        cache.set(cache_key, data_list, CACHE_TIMEOUT)
    
    return JsonResponse(data_list, safe=False)

@cache_page(CACHE_TIMEOUT)
def api_price_distribution(request):
    cache_key = 'api_price_distribution_data'
    data_list = cache.get(cache_key)
    
    if not data_list:
        data = AdsCostUseCount.objects.all().values('price', 'consume_count')
        data_list = list(data)
        cache.set(cache_key, data_list, CACHE_TIMEOUT)
    
    return JsonResponse(data_list, safe=False)

@cache_page(CACHE_TIMEOUT)
def api_room_type(request):
    cache_key = 'api_room_type_data'
    data_list = cache.get(cache_key)
    
    if not data_list:
        # 修改字段名称
        data = AdsTypeCount.objects.all().values('layout_desc', 'count')
        # 转换字段名称以保持前端兼容性
        data_list = [{'room_type': item['layout_desc'], 'count': item['count']} for item in data]
        cache.set(cache_key, data_list, CACHE_TIMEOUT)
    
    return JsonResponse(data_list, safe=False)

@cache_page(CACHE_TIMEOUT)
def api_tag_count(request):
    cache_key = 'api_tag_count_data'
    data_list = cache.get(cache_key)
    
    if not data_list:
        # 修改字段名称
        data = AdsTagMapCount.objects.all().values('tag', 'count')
        # 转换字段名称以保持前端兼容性
        data_list = [{'tag_name': item['tag'], 'count': item['count']} for item in data]
        cache.set(cache_key, data_list, CACHE_TIMEOUT)
    
    return JsonResponse(data_list, safe=False)
