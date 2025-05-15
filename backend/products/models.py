import random
from django.conf import settings
from django.db import models
from django.db.models import Q

User = settings.AUTH_USER_MODEL # auth.User

TAGS_MODEL_VALUES = ['electronics', 'cars', 'boats', 'movies', 'cameras']

class ProductQuerySet(models.QuerySet):  #不是模型所以不用繼承models.Model
    #繼承了 Django 的 models.QuerySet，用來定義查詢產品的具體邏輯。
    def is_public(self):
        return self.filter(public=True)
    #is_public(self)：過濾出 public=True 的產品，返回一個新的 QuerySet

    def search(self, query, user=None):  #search(self, query, user=None)：根據 query 搜尋產品標題或內容，並根據用戶（user）進一步過濾。
        lookup = Q(title__icontains=query) | Q(content__icontains=query) #使用 Q 物件實現標題（title__icontains）和內容（content__icontains）的模糊搜尋。
        """什麼是「模糊搜尋」？
        想像你在找一本書，書名可能包含「phone」，但你不確定是「iPhone」還是「Phone Case」，怎麼找到所有可能的書？這就是模糊搜尋。

        答案：
        模糊搜尋是指在搜尋時不要求完全匹配，而是只要部分符合條件即可。在這裡，title__icontains 和 content__icontains 實現了這種模糊搜尋。
        細節：
        title__icontains=query：
        title 是欄位名，表示搜尋產品的標題。
        __icontains 是 Django ORM 的查詢運算子，表示「包含」（contains），且忽略大小寫（i 表示 case-insensitive）。
        例如，query = "phone" 會匹配標題中包含 "phone" 的產品，像 "iPhone" 或 "Phone Case"。
        content__icontains=query：
        同理，content 是產品的內容欄位。
        __icontains 會檢查內容中是否包含 query，例如 "a phone case" 也會匹配。
        Q(...) | Q(...)：
        | 表示「或」邏輯，結合兩個條件：標題或內容只要有一個包含 query，就符合條件。
        """
        """
        Q 是 Django ORM 提供的一個類，用來構建複雜的查詢條件，特別是用於表示「與」（AND）、「或」（OR）和「非」（NOT）邏輯。
        細節：
        Q 的作用：Q 物件允許你動態構建查詢條件，特別適合需要結合多個條件的情況（例如 OR 邏輯）。
        常用運算符：
        |：表示「或」（OR）。
        &：表示「與」（AND）。
        ~：表示「非」（NOT）。
        """
        qs = self.is_public().filter(lookup) #先過濾剩公開產品（is_public()），再根據 lookup 模糊搜尋條件過濾。
        if user is not None:
            qs2 = self.filter(user=user).filter(lookup)  #如果提供了 user，也會查詢該用戶的產品（無論是否公開），然後用 | 合併結果，distinct() 去除重複。
            qs = (qs | qs2).distinct() #去除重複的產品
        return qs


class ProductManager(models.Manager):
    def get_queryset(self, *args,**kwargs):
        return ProductQuerySet(self.model, using=self._db)

    def search(self, query, user=None):
        return self.get_queryset().search(query, user=user)  
        #self.ProductQuerySet(self.model, using=self._db).search(query, user=user)

class Product(models.Model):  # pk
    """
    在 Django 中，所有的模型（包括用戶模型）在繼承 models.Model 時為每個用戶（或任何模型實例）生成一個唯一的 id 欄位，作為主鍵（primary key）。
    這個 id 欄位是一個 AutoField，會自動遞增（從 1 開始）。每次創建新用戶時，Django 會為其分配一個唯一的 id（例如第一個用戶 id=1，第二個 id=2）。
    """
    """
    models 是從 django.db 模組導入的
    models.Model 是 Django ORM 的基礎類，所有 Django 模型都要繼承它。
    繼承 models.Model 讓 Product 具備與資料庫交互的能力，例如儲存、查詢、更新資料。
    Django 會根據 Product 類的欄位（像 title、price）自動在資料庫中創建對應的表。
    """
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
    """
    models.ForeignKey連結到另一個模型（這裡是 User 模型，從 settings.AUTH_USER_MODEL 導入）。表示每個產品屬於一個用戶。
    User：目標模型，表示 Django 的用戶模型。
    default=1：如果沒指定用戶，預設使用 ID 為 1 的用戶（必須確保資料庫中有 ID 為 1 的用戶，否則會報錯）。
    null=True：允許欄位在資料庫中為空（NULL），表示產品可以沒有關聯用戶。
    on_delete=models.SET_NULL：如果關聯的用戶被刪除，產品的 user 欄位會設為 NULL，而不是刪除產品。

    User = settings.AUTH_USER_MODEL
    settings.AUTH_USER_MODEL 是 Django 設定檔中的一個變數，用來指定應用程式使用的用戶模型
    """
    title = models.CharField(max_length=120)
    """
    title 是一個字串欄位，用來儲存產品的標題。
    細節：
    models.CharField：用來儲存短字串（固定長度）。
    max_length=120：限制標題長度最多 120 個字元，必須指定這個參數，否則會報錯。
    """
    content = models.TextField(blank=True, null=True)
    """
    content 是一個長文本欄位，用來儲存產品的詳細描述。
    細節：
    models.TextField：用來儲存長文本，沒有長度限制（適合儲存大段文字）。
    blank=True：允許表單提交時此欄位為空（前端驗證用）。
    null=True：允許資料庫中此欄位為 NULL（後端儲存用）。
    """
    price = models.DecimalField(max_digits=15, decimal_places=2, default=99.99)
    """
    price 是一個十進位數字欄位，用來儲存產品價格。
    細節：
    models.DecimalField：用來儲存精確的十進位數，適合價格或金額（避免浮點數誤差）。
    max_digits=15：數字總長度最多 15 位（包括小數點前後）。
    decimal_places=2：小數點後保留 2 位，例如 999.99。
    default=99.99：如果沒指定價格，預設為 99.99。
    """
    public = models.BooleanField(default=True)
    """
    public 是一個布林欄位，用來表示產品是否公開。
    細節：
    models.BooleanField：用來儲存布林值（True 或 False）。
    default=True：預設為 True，表示產品預設是公開的。
    """
    objects = ProductManager()   # 設置一個實例，用於查詢產品數據（包含產品及用戶 ID）
    #Product.objects.search("phone") 可能返回一個 QuerySet，例如 [<Product: id=1>, <Product: id=2>]。
    #每個 Product 實例有 id（產品 ID）和 user.id（用戶 ID），例如 product.id 和 product.user.id。


    def get_absolute_url(self):
        return f"/api/products/{self.pk}/"

    @property
    def endpoint(self):
        return self.get_absolute_url()

    @property
    def path(self):
        return f"/products/{self.pk}/"

    @property
    def body(self):
        return self.content

    def is_public(self) -> bool:
        return self.public # True or False

    def get_tags_list(self):
        return [random.choice(TAGS_MODEL_VALUES)]

    @property
    def sale_price(self):
        return "%.2f" %(float(self.price) * 0.8)

    def get_discount(self):
        return "122"