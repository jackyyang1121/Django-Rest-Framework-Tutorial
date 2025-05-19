import random
from django.conf import settings   #讓這邊可以訪問settings.py，進而得知用戶模型
from django.db import models  
from django.db.models import Q   #可以用來實現複雜的查詢條件
 
User = settings.AUTH_USER_MODEL # 因為沒設定所以用Django預設模型auth.User，會自動填入使用者的pk

TAGS_MODEL_VALUES = ['electronics', 'cars', 'boats', 'movies', 'cameras']    #下方get_tags_list()會拿去用

class ProductQuerySet(models.QuerySet):  
    #不是模型所以不用繼承models.Model
    #繼承了 Django 的 models.QuerySet，用來定義查詢產品的具體邏輯。
    """
    繼承 models.QuerySet:
    功能: 讓自定義 QuerySet (如 ProductQuerySet) 擴展 Django 的查詢功能，提供客製化查詢方法 (如 is_public, search)。
    來源: Django 內建，來自 django.db.models.QuerySet。
    保留原功能:繼承 QuerySet 自動獲得 filter, all, exclude 等方法，無需重寫。
    """
    def is_public(self):
        return self.filter(public=True)
    #is_public(self)：過濾出 public=True 的產品，返回一個新的 QuerySet
    """
    .filter()
    功能: .filter() 是 Django ORM 的查詢方法，用於過濾 QuerySet，返回符合條件的記錄。
    來源: Django 內建，來自 django.db.models.QuerySet。
    """

    def search(self, query, user=None):  #search(self, query, user=None)：根據 query(自定義變數) 搜尋產品標題或內容，並根據用戶user的pk進一步過濾。
        lookup = Q(title__icontains=query) | Q(content__icontains=query) #使用 Q 物件實現標題（title__icontains）和內容（content__icontains）的模糊搜尋。
        """
        什麼是「模糊搜尋」？
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
        qs = self.is_public().filter(lookup) #先過濾剩公開產品（is_public()是抓這個class自己的），再根據 lookup 模糊搜尋條件過濾。
        if user is not None:
            qs2 = self.filter(user=user).filter(lookup)  #如果提供了 user，也會查詢該用戶的產品（無論是否公開），然後用 | 合併結果，distinct() 去除重複。
            #主要就是讓搜尋結果也包含用戶自己的非公開產品
            qs = (qs | qs2).distinct() #去除重複的產品
        return qs   #qs 是一個 QuerySet，包含符合條件的產品列表。
        #qs例子:
        #<QuerySet [
        #   <Product: id=1, user="xxx", title="iPhone", content="xxx",price="xx.xx",public="True">,
        #   <Product: id=2, user="yyy", title="Phone Case", ...>,
        #   <Product: id=3, user="zzz", title="我的私人手機", user=你自己, ...>
        # ]>


class ProductManager(models.Manager):
    """
    繼承 models.Manager:
    功能: 讓自定義 Manager (如 ProductManager) 控制模型的查詢入口，定義如何取得 QuerySet 或新增自定義查詢方法。
    來源: Django 內建，來自 django.db.models.Manager。
    """
    def get_queryset(self, *args,**kwargs):
        #*args: 像個「可裝多個東西的袋子」，接收任意數量的位置引數 (如 func(1, 2, 3))，存成一個 tuple。
        # **kwargs: 像個「標籤袋子」，接收任意數量的關鍵字引數 (如 func(a=1, b=2))，存成一個 dict。
        return ProductQuerySet(self.model, using=self._db)
    """
    功能:
    self.model: 指向當前 ProductManager 關聯的模型類 (即 Product)。
    using=self._db: 指定使用的資料庫連線 (settings.DATABASES 的設定)。

    來源: Django 內建，來自 django.db.models.Manager 和 django.db.models.QuerySet。
    """

    def search(self, query, user=None):
        return self.get_queryset().search(query, user=user)  
    #返回一個 QuerySet，包含符合條件(所有公開且符合關鍵字的產品」加上「這個 user 自己的產品（不管公開或不公開，只要有符合關鍵字）」。)的產品列表。
        #self.ProductQuerySet(self.model, using=self._db).search(query, user=user)

class Product(models.Model): 
    """
    在 Django 中，所有的模型（包括用戶模型）在繼承 models.Model 時為每個用戶（或任何模型實例）生成一個唯一的 id 欄位，作為主鍵（primary key）。
    這個 id 欄位是一個 AutoField，會自動遞增（從 1 開始）。每次創建新用戶時，Django 會為其分配一個唯一的 id（例如第一個用戶 id=1，第二個 id=2）。
    """
    """
    models 是從 django.db 模組導入的，db.sqlite3 是 Django 預設的資料庫檔案，啟動並執行遷移（migrate）時自動產生。
    models.Model 是 Django ORM 的基礎類，所有 Django 模型都要繼承它。
    繼承 models.Model 讓 Product 具備與資料庫交互的能力，例如儲存、查詢、更新資料。
    Django 會根據 Product 類的欄位（user、title、content、price、public）自動在資料庫中創建對應的表。
    """
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)  
    # User 裡面有包含pk
    #default=1是預設使用者pk
    """
    ForeignKey功能: 定義 Django 模型間的一對多關聯，將一個模型的記錄連接到另一個模型的單一記錄。
    一對多關係: 一個用戶 (User) 可以擁有多個產品 (Product)，但每個產品只屬於一個用戶。
    ForeignKey來源: Django 內建，來自 django.db.models.ForeignKey。
    ForeignKey 定義在 Product 模型，指向 User。資料庫裡，Product 表有個欄位存用戶的 ID，多個產品的這個欄位可以存同一個用戶 ID，但每個產品只有一個用戶 ID。
    default=1：如果創建Product時沒指定用戶，預設使用 ID 為 1 的用戶（必須確保資料庫中有 ID 為 1 的用戶，否則會報錯）(變成是ID為1的用戶的產品)。
    null=True：允許欄位在資料庫中為空（NULL），表示產品可以沒有關聯用戶。
    on_delete=models.SET_NULL：如果關聯的用戶被刪除，產品的 user 欄位會設為 NULL，而不是刪除產品，SET_NULL來源於 Django 內建，來自 django.db.models.SET_NULL。

    User = settings.AUTH_USER_MODEL
    我的 settings.py 沒定義 AUTH_USER_MODEL，所以 Django 自動用內建的 auth.User 模型作為用戶模型。
    這個模型包含基本欄位 (如 username、password、email)。
    我在settings.py透過 django.contrib.auth (在 INSTALLED_APPS 中) 與這個預設模型互動，處理登入、權限等。
    這個 User 模型有以下欄位:
    主鍵 id（自動產生）
    username
    password
    email
    以及其他欄位（如 first_name、last_name、is_staff、is_active、date_joined 等）
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
    price 用來儲存產品價格。
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
    #ProductManager()內的return self.get_queryset().search(query, user=user)  
    #objects拿到一個QuerySet，包含符合條件(所有公開且符合關鍵字的產品」加上「這個 user 自己的產品（不管公開或不公開，只要有符合關鍵字）」。)的產品列表。


    def get_absolute_url(self):   #目前沒用到
        return f"/api/products/{self.pk}/"

    @property  #讓這個方法可以像屬性一樣使用，不需要加括號，例如：product.endpoint，而不是 product.endpoint()。
    def endpoint(self):
        return self.get_absolute_url()

    @property #讓這個方法可以像屬性一樣使用，不需要加括號，例如：product.path，而不是 product.path()。
    #因為這個需要用方法來寫，故加上@property就可以讓他變屬性，像title、content一樣操作
    def path(self):
        return f"/products/{self.pk}/"

    @property
    def body(self):
        return self.content

    def is_public(self) -> bool:
        return self.public # True or False

    def get_tags_list(self):
        return [random.choice(TAGS_MODEL_VALUES)]

    @property  #讓這個方法可以像屬性一樣使用，不需要加括號，例如：product.sale_price，而不是 product.sale_price()。
    def sale_price(self):
        return "%.2f" %(float(self.price) * 0.8)

    def get_discount(self):
        return "122"