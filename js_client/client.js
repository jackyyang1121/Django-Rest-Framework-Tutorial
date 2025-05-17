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
    // 'submit' 是內建的事件類型，呼應index.html。它是 HTML 表單的一個標準事件
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
    // let 是 JavaScript 的一個關鍵字，用來宣告變數。
    // new 是 JavaScript 的一個關鍵字，用來創建一個物件的實例（instance）。它會調用一個構造函數（constructor），返回一個新的物件。
    // FormData 是JavaScript內建的一個 API（物件類型），用來收集和處理表單數據。它會自動從表單中提取所有輸入值，組成鍵值對。
    // new FormData(loginForm) 使用 new 創建一個 FormData 物件的實例，用來處理表單數據。
    let loginObjectData = Object.fromEntries(loginFormData); // 將表單數據轉換為對象格式
    // Object 是 JavaScript 的一個內建物件類型，用來表示物件（object）。它可以包含多個屬性和方法。
    // fromEntries 是 Object 的一個靜態方法，用來將一個可迭代的鍵值對（例如 Map 或 Array）轉換為物件。
    // Object.fromEntries(loginFormData) 將 FormData 物件轉換為一個普通的 JavaScript 物件，方便後續處理。
    let bodyStr = JSON.stringify(loginObjectData); // 將對象轉換為 JSON 字符串，用於發送請求
    // let：可以用來宣告一個變數，且它的值可以改變。就像一個可以換內容的盒子。
    // 例如：let x = 5; x = 10;（可以重新賦值）。
    // const：用來宣告一個常數，它的值不能改變。就像一個鎖住的盒子，裝進去後不能換。
    // 例如：const y = 5; y = 10;（會報錯，不能重新賦值）。
    // JSON.stringify 是 JavaScript 的一個內建方法，用來將 JavaScript 物件轉換為 JSON 字符串格式。
    // JSON 是 JavaScript Object Notation 的縮寫，是一種輕量級的數據交換格式，易於人類閱讀和編寫，也易於機器解析和生成。
    const options = {
        method: "POST", // 使用 POST 方法提交數據
        headers: {
            "Content-Type": "application/json" // 指定請求內容類型為 JSON
            // "Content-Type": "application/json" 告訴後端（接收方）：我發送的數據（body）是 JSON 格式的，後端需要用 JSON 解析器來處理。
            // 這是一個 HTTP 請求頭，確保後端知道如何正確解讀你發送的數據。
            // 如果不指定，後端可能會誤解數據格式（例如當成純文字或表單數據），導致解析失敗。
        },
        body: bodyStr // 請求主體，包含用戶輸入的數據
    };
    fetch(loginEndpoint, options) // 發送 POST 請求到後端 API，去 TokenObtainPairView拿到token
    // fetch 是瀏覽器內建的一個 API，用來發送 HTTP 請求（像 GET 或 POST），從伺服器獲取資料或發送資料。
    // 當我用 fetch(loginEndpoint, options) 發送請求時，options 包含 headers: { "Content-Type": "application/json" } 和 body: bodyStr（一個 JSON 字串）。
    // 後端（例如 Django 的 TokenObtainPairView）看到 "Content-Type"，就知道怎麼解析 body，然後提取 username 和 password。
    .then(response => {   //.then 是 JavaScript 中 Promise 物件的一個方法，用來處理非同步操作的結果。
        return response.json(); // 將回應轉換為 JSON 格式
    // 即使後端返回的是 JSON 格式的數據（例如 {"access": "token", "refresh": "token"}），fetch 最初只會把它當作一個字串流（stream）。
    // 我需要用 response.json() 來解析它，變成 JavaScript 物件（例如 { access: "token", refresh: "token" }），才能在程式碼中操作。
    // .then 就是為了接下 fetch 接收到的值，然後用括號內的變數儲存這個值。
    // 這裡的 response 是 fetch 的回應物件，包含了後端返回的所有資料。

    // fetch 是一個非同步操作，這意味著它會在背景運行，而不會阻塞主線程。
    // fetch會返回一個 Promise，當後端回應完成時，這個 Promise 會解析為一個 Response 物件，然後傳給第一個 .then 的 response。
    // Promise 是 JavaScript 中用來處理非同步操作的物件，代表一個「未來會完成（或失敗）」的操作和它的結果。
    // 細節：
    // fetch(loginEndpoint, options) 發送 HTTP 請求到後端（/api/token/）。
    // 後端（TokenObtainPairView）處理請求後，返回一個 HTTP 回應（包含 JSON 格式的 token 數據）。
    // fetch 會把這個回應包裝成一個 Response 物件，然後通過 Promise 傳給 .then(response => ...)，這就是 response 的來源。
    })
    .then(authData => {   //authData是自定義變數名稱，代表從後端獲取的認證數據，接住 response.json() 的結果()
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
    //URLSearchParams(data) 會把資料轉成 key=value&key2=value2 這種網址查詢參數格式。
    /*
    URLSearchParams 是 JavaScript 提供的一個內建物件（Web API），用於處理 URL 的查詢參數（Query String）。
    它提供了一個簡單且直觀的方式來解析、操作和生成 URL 查詢參數，特別適用於處理表單數據、API 請求或動態 URL 構建。
    */ 



/////////////////////////////讀到這裡////////////////////////////////////////////////////////////////



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
        if (validData && contentContainer) {   //要兩個條件同時成立
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
function handleAuthData(authData, callback) {  //callback是自定義變數名稱，代表回調函數，對應到 getProductList
    localStorage.setItem('access', authData.access); // 將 access token 儲存到 localStorage
    localStorage.setItem('refresh', authData.refresh); // 將 refresh token 儲存到 localStorage
    /*
    localStorage 是瀏覽器內建的儲存機制，允許你在用戶的瀏覽器中儲存簡單的數據（字串格式）。
    setItem 方法會把數據存下來，即使頁面關閉或重新整理，數據仍然存在（除非主動清除）。

    localStorage.setItem(key, value) 接受兩個參數：
    第一個參數（key）：鍵名，用來標識你要儲存的數據（必須是字串）。
    第二個參數（value）：要儲存的值（會自動轉成字串）。

    localStorage 用來儲存 token（像 access 和 refresh），讓用戶可以在瀏覽器中執行認證動作（例如發送 API 請求），而不需要每次都重新登入。
    localStorage 的數據會一直存在，直到用戶清除瀏覽器數據（例如清除快取）、程式碼主動刪除（localStorage.removeItem），或者瀏覽器被重置（像隱私模式結束）。
    */
    if (callback) {
        callback(); // 如果有回調函數，執行它（例如獲取產品列表）
        // callback() 需要確保 callback 是一個函數才能這樣用，否則會報錯。
    }
}


// 將數據寫入內容容器
function writeToContainer(data) {
    if (contentContainer) {
        contentContainer.innerHTML = "<pre>" + JSON.stringify(data, null, 4) + "</pre>"; // 將數據格式化為 JSON 並顯示
    /*
    JSON.stringify(data, null, 4)：
    把 JavaScript 物件（data）轉成好看的 JSON 文字
    null 是預設的轉換設定
    4 表示縮排用 4 個空格，讓格式更整齊

    "<pre>" + ... + "</pre>"：
    用 <pre> 標籤包住 JSON 文字
    <pre> 標籤會保留所有空格和換行，讓輸出格式不會亂掉

    contentContainer.innerHTML = ...：
    把處理好的內容放到網頁上的容器裡
    */
    
    
    
    }
}

// 獲取 fetch 請求選項
function getFetchOptions(method, body) {
    return {
        method: method === null ? "GET" : method, // 如果未指定方法，默認為 GET
        headers: {
            "Content-Type": "application/json", // 指定請求內容類型為 JSON
            "Authorization": `Bearer ${localStorage.getItem('access')}` // 添加授權頭，使用 access token
            /*
            ${} - JavaScript 的模板字面量語法
            一個可以填空的模板
            ${} 裡面可以放變數或表達式
            使用反引號 ` 包圍整個字符串
            */

            //getItem() 是瀏覽器提供的 localStorage API 的方法

            /*
            Authorization": HTTP 請求標頭的名稱
            Bearer: JWT 認證的標準前綴
            localStorage.getItem('access'): 從瀏覽器儲存中獲取 access token
            */
        },
        body: body ? body : null // 如果有主體數據，包含進請求中
        /*
        條件 ? 值1 : 值2
        如果條件為真，返回值1；如果為假，返回值2
        */
    };
}

// 檢查 token 是否無效
function isTokenNotValid(jsonData) {
    if (jsonData.code && jsonData.code === "token_not_valid") { // 如果回應顯示 token 無效
        //jsonData 是從getFetchOptions獲取的json格式的數據
        //token_not_valid 是 Django REST Framework 的 SimpleJWT 套件預定義的錯誤代碼
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
const searchClient = algoliasearch('H63LIZ0EO7', '48da47d859e79e339efc931743ce9d48'); // 初始化 Algolia 客戶端，使用應用 ID 和 API 密鑰

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
