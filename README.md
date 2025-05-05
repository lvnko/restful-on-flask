# Week #024 ~ #028

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

本專案提供了一組 RESTful API 端點，用於透過 HTTP 請求對 `data/users.csv` 中的使用者資料執行 CRUD（建立、讀取、更新、刪除）操作。

| HTTP 方法 | 路徑 (Path)        | 描述                                   | 請求主體 (Request Body) (JSON) | 回應 (Response) (JSON)                     |
| :-------- | :----------------- | :------------------------------------- | :----------------------------- | :----------------------------------------- |
| `GET`     | `/users`           | 取得所有使用者列表                     | 無                             | 包含所有使用者的陣列                       |
| `GET`     | `/users/<user_id>` | 根據 ID 取得特定使用者                 | 無                             | 包含特定使用者資訊的物件                   |
| `POST`    | `/users`           | 建立新使用者                           | `{ "username": "姓名", "age": 年齡 }` | 包含新建立的使用者資訊（含 `user_id`） |
| `PUT`     | `/users/<user_id>` | 完全更新指定 ID 的使用者資訊           | `{ "username": "姓名", "age": 年齡 }` | 包含更新後的使用者資訊                     |
| `PATCH`   | `/users/<user_id>` | 部分更新指定 ID 的使用者資訊           | `{ "username": "姓名" }` 或 `{ "age": 年齡 }` 或兩者皆有 | 包含更新後的使用者資訊                     |
| `DELETE`  | `/users/<user_id>` | 刪除指定 ID 的使用者                   | 無                             | 包含已刪除的使用者資訊                     |

**注意：**
*   `<user_id>` 代表使用者的唯一識別碼。
*   `POST`, `PUT`, `PATCH` 請求需要將 `Content-Type` 標頭設定為 `application/json`。
*   成功建立 (`POST`) 的回應會在 `Location` 標頭中包含新資源的 URL。

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

## 其他有用資源
1. Jinja 的管網及使用說明 [[連結](https://jinja.palletsprojects.com/en/stable/)]
