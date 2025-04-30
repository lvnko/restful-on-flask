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

### 靜態檔案

使用 `url_for()` 連結到位於 `static` 目錄中的靜態檔案（CSS、JS、圖片）。

```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
<script src="{{ url_for('static', filename='js/script.js') }}"></script>
<img src="{{ url_for('static', filename='images/logo.png') }}" alt="標誌">
```

以上涵蓋了在 Flask 應用程式中使用 Jinja 模板的基本概念。

## 其他有用資源
1. Jinja 的管網及使用說明 [[連結](https://jinja.palletsprojects.com/en/stable/)]
