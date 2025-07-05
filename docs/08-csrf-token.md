[回到目錄](overview.md) | [上一章](07-cross-origin.md)
---
## 8. 跨站請求偽造 (Cross-Site Request Forgery, CSRF)

### 什麼是 CSRF？

CSRF (Cross-Site Request Forgery，跨站請求偽造)，有時也被稱為 XSRF，是一種常見的網路攻擊手法。攻擊者會誘騙已通過驗證的使用者，在他們不知情的情況下，從他們自己的瀏覽器向一個他們已登入的網站發送一個惡意的、非預期的請求。

由於這個請求是從使用者的瀏覽器發出的，它會自動攜帶所有與該網站相關的驗證資訊（例如 Session Cookie）。因此，對於伺服器來說，這個請求看起來完全是合法的，就像是使用者自己操作的一樣。

**攻擊的核心在於：利用使用者已有的登入狀態，來執行非使用者本意的操作。**

#### CSRF 攻擊範例

假設您登入了一家銀行網站 `https://my-bank.com`，該網站允許您透過一個 `POST` 請求向指定帳戶轉帳，例如：
`POST /api/transfer`
`{ "to_account": "12345", "amount": 100 }`

現在，您在未登出的情況下，訪問了一個由攻擊者控制的惡意網站 `https://evil-site.com`。這個網站的頁面中可能包含一個看不見的、會自動提交的表單：

```html
<!-- evil-site.com 的頁面 -->
<html>
  <body>
    <h1>歡迎來到我的可愛貓咪網站！</h1>
    <form id="csrf-form" action="https://my-bank.com/api/transfer" method="POST" style="display:none;">
      <input type="hidden" name="to_account" value="ATTACKER_ACCOUNT_NUMBER" />
      <input type="hidden" name="amount" value="10000" />
    </form>
    <script>
      // 頁面載入後自動提交表單
      document.getElementById('csrf-form').submit();
    </script>
  </body>
</html>
```

**攻擊流程：**
1.  當您載入 `evil-site.com` 時，頁面上的 JavaScript 會立即自動提交那個隱藏的表單。
2.  這個表單會向 `https://my-bank.com/api/transfer` 發送一個 `POST` 請求。
3.  您的瀏覽器會自動將 `my-bank.com` 的 Session Cookie 附加到這個請求中。
4.  銀行伺服器收到請求，看到有效的 Session Cookie，認為是您本人操作，於是執行了轉帳，將 10000 元轉給了攻擊者。
5.  整個過程中，您可能毫無察覺。

---

### CSRF Token 如何運作以解決此問題？

為了解決 CSRF 攻擊，業界普遍採用 **CSRF Token（也稱為 Anti-CSRF Token）** 的防禦機制。這是一種同步權杖模式 (Synchronizer Token Pattern) 的實現。

**核心思想：** 伺服器要求客戶端在發送任何會改變狀態的請求（如 `POST`, `PUT`, `DELETE`）時，必須在請求中包含一個伺服器先前提供給它的、不可預測的隨機權杖 (Token)。

**運作流程：**
1.  **伺服器產生 Token：** 當使用者訪問一個需要保護的頁面（例如轉帳頁面）時，伺服器會產生一個獨一無二、不可預測的 CSRF Token。
2.  **伺服器發送 Token 給客戶端：** 伺服器會將這個 Token 嵌入到回傳的 HTML 表單中，通常是作為一個隱藏欄位 (`<input type="hidden">`)。同時，伺服器也可能將這個 Token 存在使用者的 Session 中，以便後續比對。
3.  **客戶端提交請求時帶上 Token：** 當使用者提交表單時，這個隱藏的 CSRF Token 會跟著表單的其他資料一起被發送回伺服器。
4.  **伺服器驗證 Token：** 伺服器在收到請求後，會比較請求中包含的 CSRF Token 與它自己儲存在 Session 中的 Token 是否匹配。
    *   如果**匹配**，表示這個請求是來自於合法的、由伺服器自己產生的頁面，伺服器會處理該請求。
    *   如果**不匹配**或**缺少 Token**，伺服器會認為這是一個潛在的 CSRF 攻擊，並拒絕該請求。

#### 為何這個方法有效？

攻擊者在 `evil-site.com` 上無法得知伺服器為您的這次 Session 所產生的 CSRF Token 是什麼。因為同源政策限制了 `evil-site.com` 的腳本無法讀取來自 `my-bank.com` 的頁面內容，自然也無法取得那個隱藏的 Token。因此，攻擊者偽造的請求中將缺少有效了 CSRF Token，從而被伺服器攔截。

---

#### 範例程式碼 (使用 Flask-WTF 擴充功能)

在 Flask 中，使用 `Flask-WTF` 擴充功能可以非常方便地實現 CSRF 保護。

**1. 安裝：**
```bash
pip install Flask-WTF
```

**2. 設定：**
```python
from flask import Flask, render_template, request
from flask_wtf import CSRFProtect

app = Flask(__name__)
# 設定一個密鑰，用於加密 Session 和產生 CSRF Token
app.config['SECRET_KEY'] = 'a-very-secret-key-that-is-hard-to-guess'

# 初始化 CSRF 保護
csrf = CSRFProtect(app)

@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    if request.method == 'POST':
        # Flask-WTF 會自動驗證 CSRF Token
        # 如果驗證失敗，會拋出一個錯誤，請求不會執行到這裡
        to_account = request.form.get('to_account')
        amount = request.form.get('amount')
        print(f"轉帳 {amount} 到帳戶 {to_account}")
        return "轉帳成功！"
    
    # 在 GET 請求時，渲染表單
    return render_template('transfer_form.html')

if __name__ == '__main__':
    app.run(debug=True)
```

**3. 模板 (`templates/transfer_form.html`):**
```html
<!DOCTYPE html>
<html>
<head>
    <title>轉帳</title>
</head>
<body>
    <form method="POST">
        <!-- 
          這是關鍵！
          `csrf_token` 是由 Flask-WTF 自動產生的，
          它會渲染成一個包含 CSRF Token 的隱藏 <input> 欄位。
        -->
        {{ csrf_token() }}
        
        <label for="to_account">轉入帳戶：</label>
        <input type="text" id="to_account" name="to_account"><br><br>
        
        <label for="amount">金額：</label>
        <input type="text" id="amount" name="amount"><br><br>
        
        <input type="submit" value="確認轉帳">
    </form>
</body>
</html>
```

當您載入 `/transfer` 頁面時，`{{ csrf_token() }}` 會被渲染成類似以下的 HTML：
```html
<input id="csrf_token" name="csrf_token" type="hidden" value="一長串隨機且不可預測的字串">
```
這樣，只有從這個合法頁面提交的表單才能通過伺服器的驗證。
