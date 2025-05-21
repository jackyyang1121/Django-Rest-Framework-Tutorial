from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'


"""
應用配置: 告訴 Django 我有products 應用的存在和它的設定 (如主鍵類型)。
啟用應用: 讓 products 應用在 settings.py 的 INSTALLED_APPS 中被正確識別。
你的 settings.py 有 'products'，Django 會自動載入 ProductsConfig。
自訂行為: 可以在 ProductsConfig 中添加更多配置 (如啟動時執行程式碼)，目前你只設了基本屬性。
"""
"""
django.db.models.BigAutoField作用:

自動遞增: 每新增一筆資料，主鍵值自動加 1 (如 1, 2, 3...)。
唯一性: 確保每筆資料有獨特 ID，方便查找和關聯。
64 位容量: 比普通 AutoField (32 位，最大 2,147,483,647) 大，適合大規模資料，可以給很多id。
"""