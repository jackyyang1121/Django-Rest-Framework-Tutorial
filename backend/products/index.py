from algoliasearch_django import AlgoliaIndex    #提供AlgoliaIndex類別
from algoliasearch_django.decorators import register  #提供註冊功能


from .models import Product


@register(Product)   # 註冊Product模型到Algolia
class ProductIndex(AlgoliaIndex):
    """
    功能: class ProductIndex(AlgoliaIndex) 定義了一個 Algolia 索引類，用於配置如何將 Product 模型的資料映射到 Algolia 搜尋引擎。
    白話解釋: 這是一個「資料打包工具」，告訴 Algolia 怎麼把 Product 模型的資料 (如 title, price) 轉成搜尋引擎能用的格式，還能設定哪些欄位可以搜尋、怎麼排序等。
    """
    # should_index = 'is_public' 如果加上這行，表示只有is_public為True的資料才會被索引，這樣可以避免不公開的資料被查詢
    fields = [    #會定義在hits裡面，可以在前端使用.hits
        'title',
        'body',
        'price',
        'user',
        'public',
        'path',
        'endpoint',
    ]
    settings = {     # 設定Algolia的搜尋引擎
        'searchableAttributes': ['title', 'body'],  # 設定哪些欄位可以被搜尋，例如我打了price他不會給我搜尋結果，但是打了title內的內容他會給我搜尋結果
        'attributesForFaceting': ['user', 'public']  # 設定哪些欄位可以進行分類
    }
    tags = 'get_tags_list'
