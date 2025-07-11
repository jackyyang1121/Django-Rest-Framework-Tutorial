// 獲取 DOM 「Document Object Model」（文件物件模型）元素，用於後續操作
const contentContainer = document.getElementById('content-container'); // 內容容器：用於顯示搜尋結果或產品列表
/*
document 和 getElementById 都是 JavaScript 的內建功能，無需額外引入。
document 是 DOM（文件物件模型）的入口，代表整個 HTML 頁面。它讓你訪問和操作頁面中的所有元素。
getElementById 是 document 的一個方法，用來根據元素的 id 找到特定的 HTML 元素
*/
const loginForm = document.getElementById('login-form'); // 登入表單，在index.html中定義
const searchForm = document.getElementById('search-form'); // 搜尋表單，在index.html中定義
const baseEndpoint = "http://localhost:8000/api"; // 後端 API 的基礎 URL，所有請求都基於此地址

// 為登入表單綁定提交事件監聽器
if (loginForm) {
    loginForm.addEventListener('submit', handleLogin);
/*
    addEventListener() 是 JavaScript 提供的一個方法，用於為 HTML 元素綁定事件處理器。
    'submit' 是內建的事件類型，呼應index.html。它是 HTML 表單的一個標準事件
    當用戶提交表單（例如點擊 <input type="submit"> 或按 Enter 鍵）時，會自動觸發這個事件。
    當表單提交時，觸發 handleLogin 函數
*/
}

// 為搜尋表單綁定提交事件監聽器
if (searchForm) {
    searchForm.addEventListener('submit', handleSearch);
    // 當表單提交時，觸發 handleSearch 函數
}

// 處理登入表單提交
function handleLogin(event) {
    event.preventDefault(); // 阻止表單的默認提交行為，避免頁面重新載入指向觸發事件的 DOM 元素（例如表單 <form> 或按鈕 <button>）。
/*
    event和self很像，都是可以自定義的變數，但self是Python 的物件導向程式設計是去抓function內的屬性和方法
    event是JavaScript 的事件處理，當事件（例如表單提交、點擊按鈕）觸發時，瀏覽器會創建一個 Event 物件，並將其傳遞給事件處理函數，這個物件包含了事件的詳細資訊。
    event是抓事件資訊（例如 event.type）和方法（例如 event.preventDefault()）。
    事件資訊舉例:event.type表示事件的類型，例如 "submit"（表單提交）、"click"（點擊）、"keypress"（按鍵）。event.target
    event.preventDefault() 是JavaScript 內建的功能。它是 JavaScript 事件物件 event 的一個方法，用來阻止瀏覽器的預設行為。
    當你觸發某個事件（例如表單的 'submit'），瀏覽器會執行預設動作（像重新載入頁面）。
    event.preventDefault() 告訴瀏覽器不要執行這個預設動作
*/
    const loginEndpoint = `${baseEndpoint}/token/`;
     // 登入 API 端點，導入backend/urls.py再導入backend/api/urls.py
     // 再到 rest_framework_simplejwt.views.TokenObtainPairView獲取 JWT token
    let loginFormData = new FormData(loginForm); // 收集表單數據（username 和 password）
/*
    let 是 JavaScript 的一個關鍵字，用來宣告變數。
    new 是 JavaScript 的一個關鍵字，用來創建一個物件的實例（instance）。它會調用一個構造函數（constructor），返回一個新的物件。
    FormData 不是一個普通函數，它是一個「物件模板」。不用 new，JavaScript 不知道怎麼用這個模板造東西，直接報錯說「你用錯方法了！」
    FormData 是JavaScript內建的一個 API（物件類型），用來收集和處理表單數據。它會自動從表單中提取所有輸入值，組成鍵值對{username: "xxx", password: "xxx"}。
    FormData 物件就像一個「資料盒子」，可以把表單數據裝進去，然後隨時拿出來用，或者修改裡面的內容。
    如果 FormData 是一個一般函數（例如 FormData(loginForm)），它只能立即返回結果（像一個物件或字串），無法持續「持有」數據，也無法提供後續操作（像 append 或 get）。
    因此FormData 會進階成構造函數，而構造函數只能用new創建
*/
    let loginObjectData = Object.fromEntries(loginFormData); // 將表單數據轉換為對象格式
/*
    Object 是 JavaScript 的一個工具箱，裡面包含許多方法包括fromEntries。
    fromEntries 是 Object 的一個靜態方法，用來將一個可迭代的鍵值對（例如 Map 或 Array）轉換為物件。
    不是 JavaScript 看不懂 Array，而是說「Array 像一堆便條紙，寫著鍵值對；物件像一個整理好的表格，直接用鍵找值更方便。
    Object.fromEntries(loginFormData) 將 FormData 物件轉換為一個普通的 JavaScript 物件，方便後續處理。
    「物件」長得很像 JSON，但本質上是 JavaScript 的普通物件，不是 JSON 字串或 JSON 檔案。
*/
    let bodyStr = JSON.stringify(loginObjectData); // 將對象轉換為 JSON 字符串，用於發送請求
/*
    et：可以用來宣告一個變數，且它的值可以改變。就像一個可以換內容的盒子。
    例如：let x = 5; x = 10;（可以重新賦值）。
    const：用來宣告一個常數，它的值不能改變。就像一個鎖住的盒子，裝進去後不能換。
    例如：const y = 5; y = 10;（會報錯，不能重新賦值）。
    這邊的JSON和Object一樣都是JavaScript的內建工具箱
    JSON.stringify 是 JavaScript 的一個內建方法，用來將 JavaScript 物件轉換為 JSON 字符串格式。
    JSON 字串: 純文字，格式固定，無法直接操作屬性。
    JSON 資料: JavaScript 物件，可直接存取屬性或方法。
    JSON 是 JavaScript Object Notation 的縮寫，是一種輕量級的數據交換格式，易於人類閱讀和編寫，也易於機器解析和生成。
*/
    const options = {
        //method, headers, body 是 fetch 這個JavaScript 內建的function需要的參數。
        //如果不提供，之後使用fetch 會用預設值（例如 method: "GET"，無 headers 或 body）
        method: "POST", // 使用 POST 方法提交數據
        headers: {
            "Content-Type": "application/json" // 指定請求內容類型為 JSON字符串，因為 HTTP 傳輸的是文字
        },
        body: bodyStr // 請求主體，包含用戶輸入的數據，bodyStr是一個包含user和password鍵值對的 JSON 字符串
        /*
            method：
            功能：指定 HTTP 請求的方法（例如 "GET"、"POST"、"PUT"）。
            作用：告訴後端這是什麼類型的請求（POST 用於發送數據，GET 用於獲取數據）。
            白話：這是告訴快遞員「這是寄東西（POST）還是拿東西（GET）」。

            headers：
            功能：指定 HTTP 請求的標頭（headers），像是元數據，告訴後端請求的格式或認證資訊。
            作用：這裡的 "Content-Type": "application/json" 表示請求的 body 是 JSON 格式，後端會知道怎麼解析。
            白話：這是快遞單上的「包裹說明」，告訴收件人「裡面裝的是 JSON 格式的東西」。
            DRF 會自動根據 "Content-Type": "application/json" 幫你把資料轉成 Python 物件，讓我直接用 request.data 取得。
            這就是前後端 JSON 溝通的標準做法。

            body：
            功能：包含請求的實際數據（例如 JSON 字串、FormData）。
            作用：這是你要發送給後端的內容（登入的 username 和 password）。
            白話：這是快遞包裹裡的東西，真正要送的內容。
        */
    };
    fetch(loginEndpoint, options) // 發送 POST 請求到後端 API，去 TokenObtainPairView拿到token
/*
    fetch 是瀏覽器內建的一個 API，JavaScript 的內建function，用來發送 HTTP 請求（像 GET 或 POST），從伺服器獲取資料或發送資料。
    當我用 fetch(loginEndpoint, options) 發送請求時，options 包含 headers: { "Content-Type": "application/json" } 和 body: bodyStr（一個 JSON 字串）。
    後端（例如 Django 的 TokenObtainPairView）看到 "Content-Type"，就知道怎麼解析 body，然後提取 username 和 password。
*/
    .then(response => {   //.then 是 JavaScript 中 Promise 物件的一個方法，用來處理非同步操作的結果。
        return response.json(); // 將回應轉換為 JSON 格式
    /*
        後端TokenObtainPairView返回的token是 JSON 格式的數據 {"access": "token", "refresh": "token"}
        但html傳輸的是文字，fetch 只會把它當作一個JSON字串
        我需要用 response.json() 來解析它，變成 JavaScript 物件（例如 { access: "token", refresh: "token" }），才能在程式碼中操作。
        .then 就是為了接下 fetch 接收到的值，然後用括號內的變數儲存這個值。
        這裡的 response 是 fetch 的回應物件，包含了後端返回的所有資料。

        fetch 是一個非同步操作，這意味著它會在背景運行，而不會阻塞主線程。
        fetch會返回一個 Promise，當後端回應完成時，這個 Promise 會解析為一個 Response 物件，然後傳給第一個 .then 的 response。
        Promise 是 JavaScript 中用來處理非同步操作的物件，代表一個「未來會完成（或失敗）」的操作和它的結果。
        細節：
        fetch(loginEndpoint, options) 發送 HTTP 請求到後端（/api/token/）。
        後端（TokenObtainPairView）處理請求後，返回一個 HTTP 回應（包含 JSON 格式的 token 數據）。
        fetch 會把這個回應包裝成一個 Response 物件，然後通過 Promise 傳給 .then(response => ...)，這就是 response 的來源。
    */
    })
    .then(authData => {   //authData是自定義變數名稱，代表從後端獲取的認證數據，接住 response.json() 的結果=JSON格式的token+(username+password鍵值對)
        handleAuthData(authData, getProductList); // 處理認證數據並調用回調函數獲取產品列表
    })
    .catch(err => {
        console.log('err', err); // 捕獲並記錄請求中的錯誤
    });
}


// 處理搜尋表單提交
function handleSearch(event) {
    event.preventDefault(); // 阻止表單的默認提交行為
    let formData = new FormData(searchForm); // 收集表單數據（搜尋查詢）(text)
    let data = Object.fromEntries(formData); // 將表單數據轉換為物件
    let searchParams = new URLSearchParams(data); // 將對象轉換為 URL 查詢參數
    //searchParams 是從formData獲取的資料，儲存的資料長這樣:
    //searchParams = {text: "xxx"}
    //URLSearchParams(data) 會把資料轉成 key=value&key2=value2 這種網址查詢參數格式。
    /*
    URLSearchParams 是 JavaScript 提供的一個內建物件（Web API），用於處理 URL 的查詢參數（Query String）。
    它提供了一個簡單且直觀的方式來解析、操作和生成 URL查詢參數，特別適用於處理表單數據、API 請求或動態 URL 構建。
    */ 
    


    const endpoint = `${baseEndpoint}/search/?${searchParams}`; // 搜尋 API 端點，包含查詢參數
    //?${searchParams}是動態參數不影響路徑，因此實際路徑是localhost:8000/api/search/，?${searchParams}會在後端search/views.py中處理
    const headers = {
        "Content-Type": "application/json", // 指定請求內容類型為 JSON
    };
    const authToken = localStorage.getItem('access'); // 從 localStorage 獲取 access token，登入後AuthData會存token到瀏覽器
    if (authToken) {
        headers['Authorization'] = `Bearer ${authToken}`; // 如果 token 存在，添加授權頭
    }
    const options = {
        method: "GET", // 使用 GET 方法獲取搜尋結果
        headers: headers // 請求頭，包含認證信息
    };
    fetch(endpoint, options) // 發送 GET 請求到後端 API
    .then(response => {  //response目前儲存的資料包含endpoint回傳的text、user和option內的資料，且資料形式是option內的headers和endpoint接收到的後端回傳資料是JSON字串
        return response.json(); // 將回應轉換為 JSON 格式
    })
    .then(data => {
        const validData = isTokenNotValid(data); // 檢查 token 是否有效
        if (validData && contentContainer) {   //要兩個條件同時成立
            contentContainer.innerHTML = ""; // 清空內容容器，innerHTML 是 DOM 的一個屬性，用來獲取或設置元素的 HTML 內容，JavaScript內建的功能
            if (data && data.hits) { // 如果回應包含搜尋結果，data.hits是從algolia獲取的搜尋結果，hits 是 Algolia 搜索服务的内建功能，用來獲取搜尋結果
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
        callback(); 
        //這邊的用意是先執行上面的localStorage.setItem先把token儲存到localStorage
        //這時如果有callback也就是getProductList()，再執行getProductList()去瀏覽器抓token才抓得到
    }
}


// 將數據寫入內容容器
function writeToContainer(data) {
    if (contentContainer) {   //contentContainer是網頁上的容器，在index.html的<div id="content-container"></div>，上面有寫
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
function getFetchOptions(method, body) {  //method和body是自定義變數名稱，分別代表請求方法和請求主體
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
            Bearer: JWT 認證的標準前綴，在settings.py中SIMPLE_JWT設定好
            localStorage.getItem('access'): 從瀏覽器儲存中獲取 access token
            access token在前端登入時handleAuthData()會儲存token在瀏覽器
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
function isTokenNotValid(jsonData) {  // jsonData 是自定義變數名稱，代表從後端獲取的 JSON 數據，下面用的是data(isTokenNotValid(data))
    if (jsonData.code && jsonData.code === "token_not_valid") { // 如果jsonData.code 存在則略過，如果不在則執行
        //jsonData 是從getFetchOptions獲取的json格式的數據
        //token_not_valid 是 Django REST Framework 的 SimpleJWT 套件預定義的錯誤代碼
        alert("Please login again"); // 提示用戶重新登入
        return false; // 返回 false 表示 token 無效
    }
    return true; // 返回 true 表示 token 有效
}


// 獲取產品列表
function getProductList() {
    const endpoint = `${baseEndpoint}/products/`; // 產品列表 API 端點
    const options = getFetchOptions(); // 使用預設 GET 方法和授權頭
    fetch(endpoint, options) // 發送 GET 請求獲取產品列表，API回傳JSON字串
    .then(response => {
        return response.json(); // 將回應轉換為 JSON 格式
    })
    .then(data => {
        const validData = isTokenNotValid(data); // 檢查 token 是否有效
        if (validData) {
            writeToContainer(data); // 如果 token 有效，將數據寫入內容容器
            //我在前端網頁上能看到很多產品資訊，就是因為有呼叫 writeToContainer(data) 這個函數。
            //顯示在網頁的 content-container 區塊裡
        }
    });
}
/*
差異總結
| 函數               | 主要用途                 | 操作對象           | 影響範圍       |
|-------------------|-------------------------|--------------------|---------------|
| handleAuthData    | 存 token、執行 callback | localStorage、token| 認證、API 請求 |
| writeToContainer  | 顯示資料在網頁上        | contentContainer   | 畫面顯示       |

handleAuthData 是「存資料（token）到 localStorage」+「觸發後續動作」。
writeToContainer 是「把資料（通常是 API 回傳的 JSON）顯示在網頁上」。
*/


// 配置 Algolia InstantSearch.js
const searchClient = algoliasearch('H63LIZ0EO7', '48da47d859e79e339efc931743ce9d48'); // 初始化 Algolia 客戶端，使用應用 ID 和 API 密鑰

const search = instantsearch({
    indexName: 'cfe_Product', // 指定要搜尋的 Algolia 索引名稱
    searchClient, // 使用初始化的 Algolia 客戶端
});

// 添加 InstantSearch.js 小部件
search.addWidgets([  //addWidgets() 是 InstantSearch.js 的一個方法，用於添加小部件到搜索界面。
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
