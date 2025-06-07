/**
 * 图表工具类 - 用于优化图表加载和数据处理
 */

// 数据缓存对象
const DataCache = {
    cache: {},
    
    // 设置缓存
    set: function(key, data, expireMinutes = 5) {
        const expireTime = new Date().getTime() + (expireMinutes * 60 * 1000);
        this.cache[key] = {
            data: data,
            expireTime: expireTime
        };
        // 保存到本地存储
        try {
            localStorage.setItem('chart_data_' + key, JSON.stringify({
                data: data,
                expireTime: expireTime
            }));
        } catch (e) {
            console.warn('无法保存到本地存储:', e);
        }
    },
    
    // 获取缓存
    get: function(key) {
        // 先尝试从内存缓存获取
        const cached = this.cache[key];
        if (cached && cached.expireTime > new Date().getTime()) {
            return cached.data;
        }
        
        // 再尝试从本地存储获取
        try {
            const localData = localStorage.getItem('chart_data_' + key);
            if (localData) {
                const parsed = JSON.parse(localData);
                if (parsed.expireTime > new Date().getTime()) {
                    // 同步到内存缓存
                    this.cache[key] = parsed;
                    return parsed.data;
                }
            }
        } catch (e) {
            console.warn('无法从本地存储读取:', e);
        }
        
        return null;
    },
    
    // 清除缓存
    clear: function(key) {
        if (key) {
            delete this.cache[key];
            localStorage.removeItem('chart_data_' + key);
        } else {
            this.cache = {};
            // 清除所有图表相关的本地存储
            Object.keys(localStorage).forEach(key => {
                if (key.startsWith('chart_data_')) {
                    localStorage.removeItem(key);
                }
            });
        }
    }
};

// 图表工具类
const ChartUtils = {
    // 延迟加载的图表队列
    chartQueue: [],
    
    // 初始化所有图表延迟加载
    initLazyLoad: function() {
        // 监听滚动事件
        window.addEventListener('scroll', this.checkChartsInView.bind(this));
        window.addEventListener('resize', this.checkChartsInView.bind(this));
        
        // 初始检查
        setTimeout(this.checkChartsInView.bind(this), 100);
    },
    
    // 添加图表到延迟加载队列
    addToLazyLoad: function(chartId, initFunction) {
        this.chartQueue.push({
            id: chartId,
            init: initFunction,
            loaded: false
        });
    },
    
    // 检查图表是否在视图中
    checkChartsInView: function() {
        this.chartQueue.forEach(chart => {
            if (!chart.loaded) {
                const element = document.getElementById(chart.id);
                if (element && this.isInViewport(element)) {
                    chart.init();
                    chart.loaded = true;
                }
            }
        });
    },
    
    // 检查元素是否在视图中
    isInViewport: function(element) {
        const rect = element.getBoundingClientRect();
        return (
            rect.top <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.bottom >= 0
        );
    },
    
    // 异步加载数据
    loadData: function(url, params = {}, useCache = true) {
        return new Promise((resolve, reject) => {
            const cacheKey = url + JSON.stringify(params);
            
            // 检查缓存
            if (useCache) {
                const cachedData = DataCache.get(cacheKey);
                if (cachedData) {
                    resolve(cachedData);
                    return;
                }
            }
            
            // 显示加载动画
            this.showLoading();
            
            // 构建查询字符串
            const queryString = Object.keys(params)
                .map(key => encodeURIComponent(key) + '=' + encodeURIComponent(params[key]))
                .join('&');
            
            const fullUrl = url + (queryString ? '?' + queryString : '');
            
            // 发起请求
            fetch(fullUrl)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('网络响应错误');
                    }
                    return response.json();
                })
                .then(data => {
                    // 缓存数据
                    if (useCache) {
                        DataCache.set(cacheKey, data);
                    }
                    resolve(data);
                })
                .catch(error => {
                    console.error('加载数据失败:', error);
                    reject(error);
                })
                .finally(() => {
                    // 隐藏加载动画
                    this.hideLoading();
                });
        });
    },
    
    // 显示加载动画
    showLoading: function() {
        let loading = document.querySelector('.loading');
        if (!loading) {
            loading = document.createElement('div');
            loading.className = 'loading';
            const spinner = document.createElement('div');
            spinner.className = 'spinner';
            loading.appendChild(spinner);
            document.body.appendChild(loading);
        }
        loading.style.display = 'flex';
    },
    
    // 隐藏加载动画
    hideLoading: function() {
        const loading = document.querySelector('.loading');
        if (loading) {
            loading.style.display = 'none';
        }
    },
    
    // 优化图表配置
    optimizeChartOption: function(option) {
        // 添加动画延迟，避免同时渲染多个图表导致卡顿
        if (!option.animation) {
            option.animation = true;
        }
        
        // 设置渐进式渲染
        if (!option.progressive) {
            option.progressive = 200;
            option.progressiveThreshold = 500;
        }
        
        // 优化提示框
        if (option.tooltip && !option.tooltip.enterable) {
            option.tooltip.enterable = true;
            option.tooltip.hideDelay = 100;
        }
        
        return option;
    },
    
    // 创建响应式图表
    createResponsiveChart: function(chartId) {
        const chart = echarts.init(document.getElementById(chartId));
        
        // 添加响应式调整
        window.addEventListener('resize', function() {
            chart.resize();
        });
        
        return chart;
    }
};

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    ChartUtils.initLazyLoad();
}); 