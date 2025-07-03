[回到目錄](overview.md) | [上一章](01-jinja-on-flask.md) | [下一章](03-status-codes-n-meaning.md)
---
## 2. Jinja 與 Flask 的實用動態語法
### 靜態檔案

使用 `url_for()` 連結到位於 `static` 目錄中的靜態檔案（CSS、JS、圖片）。

```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
<script src="{{ url_for('static', filename='js/script.js') }}"></script>
<img src="{{ url_for('static', filename='images/logo.png') }}" alt="標誌">
```

### 動態產生 ENDPOINTS 的 URL

除了連結靜態檔案，`url_for()` 最常見的用途是動態產生應用程式中特定 Endpoints 的 URL。這樣可以避免在模板中硬編碼 URL，使得在修改路由時更加方便。

第一個參數是 Endpoint 的名稱（與 `@app.route()` 裝飾器中定義的函數同名）。

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
