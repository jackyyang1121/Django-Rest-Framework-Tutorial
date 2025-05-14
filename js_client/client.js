// 獲取 DOM 「Document Object Model」（文件物件模型）元素，用於後續操作
const contentContainer = document.getElementById('content-container'); // 內容容器：用於顯示搜尋結果或產品列表
// document 和 getElementById 都是 JavaScript 的內建功能，無需額外引入。
// document 是 DOM（文件物件模型）的入口，代表整個 HTML 頁面。它讓你訪問和操作頁面中的所有元素。
// getElementById 是 document 的一個方法，用來根據元素的 id 找到特定的 HTML 元素
const loginForm = document.getElementById('login-form'); // 登入表單，在index.html中定義
const searchForm = document.getElementById('search-form'); // 搜尋表單，在index.html中定義
const baseEndpoint = "http://localhost:8000/api"; // 後端 API 的基礎 URL，所有請求都基於此地址

// 為登入表單綁定提交事件監聽器
if (loginForm) {
    loginForm.addEventListener('submit', handleLogin);
    // 'submit' 是內建的事件類型。它是 HTML 表單的一個標準事件
    // 當用戶提交表單（例如點擊 <input type="submit"> 或按 Enter 鍵）時，會自動觸發這個事件。
     // 當表單提交時，觸發 handleLogin 函數
}

// 為搜尋表單綁定提交事件監聽器
if (searchForm) {
    searchForm.addEventListener('submit', handleSearch);
    // 當表單提交時，觸發 handleSearch 函數
}

// 處理登入表單提交
function handleLogin(event) {
    event.preventDefault(); // 阻止表單的默認提交行為，避免頁面重新載入
    // event.preventDefault() 是內建的功能。它是 JavaScript 事件物件 (event) 的一個方法，用來阻止瀏覽器的預設行為。
    // 當你觸發某個事件（例如表單的 'submit'），瀏覽器會執行預設動作（像重新載入頁面）。
    // event.preventDefault() 告訴瀏覽器不要執行這個預設動作
    const loginEndpoint = `${baseEndpoint}/token/`;
     // 登入 API 端點，導入backend/urls.py再導入backend/api/urls.py
     // 再到 rest_framework_simplejwt.views.TokenObtainPairView獲取 JWT token
    let loginFormData = new FormData(loginForm); // 收集表單數據（username 和 password）
    let loginObjectData = Object.fromEntries(loginFormData); // 將表單數據轉換為對象格式
    let bodyStr = JSON.stringify(loginObjectData); // 將對象轉換為 JSON 字符串，用於發送請求
    const options = {
        method: "POST", // 使用 POST 方法提交數據
        headers: {
            "Content-Type": "application/json" // 指定請求內容類型為 JSON
        },
        body: bodyStr // 請求主體，包含用戶輸入的數據
    };
    fetch(loginEndpoint, options) // 發送 POST 請求到後端 API
    .then(response => {
        return response.json(); // 將回應轉換為 JSON 格式
    })
    .then(authData => {
        handleAuthData(authData, getProductList); // 處理認證數據並調用回調函數獲取產品列表
    })
    .catch(err => {
        console.log('err', err); // 捕獲並記錄請求中的錯誤
    });
}

// 處理搜尋表單提交
function handleSearch(event) {
    event.preventDefault(); // 阻止表單的默認提交行為
    let formData = new FormData(searchForm); // 收集表單數據（搜尋查詢）
    let data = Object.fromEntries(formData); // 將表單數據轉換為對象格式
    let searchParams = new URLSearchParams(data); // 將對象轉換為 URL 查詢參數
    const endpoint = `${baseEndpoint}/search/?${searchParams}`; // 搜尋 API 端點，包含查詢參數
    const headers = {
        "Content-Type": "application/json", // 指定請求內容類型為 JSON
    };
    const authToken = localStorage.getItem('access'); // 從 localStorage 獲取 access token
    if (authToken) {
        headers['Authorization'] = `Bearer ${authToken}`; // 如果 token 存在，添加授權頭
    }
    const options = {
        method: "GET", // 使用 GET 方法獲取搜尋結果
        headers: headers // 請求頭，包含認證信息
    };
    fetch(endpoint, options) // 發送 GET 請求到後端 API
    .then(response => {
        return response.json(); // 將回應轉換為 JSON 格式
    })
    .then(data => {
        const validData = isTokenNotValid(data); // 檢查 token 是否有效
        if (validData && contentContainer) {
            contentContainer.innerHTML = ""; // 清空內容容器
            if (data && data.hits) { // 如果回應包含搜尋結果
                let htmlStr = "";
                for (let result of data.hits) {
                    htmlStr += "<li>" + result.title + "</li>"; // 構建搜尋結果的 HTML 列表
                }
                contentContainer.innerHTML = htmlStr; // 將結果顯示在內容容器中
                if (data.hits.length === 0) {
                    contentContainer.innerHTML = "<p>No results found</p>"; // 如果無結果，顯示提示
                }
            } else {
                contentContainer.innerHTML = "<p>No results found</p>"; // 如果無結果，顯示提示
            }
        }
    })
    .catch(err => {
        console.log('err', err); // 捕獲並記錄請求中的錯誤
    });
}

// 處理認證數據
function handleAuthData(authData, callback) {
    localStorage.setItem('access', authData.access); // 將 access token 儲存到 localStorage
    localStorage.setItem('refresh', authData.refresh); // 將 refresh token 儲存到 localStorage
    if (callback) {
        callback(); // 如果有回調函數，執行它（例如獲取產品列表）
    }
}

// 將數據寫入內容容器
function writeToContainer(data) {
    if (contentContainer) {
        contentContainer.innerHTML = "<pre>" + JSON.stringify(data, null, 4) + "</pre>"; // 將數據格式化為 JSON 並顯示
    }
}

// 獲取 fetch 請求選項
function getFetchOptions(method, body) {
    return {
        method: method === null ? "GET" : method, // 如果未指定方法，默認為 GET
        headers: {
            "Content-Type": "application/json", // 指定請求內容類型為 JSON
            "Authorization": `Bearer ${localStorage.getItem('access')}` // 添加授權頭，使用 access token
        },
        body: body ? body : null // 如果有主體數據，包含進請求中
    };
}

// 檢查 token 是否無效
function isTokenNotValid(jsonData) {
    if (jsonData.code && jsonData.code === "token_not_valid") { // 如果回應顯示 token 無效
        alert("Please login again"); // 提示用戶重新登入
        return false; // 返回 false 表示 token 無效
    }
    return true; // 返回 true 表示 token 有效
}

// 驗證 JWT token
function validateJWTToken() {
    const endpoint = `${baseEndpoint}/token/verify/`; // token 驗證 API 端點
    const options = {
        method: "POST", // 使用 POST 方法提交 token
        headers: {
            "Content-Type": "application/json" // 指定請求內容類型為 JSON
        },
        body: JSON.stringify({
            token: localStorage.getItem('access') // 提交當前的 access token
        })
    };
    fetch(endpoint, options) // 發送 POST 請求驗證 token
    .then(response => response.json()) // 將回應轉換為 JSON 格式
    .then(x => {
        // 可在此處理 token 驗證結果，例如刷新 token
    });
}

// 獲取產品列表
function getProductList() {
    const endpoint = `${baseEndpoint}/products/`; // 產品列表 API 端點
    const options = getFetchOptions(); // 使用預設 GET 方法和授權頭
    fetch(endpoint, options) // 發送 GET 請求獲取產品列表
    .then(response => {
        return response.json(); // 將回應轉換為 JSON 格式
    })
    .then(data => {
        const validData = isTokenNotValid(data); // 檢查 token 是否有效
        if (validData) {
            writeToContainer(data); // 如果 token 有效，將數據寫入內容容器
        }
    });
}

// 頁面加載時驗證 JWT token
validateJWTToken();

// 配置 Algolia InstantSearch.js
const searchClient = algoliasearch('4IHLYNCMBJ', '2d98a3c1e68d4f81bbba206ca075cfbb'); // 初始化 Algolia 客戶端，使用應用 ID 和 API 密鑰

const search = instantsearch({
    indexName: 'cfe_Product', // 指定要搜尋的 Algolia 索引名稱
    searchClient, // 使用初始化的 Algolia 客戶端
});

// 添加 InstantSearch.js 小部件
search.addWidgets([
    // 搜尋框小部件：提供即時搜尋輸入框
    instantsearch.widgets.searchBox({
        container: '#searchbox', // 指定搜尋框的容器
    }),
    // 清除篩選條件小部件：提供按鈕以重置篩選條件
    instantsearch.widgets.clearRefinements({
        container: "#clear-refinements" // 指定清除按鈕的容器
    }),
    // 用戶篩選列表小部件：根據 user 屬性篩選搜尋結果
    instantsearch.widgets.refinementList({
        container: "#user-list", // 指定用戶篩選列表的容器
        attribute: 'user' // 指定篩選的屬性為 user
    }),
    // 公開狀態篩選列表小部件：根據 public 屬性篩選搜尋結果
    instantsearch.widgets.refinementList({
        container: "#public-list", // 指定公開狀態篩選列表的容器
        attribute: 'public' // 指定篩選的屬性為 public
    }),
    // 搜尋結果列表小部件：顯示搜尋結果
    instantsearch.widgets.hits({
        container: '#hits', // 指定搜尋結果的容器
        templates: {
            item: ` <!-- 搜尋結果項目的模板 -->
                <div>
                    <div>{{#helpers.highlight}}{ "attribute": "title" }{{/helpers.highlight}}</div>
                    <!-- 高亮顯示標題 -->
                    <div>{{#helpers.highlight}}{ "attribute": "body" }{{/helpers.highlight}}</div>
                    <!-- 高亮顯示內容 -->
                    <p>{{ user }}</p><p>\${{ price }}</p>
                    <!-- 顯示用戶和價格 -->
                </div>`
        }
    })
]);

// 啟動 InstantSearch.js，開始即時搜尋功能
search.start();
