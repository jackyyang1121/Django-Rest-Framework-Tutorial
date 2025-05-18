from algoliasearch_django import algolia_engine


def get_client():
    return algolia_engine.client

def get_index(index_name='cfe_Product'):
    # cfe_Article
    client = get_client()
    index = client.init_index(index_name)
    return index


def perform_search(query, **kwargs):   #接受一個搜尋關鍵字（query）和可選的關鍵字參數（**kwargs）
    """
    query：必需參數，表示搜尋的關鍵字（例如 "hello"）。
    **kwargs：可選的關鍵字參數，允許傳入任意鍵值對（例如 tags=["electronics"], public=True, user="john"）。
    """
    """
    perform_search("hello", tags=["electronics"], public=True)
    """
    index = get_index()
    params = {}
    tags = ""
    if "tags" in kwargs:   #檢查 kwargs 是否包含 tags 鍵
        tags = kwargs.pop("tags") or []
        if len(tags) != 0: 
            params['tagFilters'] = tags
    index_filters = [f"{k}:{v}" for k,v in kwargs.items() if v]
    """
    kwargs.items()：迭代 kwargs 中剩餘的鍵值對（例如 public=True, user="john"）。
    if v：過濾掉值為 False、None 或空的值（只保留「有意義」的條件）。
    f"{k}:{v}"：將每個鍵值對格式化為 key:value 字串（例如 public:True, user:john）。
    結果是一個列表，例如 ["public:True", "user:john"]。
    """
    if len(index_filters) != 0:
         params['facetFilters'] = index_filters
    print(params)
    results = index.search(query, params)  #index.search(query, params) 是 Algolia 的 API 方法，用於執行搜尋操作。
    return results