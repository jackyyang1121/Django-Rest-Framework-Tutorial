from algoliasearch_django import algolia_engine


def get_client():
    return algolia_engine.client   #algolia_engine.client 是一個已經設定好的 Algolia 客戶端，負責連接到 Algolia 服務。我可以用它來執行搜尋、更新索引等操作。

def get_index(index_name='cfe_Product'):
    # cfe_Article
    client = get_client()
    index = client.init_index(index_name)
    return index    #找到index為cfe_Product的Product，之後讓Algolia搜尋引擎可以從Product裡面搜尋


def perform_search(query, **kwargs):   #接受一個搜尋關鍵字（query）和可選的關鍵字參數（**kwargs）
    """
    query：必需參數，表示搜尋的關鍵字（例如 "hello"）。
    **kwargs：可選的關鍵字參數，允許傳入任意鍵值對（例如 tags=["electronics"], public=True, user="john"）。
    """
    index = get_index()    #Algolia搜尋引擎的index
    params = {}
    tags = ""
    if "tags" in kwargs:   
        tags = kwargs.pop("tags") or [] #pop("tags") 從 kwargs 字典中把 tags 這個鍵值對拿出來，同時從字典中刪除它並取出其值。or []: 若 tags 是 None 或空，設為空列表 []。目前是空的
        if len(tags) != 0:   #如果tags不是空，則把tags加入params
            params['tagFilters'] = tags
    index_filters = [f"{k}:{v}" for k,v in kwargs.items() if v]
    """
    kwargs.items()：迭代 kwargs 中剩餘的鍵值對（例如 public=True, user="john"）。
    if v：過濾掉值為 False、None 或空的值（只保留「有意義」的條件）。
    f"{k}:{v}"：將每個鍵值對格式化為 key:value 字串（例如 public:True, user:john），Algolia 的過濾語法。
    結果是一個列表，長 [user="xxx", public="True", tag = None, query="我打的字"]。
    """
    if len(index_filters) != 0:
         params['facetFilters'] = index_filters
    print(params)  #包含tags和public、user所有條件
    results = index.search(query, params)  #index.search(query, params) 是 Algolia 的 API 方法，用於執行搜尋操作。
    #.search 就像按下「搜尋按鈕」，告訴 Algolia 用給定的關鍵字 (query) 和條件 (params) 去搜尋資料，然後把結果 (如符合的產品) 回傳給你。
    return results