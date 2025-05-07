# Week #024 ~ #025

## 專案啟動選項與步驟

1. 使用 conda 創建一個 environment
```bash
# 請選擇你想要的 env 名稱，並取代以下 {{ENV_NAME}} 的字串
conda create -n {{ENV_NAME}} python=3.6 flask flask-restful -c conda-forge -y

# 安裝完成後啟動剛剛創建的 environment
conda activate {{ENV_NAME}}
```
2. 啟動專案的 api server
```bash
# 第一至第二堂製作的 API 編程，該時還沒有採用 flask_restful
python main.py

# 第三堂與之後的 API 編程
python refactor.py
```

## 使用 Jinja 模板的 Flask 專案

以下整理了 Flask 搭配 Jinja 模板引擎的基本用法。

## Jinja 模板基礎

Flask 預設使用 Jinja2 作為其模板引擎。Jinja 允許您直接在 HTML 檔案中嵌入類似 Python 的表達式和邏輯。

### 渲染模板

在您的 Flask 視圖函數中，使用 `render_template()` 函數來渲染位於 `templates` 目錄（預設）中的 HTML 檔案。

```python
# app.py (或您的主要 Flask 檔案)
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')     
def index():
    # 傳遞給模板的資料
    user_name = "訪客"
    items = ["蘋果", "香蕉", "櫻桃"]
    is_logged_in = True
    return render_template('index.html', name=user_name, item_list=items, logged_in=is_logged_in)

if __name__ == '__main__':
    app.run(debug=True)
```

### 變數

將 Python 程式碼中的變數傳遞給模板。使用雙大括號 `{{ }}` 來存取它們。

```html
<!-- templates/index.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Jinja 示範</title>
</head>
<body>
    <h1>哈囉，{{ name }}！</h1>
</body>
</html>
```

### 控制結構

使用 `{% %}` 語法來運用 `if` 語句和 `for` 迴圈等控制結構。

```html
<!-- templates/index.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Jinja 示範</title>
</head>
<body>
    <h1>哈囉，{{ name }}！</h1>

    {% if logged_in %}
        <p>歡迎回來！</p>
    {% else %}
        <p>請登入。</p>
    {% endif %}

    <h2>項目：</h2>
    <ul>
        {% for item in item_list %}
            <li>{{ item }}</li>
        {% else %}
            <li>找不到項目。</li>
        {% endfor %}
    </ul>
</body>
</html>
```

### 模板繼承

建立一個具有通用結構的基礎模板，並定義子模板可以覆寫的區塊 (blocks)。

**基礎模板 (`templates/base.html`)**
```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}我的網站{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <header>
        <h1>我的網站</h1>
    </header>
    <main>
        {% block content %}
        <!-- 預設內容放在這裡 -->
        {% endblock %}
    </main>
    <footer>
        <p>&copy; 2025 我的公司</p>
    </footer>
</body>
</html>
```

**子模板 (`templates/index.html`)**
```html
{% extends "base.html" %}

{% block title %}首頁{% endblock %}

{% block content %}
    <h1>哈囉，{{ name }}！</h1>

    {% if logged_in %}
        <p>歡迎回來！</p>
    {% else %}
        <p>請登入。</p>
    {% endif %}

    <h2>項目：</h2>
    <ul>
        {% for item in item_list %}
            <li>{{ item }}</li>
        {% else %}
            <li>找不到項目。</li>
        {% endfor %}
    </ul>
{% endblock %}
```

### 過濾器 (Filters)

使用過濾器來修改變數。

```html
<p>使用者名稱：{{ username | lower }}</p>
<p>項目數量：{{ items | length }}</p>
<p>原始 HTML：{{ raw_html | safe }}</p>
```

以上涵蓋了在 Flask 應用程式中使用 Jinja 模板的基本概念。

### Flask 請求生命週期處理函式 (Request Lifecycle Hooks)

Flask 提供了一些裝飾器，允許您在請求處理的不同階段執行函式。這些對於執行如身份驗證、資料庫連線管理、日誌記錄或修改回應等任務非常有用。

*   **`@app.before_request`**
    *   **時機：** 在每個請求實際由視圖函數處理之前執行。
    *   **用途：** 常用於身份驗證檢查、開啟資料庫連線、記錄請求資訊、或在請求物件 (`flask.request`) 可用後對其進行預處理。
    *   **注意：** 如果此函式返回一個回應物件（或任何非 `None` 的值），Flask 將使用該回應，而不會呼叫相應的視圖函數。
    ```python
    from flask import g, request

    @app.before_request
    def load_current_user():
        user_id = request.cookies.get('user_id')
        if user_id:
            g.user = get_user_from_db(user_id) # 假設的函數
        else:
            g.user = None
    ```

*   **`@app.after_request`**
    *   **時機：** 在每個請求的視圖函數成功處理並產生回應之後，但在回應發送給客戶端之前執行。
    *   **用途：** 常用於修改回應物件，例如添加自訂標頭、記錄回應資訊、或對回應內容進行後處理。
    *   **注意：** 此函式必須接收一個回應物件作為參數，並且必須返回一個回應物件（可以是同一個或一個新的）。如果在請求處理期間發生未處理的例外，此函式不會執行。
    ```python
    @app.after_request
    def add_header(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response
    ```

*   **`@app.after_this_request`**
    *   **時機：** 僅在當前請求的視圖函數成功處理並產生回應之後執行一次。
    *   **用途：** 當您只需要為特定請求執行一次後處理操作時使用，例如在特定下載完成後設定一個 cookie。
    *   **注意：** 與 `@app.after_request` 類似，它接收回應物件並必須返回一個回應物件。
    ```python
    from flask import after_this_request

    @app.route('/set-cookie')
    def set_cookie_route():
        @after_this_request
        def remember_me(response):
            response.set_cookie('last_visit', 'true', max_age=60*60*24*7) # 7 天
            return response
        return "Cookie will be set for this request."
    ```

*   **`@app.teardown_request`**
    *   **時機：** 在每個請求處理完成後執行，無論請求處理期間是否發生例外。
    *   **用途：** 主要用於清理資源，例如關閉資料庫連線或釋放其他在請求期間分配的資源。
    *   **注意：** 此函式接收一個參數，即在請求處理期間發生的例外物件（如果沒有例外，則為 `None`）。它不應該修改回應物件，並且其返回值會被忽略。
    ```python
    @app.teardown_request
    def close_db_connection(exception=None):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()
        if exception:
            app.logger.error(f"An exception occurred: {exception}")
    ```

這些請求鉤子為 Flask 應用程式提供了強大的擴展性，允許開發者在請求處理流程的關鍵點注入自訂邏輯。

## 一些有用的 Python 語法
### 靜態檔案

使用 `url_for()` 連結到位於 `static` 目錄中的靜態檔案（CSS、JS、圖片）。

```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
<script src="{{ url_for('static', filename='js/script.js') }}"></script>
<img src="{{ url_for('static', filename='images/logo.png') }}" alt="標誌">
```

### 產生視圖函數的 URL

除了連結靜態檔案，`url_for()` 最常見的用途是動態產生應用程式中特定視圖函數（endpoints）的 URL。這樣可以避免在模板中硬編碼 URL，使得在修改路由時更加方便。

第一個參數是視圖函數的名稱（與 `@app.route()` 裝飾器中定義的函數同名）。

**範例 (`templates/form.html`)**

在 `templates/form.html` 中，`url_for('index')` 會產生與 `index` 視圖函數對應的 URL（通常是 `/`），並將其設定為表單的提交目標 (`action`)：

```html
<form action="{{ url_for('index') }}" method="POST">
    <!-- 表單欄位 -->
    <input name="username" type="text" />
    <input name="age" type="number" />
    <input type="submit" />
</form>
```

如果路由包含變數（例如 `@app.route('/user/<username>')`），您可以在 `url_for()` 中將其作為關鍵字參數傳遞：

```python
# Python 視圖函數
@app.route('/user/<username>')
def profile(username):
    return f'使用者：{username}'
```

```html
<!-- 模板中的連結 -->
<a href="{{ url_for('profile', username='JohnDoe') }}">查看 JohnDoe 的個人資料</a>
```

## RESTful API 使用說明

本專案提供了一組 RESTful API 端點，用於管理使用者 (Users)、班級 (Classes) 和訊息 (Messages)。

**使用者 (Users) API**
| HTTP 方法 | 路徑 (Path)        | 描述                                   | 請求主體 (Request Body) (JSON) & Headers | 回應 (Response) (JSON / Text)                     |
| :-------- | :----------------- | :------------------------------------- | :--------------------------------------- | :------------------------------------------------ |
| `GET`     | `/users`           | 取得所有使用者列表                     | 無                                       | 包含所有使用者的陣列 (200 OK)                     |
| `GET`     | `/users/<user_id>` | 根據 ID 取得特定使用者                 | 無                                       | 包含特定使用者資訊的物件 (200 OK)                 |
| `POST`    | `/users`           | 建立新使用者                           | `{ "username": "姓名 (必填)", "age": 年齡 (必填) }` | 包含新建立的使用者資訊 (含 `user_id`) (201 Created, Location header) |
| `PUT`     | `/users/<user_id>` | 更新指定 ID 的使用者資訊 (可部分更新)  | `{ "username": "姓名", "age": 年齡 }` (欄位皆可選) | 包含更新後的使用者資訊 (200 OK)                   |
| `PATCH`   | `/users/<user_id>` | 部分更新指定 ID 的使用者資訊           | `{ "username": "姓名", "age": 年齡 }` (欄位皆可選) | 包含更新後的使用者資訊 (200 OK)                   |
| `DELETE`  | `/users/<user_id>` | 刪除指定 ID 的使用者                   | 無                                       | 包含已刪除的使用者資訊 (200 OK)                   |

**班級 (Classes) API**
| HTTP 方法 | 路徑 (Path)         | 描述                                   | 請求主體 (Request Body) (JSON) & Headers | 回應 (Response) (JSON / Text)                     |
| :-------- | :------------------ | :------------------------------------- | :--------------------------------------- | :------------------------------------------------ |
| `GET`     | `/classes`          | 取得所有班級列表                       | 無                                       | 包含所有班級資訊的陣列 (含使用者列表) (200 OK)    |
| `GET`     | `/classes/<class_id>`| 根據 ID 取得特定班級                   | 無                                       | 包含特定班級資訊的物件 (含使用者列表) (200 OK)  |

**訊息 (Messages) API**
| HTTP 方法 | 路徑 (Path)           | 描述                                   | 請求主體 (Request Body) (JSON) & Headers | 回應 (Response) (JSON / Text)                     |
| :-------- | :-------------------- | :------------------------------------- | :--------------------------------------- | :------------------------------------------------ |
| `POST`    | `/messages/<user_id>` | 為指定使用者提交訊息 (非同步處理)      | Body: `{ "data_date": "日期 (必填)", "location": "地點 (必填)" }`<br>Header: `token: xuemi-token` | "Acknowledged" (202 Accepted)                     |

**注意：**
*   `<user_id>` 和 `<class_id>` 代表資源的唯一識別碼。
*   所有 `POST`, `PUT`, `PATCH` 請求的請求主體應為 JSON 格式，且 `Content-Type` 標頭應設定為 `application/json`。
*   使用者 `POST` 請求成功建立後，回應會在 `Location` 標頭中包含新資源的 URL。
*   訊息 `POST` 請求需要一個值為 `xuemi-token` 的 `token` 標頭進行驗證。若 token 遺失，回應 401；若 token 無效，回應 403。
*   訊息 `POST` 請求成功後會設定 `sent_message_before=true` 和 `message_only=1` (路徑 `/messages`) 的 cookies。

### 常見 HTTP/API 狀態碼說明

API 回應通常會包含一個 HTTP 狀態碼，用來表示請求的處理結果。以下是一些常見狀態碼及其意義：

*   **`200 OK` (成功)**
    *   **意義：** 請求已成功處理。
    *   **常見場景：** `GET` 請求成功取得資料、`PUT`/`PATCH` 請求成功更新資源、`DELETE` 請求成功刪除資源（有時也用 `204 No Content`）。

*   **`201 Created` (已建立)**
    *   **意義：** 請求已成功，且因此建立了一個新的資源。
    *   **常見場景：** `POST` 請求成功建立新資源（例如，建立新使用者）。回應通常包含一個 `Location` 標頭，指向新建立資源的 URL。

    *   **`202 Accepted` (已接受)**
    *   **意義：** 伺服器已接受請求進行處理，但處理尚未完成。請求最終可能會或可能不會被執行。
    *   **常見場景：** 用於非同步操作，例如將任務放入佇列處理。伺服器告知客戶端請求有效且已被接受，但結果稍後才會產生。本專案中的 `/messages` 端點即使用此狀態碼。

    *   **`204 No Content` (無內容)**
    *   **意義：** 伺服器已成功處理請求，但沒有任何內容需要返回。
    *   **常見場景：** `DELETE` 請求成功刪除資源後，或者 `PUT` 請求成功更新資源但不需要返回更新後的內容時。

*   **`301 Moved Permanently` (永久移動)**
    *   **意義：** 請求的資源已被永久移動到新的 URL。回應中通常會包含一個 `Location` 標頭，指示新的 URL。
    *   **常見場景：** 網站結構變更，舊的 URL 需要永久指向新的位置。搜尋引擎會更新其索引。

*   **`302 Found` (找到)**
    *   **意義：** 請求的資源暫時位於不同的 URL。客戶端應繼續使用原始 URL 進行未來的請求。回應中通常會包含一個 `Location` 標頭，指示臨時的 URL。
    *   **常見場景：** 臨時性的網頁重新導向，例如登入後跳轉到使用者儀表板。

*   **`304 Not Modified` (未修改)**
    *   **意義：** 表示自上次請求以來，請求的資源未被修改。客戶端可以使用其快取的版本。
    *   **常見場景：** 客戶端發送帶有條件的 `GET` 請求（例如使用 `If-Modified-Since` 或 `If-None-Match` 標頭），伺服器確認資源未變更，因此不需要重新傳輸。

*   **`400 Bad Request` (錯誤請求)**
    *   **意義：** 伺服器無法理解請求，通常是因為客戶端錯誤（例如，格式錯誤的請求語法、無效的請求訊息框架、或欺騙性的請求路由）。
    *   **常見場景：** 請求的 JSON 主體格式錯誤、缺少必要的參數、參數類型不符等。

*   **`401 Unauthorized` (未授權)**
    *   **意義：** 請求需要使用者驗證。客戶端必須先進行身份驗證才能取得請求的回應。
    *   **常見場景：** 存取需要登入的資源，但未提供有效的身份驗證憑證（如 API 金鑰、Token）。

    *   **`403 Forbidden` (禁止)**
    *   **意義：** 客戶端沒有存取內容的權限；也就是說，它是未經授權的，因此伺服器拒絕給予請求的資源。與 `401 Unauthorized` 不同，客戶端的身份是已知的，但其權限不足。
    *   **常見場景：** 已登入的使用者嘗試存取其角色不允許的操作或資源。

*   **`404 Not Found` (未找到)**
    *   **意義：** 伺服器找不到請求的資源。URL 是正確的，但資源不存在。
    *   **常見場景：** 請求一個不存在的使用者 ID (`/users/999`) 或一個無效的 API 路徑。

*   **`405 Method Not Allowed` (方法不允許)**
    *   **意義：** 伺服器知道請求的方法，但目標資源不支援該方法。
    *   **常見場景：** 對於只允許 `GET` 的資源端點嘗試使用 `POST` 或 `DELETE` 方法。

*   **`500 Internal Server Error` (內部伺服器錯誤)**
    *   **意義：** 伺服器遇到了不知道如何處理的意外情況。
    *   **常見場景：** 伺服器端的程式碼發生錯誤（未處理的異常）、資料庫連線失敗、或其他伺服器內部問題。這通常表示需要修復伺服器端的程式碼。

*   **`503 Service Unavailable` (服務不可用)**
    *   **意義：** 伺服器目前無法處理請求（可能是由於過載或正在進行維護）。這通常是暫時性的狀態。
    *   **常見場景：** 伺服器負載過高、正在部署新版本、或依賴的外部服務暫時中斷。

### 常見 API 效能指標

監控 API 的效能對於確保其穩定性和可靠性至關重要。以下是一些關鍵的效能指標：

*   **每秒請求數 (Requests Per Second, RPS)**
    *   **意義：** 指標量測伺服器在一秒鐘內能夠成功處理的請求數量。它反映了 API 的吞吐量和處理能力。
    *   **用途：** 用於評估 API 的負載能力，進行容量規劃，以及偵測效能瓶頸。較高的 RPS 通常表示較好的處理能力。

*   **回應時間 (Response Time / Latency)**
    *   **意義：** 指從客戶端發送請求到接收到伺服器完整回應所花費的總時間。通常以毫秒 (ms) 為單位。
    *   **用途：** 衡量 API 的反應速度。較低的回應時間表示使用者體驗較好。監控平均回應時間、P95/P99 百分位數回應時間（95% 或 99% 的請求在此時間內完成）有助於全面了解效能。
    *   **計算 P99 回應時間：**
        *   P99 回應時間指的是 99% 的請求其回應時間都「快於或等於」此數值。換句話說，只有 1% 的請求比這個值慢。
        *   計算步驟：
            1.  **收集數據：** 收集在特定時間段內所有請求的回應時間數據。
            2.  **排序：** 將所有收集到的回應時間由小到大排序。
            3.  **取值：** 找出排序後位於第 99 百分位數的值。例如，如果您有 1000 個請求記錄，P99 就是排序後第 990 個請求的回應時間 (1000 * 0.99 = 990)。如果有 100 個請求，P99 就是第 99 個請求的回應時間。
        *   **重要性：** P99 (以及 P95、P90 等百分位數) 比平均回應時間更能反映大多數使用者的體驗，因為它不容易受到極少數異常慢的請求影響，從而更準確地呈現 API 在高負載或峰值情況下的「最差情況」效能。

*   **錯誤率 (Error Rate)**
    *   **意義：** 指在一段時間內，導致錯誤（通常是 4xx 或 5xx 狀態碼）的請求佔總請求數量的百分比。
    *   **用途：** 反映 API 的穩定性和可靠性。持續偏高的錯誤率表示 API 可能存在問題（程式碼錯誤、資源不足、相依服務問題等），需要進行調查和修復。

## 其他有用資源
1. Jinja 的管網及使用說明 [[連結](https://jinja.palletsprojects.com/en/stable/)]
2. 三方伺服器 Logging 管理服務：Centralize / elastic search
3. Flask 官網上關於模組化應用的描述 [[連結](https://flask.palletsprojects.com/en/stable/blueprints/)]