[回到目錄](overview.md) | [上一章](06-jason-web-token.md)

## 7. 跨來源資源共用 (Cross-Origin Resource Sharing, CORS)

### 什麼是 CORS？

CORS (Cross-Origin Resource Sharing，跨來源資源共用) 是一種基於 HTTP 標頭的機制，它允許伺服器指示**除了它自己的來源 (Origin) 之外**的任何其他來源（網域、協定或通訊埠），可以從瀏覽器載入資源。

簡單來說，CORS 是瀏覽器為了安全而實施的**同源政策 (Same-Origin Policy)** 的一種例外情況。同源政策限制了網頁或腳本只能請求來自相同來源的資源，這可以防止惡意網站讀取另一個網站的敏感資料。然而，在現代 Web 開發中，前端和後端經常部署在不同的網域（例如，前端在 `https://my-app.com`，API 在 `https://api.my-app.com`），這就需要一種安全的方式來允許這種跨來源的請求。CORS 就是為此而生的標準。

---

### CORS 為何重要？

CORS 的重要性主要體現在**安全性**上。它在允許合法跨來源請求的同時，保護了使用者和網站免受惡意攻擊，特別是**跨站請求偽造 (Cross-Site Request Forgery, CSRF)**。

如果沒有同源政策和 CORS 的保護，會發生以下危險情況：

1.  **惡意網站讀取敏感資料：**
    假設您登入了一個銀行網站 `https://my-bank.com`，瀏覽器儲存了您的登入 Session Cookie。
2.  接著，您在另一個分頁中無意間訪問了一個惡意網站 `https://evil-site.com`。
3.  這個惡意網站的腳本可以向 `https://my-bank.com/api/get-balance` 發送一個 AJAX 請求。
4.  由於瀏覽器在發送請求時會**自動帶上** `my-bank.com` 的 Cookie，這個請求對於銀行伺服器來說是完全合法的。
5.  如果沒有 CORS，惡意網站的腳本就能成功讀取到您的帳戶餘額等敏感資訊。

CORS 機制透過要求伺服器明確聲明「我允許 `https://evil-site.com` 讀取我的資源」，從而阻止了這種未經授權的讀取。由於銀行伺服器顯然不會這樣設定，瀏覽器就會阻止惡意網站的請求，保護了您的資料安全。

---

### 如果瀏覽器不遵守 CORS，Cookie 如何被竊取？

如果瀏覽器不遵守 CORS 政策，客戶端 Session Cookie 的安全性將面臨嚴重威脅。如上所述，瀏覽器在向特定網域發送請求時，會自動附加該網域下的所有 Cookie。

**攻擊流程：**
1.  **使用者登入：** 使用者登入合法網站 `A.com`，瀏覽器儲存了包含 Session ID 的 Cookie。
2.  **誘騙使用者：** 使用者被誘騙點擊了惡意網站 `B.com` 的連結。
3.  **惡意腳本執行：** `B.com` 頁面中的 JavaScript 向 `A.com` 的 API（例如 `/api/user/profile`）發起一個 `fetch` 或 `XMLHttpRequest` 請求。
4.  **Cookie 自動發送：** 瀏覽器會將 `A.com` 的 Session Cookie 自動附加到這個請求中。
5.  **伺服器正常回應：** `A.com` 的伺服器看到有效的 Session Cookie，認為是合法請求，於是返回了使用者的個人資料（如姓名、Email、電話等）。
6.  **資料被竊取：** **如果沒有 CORS**，瀏覽器會允許 `B.com` 的 JavaScript 讀取這個回應。如此一來，惡意網站就成功竊取了使用者的個人資料。

CORS 正是防範這種攻擊的關鍵防線。在有 CORS 的情況下，即使請求已發送到伺服器且伺服器已回應，瀏覽器在接收到回應後，會檢查 `Access-Control-Allow-Origin` 標頭。如果標頭不允許 `B.com`，瀏覽器會**直接丟棄回應**，不讓 JavaScript 讀取，從而保護了資料。

---

### 如何管理、修改或繞過 CORS 設定

處理 CORS 問題通常取決於您對伺服器和 API 的控制程度。

#### a. 完全控制伺服器

這是最理想的情況。您可以直接在後端應用程式或 Web 伺服器（如 Nginx、Apache）的設定中，添加 CORS 相關的 HTTP 標頭。

**方法：**
在伺服器的回應中加入以下標頭：
*   `Access-Control-Allow-Origin`: 指定允許存取此資源的來源。可以是特定的網域（`https://example.com`）或萬用字元 `*`（允許任何來源，但有安全風險且通常不允許傳送 Cookie）。
*   `Access-Control-Allow-Methods`: 指定允許的 HTTP 方法（`GET`, `POST`, `PUT`, `DELETE` 等）。
*   `Access-Control-Allow-Headers`: 指定在實際請求中可以攜帶的標頭。
*   `Access-Control-Allow-Credentials`: 如果設為 `true`，則允許瀏覽器在跨來源請求中發送 Cookie。當使用此標頭時，`Access-Control-Allow-Origin` **不能**設為 `*`。

**範例 (Flask 後端):**
```python
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
# 允許來自 example.com 的請求，並支援 credentials
CORS(app, resources={r"/api/*": {"origins": "https://example.com", "supports_credentials": True}})

@app.route("/api/data")
def get_data():
    return {"message": "This is CORS-enabled data!"}
```

#### b. 在不屬於自己的伺服器上部署 API

這種情況常見於使用平台即服務 (PaaS) 或無伺服器 (Serverless) 功能（如 AWS Lambda, Vercel Functions）時。雖然您不擁有實體伺服器，但您仍然可以控制 API 的程式碼。

**方法：**
解決方案與 (a) 類似，您需要在您的**應用程式或函式程式碼**中設定 CORS 回應標頭。所有主流的 Web 框架和 Serverless 平台都提供了設定回應標頭的方法。

**範例 (Vercel Edge Function):**
```javascript
// /api/hello.js
export const config = {
  runtime: 'edge',
};

export default (request) => {
  return new Response('Hello, world!', {
    status: 200,
    headers: {
      'Access-Control-Allow-Origin': '*', // 或指定特定網域
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    },
  });
};
```

#### c. 不擁有 API 和伺服器

當您作為前端開發人員，需要串接一個**不支援 CORS** 的第三方 API 時，這是最棘手的情況。由於您無法修改伺服器設定，只能從客戶端尋找解決方案。

**方法 1：代理伺服器 (Proxy Server)**
這是最推薦且最可靠的方法。您可以建立一個由您自己控制的簡單後端服務（代理），它的功能是：
1.  接收您前端應用的請求。
2.  將這個請求轉發給目標第三方 API。
3.  接收第三方 API 的回應。
4.  將這個回應加上**您自己設定的、正確的 CORS 標頭**，然後再回傳給您的前端應用。

從瀏覽器的角度來看，它是在與您的代理伺服器（同源或已正確設定 CORS）進行通訊，因此不會觸發 CORS 錯誤。

**方法 2：瀏覽器擴充功能 (僅限開發環境)**
在**開發和測試階段**，可以使用瀏覽器擴充功能來強制繞過 CORS 限制。

*   **解決方案：** 安裝 **Allow CORS: Access-Control-Allow-Origin** 等 Chrome 網上應用程式商店的擴充功能。
*   **運作方式：** 這些擴充功能會攔截所有 HTTP 回應，並自動在其中添加 `Access-Control-Allow-Origin: *` 等標頭，從而「欺騙」瀏覽器，讓它認為所有請求都是合法的。
*   **警告：** 這是一個**極其不安全**的做法，它會完全禁用瀏覽器的同源政策保護，使您在瀏覽任何網站時都面臨 CSRF 和資料竊取的風險。**此方法絕對不能用於生產環境，並且在使用後應立即停用。**
