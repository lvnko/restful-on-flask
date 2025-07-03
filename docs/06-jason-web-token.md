[回到目錄](overview.md) | [上一章](05-sessions-pros-n-cons.md)
---
## 6. JSON Web Token (JWT)

### 什麼是 JWT (JSON Web Token)？

JWT (JSON Web Token) 是一種開放標準 (RFC 7519)，它定義了一種簡潔且獨立的方式，用於在各方之間安全地傳輸資訊，這些資訊以 JSON 物件的形式存在。由於這些資訊是經過數位簽章的，因此可以被驗證和信任。

JWT 的核心優勢在於其**無狀態 (Stateless)** 的特性。伺服器不需要在後端儲存任何關於使用者的 Session 資訊。當客戶端發送請求時，只需附上 JWT，伺服器就能驗證其合法性並解析出使用者資訊。

一個 JWT Token 由三個部分組成，並以點 (`.`) 分隔：

`eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c`

這三個部分分別是：
1.  **標頭 (Header)**
2.  **負載 (Payload)**
3.  **簽章 (Signature)**

---

#### 1. 標頭 (Header)

標頭通常由兩個部分組成：
*   **`typ` (Type):** 令牌的類型，固定為 `JWT`。
*   **`alg` (Algorithm):** 用於產生簽章的加密演算法，例如 `HS256` (HMAC-SHA256) 或 `RS256` (RSA-SHA256)。

這個 JSON 物件會經過 **Base64Url** 編碼，形成 JWT 的第一部分。

**範例：**
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```
**編碼後：** `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9`

---

#### 2. 負載 (Payload)

負載部分包含了**聲明 (Claims)**，這些是關於實體（通常是使用者）和其他附加資料的陳述。聲明分為三種類型：

*   **註冊聲明 (Registered Claims):** 這些是一組預先定義的聲明，雖然不是強制性的，但建議使用以確保互通性。常見的包括：
    *   `iss` (Issuer): 簽發者
    *   `sub` (Subject): 主題（通常是使用者的唯一標識符）
    *   `aud` (Audience): 接收者
    *   `exp` (Expiration Time): 過期時間（時間戳）
    *   `nbf` (Not Before): 生效時間（時間戳）
    *   `iat` (Issued At): 簽發時間（時間戳）
    *   `jti` (JWT ID): JWT 的唯一標識符

*   **公開聲明 (Public Claims):** 這些可以由使用 JWT 的人自由定義，但為了避免衝突，它們應該在 [IANA JSON Web Token Registry](https://www.iana.org/assignments/json-web-token/json-web-token.xhtml) 中定義，或包含一個抗衝突的命名空間。

*   **私有聲明 (Private Claims):** 這些是為在同意使用它們的各方之間共享資訊而創建的自訂聲明，既不是註冊聲明也不是公開聲明。

**重要提示：** 負載僅經過 **Base64Url** 編碼，並未加密。這意味著任何能夠截獲 JWT 的人都可以讀取其內容。因此，**切勿在負載中存放任何敏感資訊**，例如密碼。

**範例：**
```json
{
  "sub": "1234567890",
  "name": "John Doe",
  "iat": 1516239022,
  "admin": true
}
```
**編碼後：** `eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJhZG1pbiI6dHJ1ZX0`

---

#### 3. 簽章 (Signature)

簽章是用於驗證訊息在傳輸過程中沒有被篡改，並且對於使用私鑰簽章的令牌，它還可以驗證 JWT 的發送者是誰。

簽章的產生方式如下：
1.  取編碼後的標頭 (Header)。
2.  取編碼後的負載 (Payload)。
3.  取一個**密鑰 (Secret)**。
4.  將前兩者用點 (`.`) 連接起來。
5.  使用標頭中指定的加密演算法 (`alg`)，搭配密鑰對上述字串進行雜湊計算。

**公式：**
```
HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  secret
)
```

這個簽章確保了資料的完整性。只有持有密鑰的伺服器才能驗證令牌的有效性。如果有人試圖修改標頭或負載，由於他們沒有密鑰，無法產生出正確的簽章，因此伺服器在驗證時會發現簽章不匹配，並拒絕該令牌。
