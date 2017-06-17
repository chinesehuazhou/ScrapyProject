

## 目录

+ spiders/sp_douban.py:主要的代码内容
+ items.py:DoubanTopMoviesItem--豆瓣top250电影字段
+ middlewares.py:

```

```



![内容区](C:\dev\py\实例\py_douban 爬虫记录\内容区.PNG)



## 爬取链接的三种方式

1. 重写start_requests方法

``` python
base_url = "https://movie.douban.com/top250"
# 共有10页，格式固定。重写start_requests方法，等价于start_urls及翻页
def start_requests(self):
    for i in range(0, 226, 25):
        url = self.base_url + "?start=%d&filter=" % i
        yield scrapy.Request(url, callback=self.parse)
```
2. 初始start_urls加当前页的下一页

``` python
base_url = "https://movie.douban.com/top250"
start_urls = [base_url]
# 取下一页链接，继续爬取
new_url = response.xpath('//link[@rel="next"]/@href').extract_first()
if new_url:
    next_url = self.base_url+new_url
    yield scrapy.Request(next_url, callback=self.parse)
```

3. 初始start_urls加LinkExtractor 链接提取器方法

``` python
# 这个方法需要较大调整（引入更多模块、类继承CrawlSpider、方法命名不能是parse）
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

base_url = "https://movie.douban.com/top250"
start_urls = [base_url]
rules = [Rule(LinkExtractor(allow=(r'https://movie.douban.com/top250\?start=\d+.*')),
                   callback='parse_item', follow=True)
              ]
```

