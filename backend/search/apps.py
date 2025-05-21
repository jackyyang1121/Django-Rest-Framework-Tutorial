from django.apps import AppConfig


class SearchConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'search'

"""
若我在search有自訂models.py，則這個檔案就可以提供以下功能，不過這邊目前沒有
"""
"""
應用配置: 告訴 Django 我有search 應用的存在和它的設定 (如主鍵類型)。
啟用應用: 讓 search 應用在 settings.py 的 INSTALLED_APPS 中被正確識別。
你的 settings.py 有 'search'，Django 會自動載入 SearchConfig。
自訂行為: 可以在 SearchConfig 中添加更多配置 (如啟動時執行程式碼)，目前你只設了基本屬性。
"""
"""
django.db.models.BigAutoField作用:

自動遞增: 每新增一筆資料，主鍵值自動加 1 (如 1, 2, 3...)。
唯一性: 確保每筆資料有獨特 ID，方便查找和關聯。
64 位容量: 比普通 AutoField (32 位，最大 2,147,483,647) 大，適合大規模資料。
"""