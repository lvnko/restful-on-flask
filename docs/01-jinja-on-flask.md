[回到目錄](overview.md) | [下一章](02-dyn-bind-jinja-n-flask.md)
---
## 1. 在 Flask 架構上使用 Jinja 模板

以下整理了 Flask 搭配 Jinja 模板引擎的基本用法。

### Jinja 模板基礎

Flask 預設使用 Jinja2 作為其模板引擎。Jinja 允許您直接在 HTML 檔案中嵌入類似 Python 的表達式和邏輯。

#### 渲染模板

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

#### 變數

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

#### 控制結構

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

#### 模板繼承

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

#### 過濾器 (Filters)

使用過濾器來修改變數。

```html
<p>使用者名稱：{{ username | lower }}</p>
<p>項目數量：{{ items | length }}</p>
<p>原始 HTML：{{ raw_html | safe }}</p>
```

以上涵蓋了在 Flask 應用程式中使用 Jinja 模板的基本概念。

#### Flask 請求生命週期處理函式 (Request Lifecycle Hooks)

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
