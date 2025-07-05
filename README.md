# Python : 後端開發與網站安全管理

## A. 專案版本 (分支)
本專案中包括了兩個單元的學習筆記與練習，它們被整理在不同的開發分支中 (branch)，詳列如下：
- **Week #24 ~ #25** [``lesson#05``](https://github.com/lvnko/restful-on-flask/tree/lesson%2305)：<br/>
    後端框架與 API 開發    
- **Week #30 ~ #33** [``main``](https://github.com/lvnko/restful-on-flask/tree/main)：<br/>
    網站安全與權限認證

## B. 專案檔案概覽
關於本專案的檔案分佈可以參考以下簡錄：
- **學習筆記** [``/docs/overview.md``](/docs/overview.md)：<br/>
    關於各章節學習內容的筆記
- **課程練習** [``/README.md#c-專案啟動選項與步驟``](#c-專案啟動選項與步驟)：<br/>
    這次的學習內容主要以 RESTful API 的架設與不同的使用功能做練習，可跟隨本文的章節 #C 來練習

## C. 專案啟動選項與步驟

### C.1. 創建開發 environment
在以下選擇你熟悉的工具來創建你的開發環境：

#### C.1.a. 使用 Conda 創建
如果你習慣使用 Conda，可以依照以下步驟設定環境：

1.  **打開終端機**：
    開啟你的終端機應用程式 (例如 Terminal, iTerm2, 或 Conda Prompt)。

2.  **創建 Conda 環境**：
    執行以下指令來創建一個新的 Conda 環境。這裡我們使用專案指定的 Python 版本 `3.10.18`，並將環境命名為 `restful-flask`（你也可以自訂名稱）。
    ```shell
    conda create -n restful-flask python=3.10.18 -y
    # 或參考以下的指令去完成依賴模組的安裝
    # conda create -n {{ENV_NAME}} python=3.10.18 flask flask-restful flask-session flask-unsign Jinja2 -c conda-forge -y
    # 這樣的話，你便不需要執行之後的第 4. 個步驟。
    ```

3.  **啟用 Conda 環境**：
    創建完成後，啟用該環境。
    ```shell
    conda activate restful-flask
    ```
    啟用後，你會在終端機提示符前看到環境名稱 `(restful-flask)`。

4.  **安裝相依套件**：
    在已啟用的環境中，使用 `pip` 和 `requirements.txt` 檔案來安裝所有專案需要的套件。
    ```shell
    pip install -r requirements.txt
    ```

5.  **(可選) 在 VS Code 中選擇直譯器**：
    *   按下 `Cmd + Shift + P` (macOS) 或 `Ctrl + Shift + P` (Windows/Linux) 開啟命令面板。
    *   輸入 `Python: Select Interpreter`。
    *   從列表中選擇名為 `restful-flask` 的 Conda 環境。

#### C.1.b. 使用 Venv 創建
在 VS Code 中，你可以按照以下步驟操作：

1.  **打開終端機**：
    在 VS Code 中，透過 `Terminal` > `New Terminal` 開啟一個新的終端機。

2.  **創建虛擬環境**：
    在終端機中輸入以下指令來創建一個名為 `.venv` 的虛擬環境。VS Code 會自動偵測到這個環境。
    ```shell
    python3 -m venv .venv
    ```

3.  **選擇直譯器 (Interpreter)**：
    *   按下 `Cmd + Shift + P` (macOS) 或 `Ctrl + Shift + P` (Windows/Linux) 來開啟命令面板。
    *   輸入 `Python: Select Interpreter`。
    *   從列表中選擇 `./.venv/bin/python`。這會讓 VS Code 在此後自動為你啟用該環境。

4.  **安裝相依套件**：
    選擇直譯器後，VS Code 可能會提示你 `requirements.txt` 中的套件尚未安裝。你也可以手動在已啟用虛擬環境的終端機中執行以下指令來安裝所有必要的套件：
    ```shell
    pip install -r requirements.txt
    ```

### C.2. 啟動專案的 api server
#### C.2.1. Week #24 ~ #25 第二堂及之前製作的 API 編程，該時還沒有採用 flask_restful
```shell
python main.py
# [!] 使用說明請參考本頁面的章節 D
```
#### C.2.2. Week #30 第一堂集之及製作的 API 編程：
```shell
# Chapter 1: flask_restful API 練習
# Chapter 2: Client-side 及 Server-side Session 的練習
# [!] 使用說明請參考本頁面的章節 D
python refactor.py
```
#### C.2.3. 最新的 API 編程，包含了 JWT 及 CSRF Token 的練習
```shell
# Chapter 2: CSRF Token 的練習 => E
# 第一步 - 起始用戶平台：
python app.py
# 以瀏覽器訪問 http://localhost:8081/

# 第二步 - 起始惡意網頁：
# 打開另一個 Terminal
cd csrf_serve
python -m http.server 8002
# 以瀏覽器訪問 http://localhost:8002/bad_site.html
# [!] 使用說明請參考本頁面的章節 E
```

## D. RESTful API 使用說明

本專案提供了一組 RESTful API 端點，用於管理使用者 (Users)、班級 (Classes) 和訊息 (Messages)。你可以用如 Postman 這樣的 API Client 來嘗試訪問：
> [!TIP]
> 由於這個 API 有分 v1 與 v2 兩個 blueprint<br/>
> 訪問時請在端點路徑中指定才能成功訪問，格式參考如下例子:
> - ``http://localhost:8081/v1/classes``
> - ``http://localhost:8081/v2/users``

### D1. 使用者 (Users) API
>支援版本： `v1`, `v2`
>注意：在 `v2` 版本中，`GET` 請求需要先登入 (參考 `v2` 的登入 API)。

| HTTP 方法 | 路徑 (Path)        | 描述                                   | 請求主體 (Request Body) (JSON) & Headers | 回應 (Response) (JSON / Text)                     |
| :-------- | :----------------- | :------------------------------------- | :--------------------------------------- | :------------------------------------------------ |
| `GET`     | `/users`           | 取得所有使用者列表                     | 無                                       | 包含所有使用者的陣列 (200 OK)                     |
| `GET`     | `/users/<user_id>` | 根據 ID 取得特定使用者                 | 無                                       | 包含特定使用者資訊的物件 (200 OK)                 |
| `POST`    | `/users`           | 建立新使用者                           | `{ "username": "姓名 (必填)", "age": 年齡 (必填) }` | 包含新建立的使用者資訊 (含 `user_id`) (201 Created, Location header) |
| `PUT`     | `/users/<user_id>` | 更新指定 ID 的使用者資訊 (可部分更新)  | `{ "username": "姓名", "age": 年齡 }` (欄位皆可選) | 包含更新後的使用者資訊 (200 OK)                   |
| `PATCH`   | `/users/<user_id>` | 部分更新指定 ID 的使用者資訊           | `{ "username": "姓名", "age": 年齡 }` (欄位皆可選) | 包含更新後的使用者資訊 (200 OK)                   |
| `DELETE`  | `/users/<user_id>` | 刪除指定 ID 的使用者                   | 無                                       | 包含已刪除的使用者資訊 (200 OK)                   |

### D2. 班級 (Classes) API
>支援版本： `v1`

| HTTP 方法 | 路徑 (Path)         | 描述                                   | 請求主體 (Request Body) (JSON) & Headers | 回應 (Response) (JSON / Text)                     |
| :-------- | :------------------ | :------------------------------------- | :--------------------------------------- | :------------------------------------------------ |
| `GET`     | `/classes`          | 取得所有班級列表                       | 無                                       | 包含所有班級資訊的陣列 (含使用者列表) (200 OK)    |
| `GET`     | `/classes/<class_id>`| 根據 ID 取得特定班級                   | 無                                       | 包含特定班級資訊的物件 (含使用者列表) (200 OK)  |

### D3. 訊息 (Messages) API
>支援版本： `v1`

| HTTP 方法 | 路徑 (Path)           | 描述                                   | 請求主體 (Request Body) (JSON) & Headers | 回應 (Response) (JSON / Text)                     |
| :-------- | :-------------------- | :------------------------------------- | :--------------------------------------- | :------------------------------------------------ |
| `POST`    | `/messages/<user_id>` | 為指定使用者提交訊息 (非同步處理)      | Body: `{ "data_date": "日期 (必填)", "location": "地點 (必填)" }`<br>Header: `token: xuemi-token` | "Acknowledged" (202 Accepted)                     |

### D4. 登入/登出 (Auth) API
>支援版本： `v2`

| HTTP 方法 | 路徑 (Path) | 描述 | 請求主體 (Request Body) (JSON) | 回應 (Response) |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/login` | 使用者登入 | `{"username": "帳號", "password": "密碼"}` | 成功時設定 session (200 OK) |
| `POST` | `/logout` | 使用者登出 | 無 | 清除 session (200 OK) |

**注意：**
*   `<user_id>` 和 `<class_id>` 代表資源的唯一識別碼。
*   所有 `POST`, `PUT`, `PATCH` 請求的請求主體應為 JSON 格式，且 `Content-Type` 標頭應設定為 `application/json`。
*   使用者 `POST` 請求成功建立後，回應會在 `Location` 標頭中包含新資源的 URL。
*   訊息 `POST` 請求需要一個值為 `xuemi-token` 的 `token` 標頭進行驗證。若 token 遺失，回應 401；若 token 無效，回應 403。
*   訊息 `POST` 請求成功後會設定 `sent_message_before=true` 和 `message_only=1` (路徑 `/messages`) 的 cookies。

## E. 模擬 JWT 及 CSRF Token 用戶登入及功能頁面

本專案透過 `app.py` 提供了一個模擬網站，用於演示使用者登入、帳戶資訊查詢及登出功能。

### 頁面與功能說明

| 路徑 (Path) | HTTP 方法 | 功能描述 | 頁面 |
| :--- | :--- | :--- | :--- |
| `/` | `GET`, `POST` | 顯示首頁 (`GET`)，並處理使用者登入請求 (`POST`)。成功後會跳轉至帳戶頁面。 | `homepage.html` |
| `/accounts` | `GET`, `POST` | 顯示使用者帳戶頁面 (`GET`)，並處理轉帳請求 (`POST`)。此頁面需要登入才能存取。 | `accounts.html` |
| `/logout` | `GET` | 處理使用者登出請求。清除 Session 後跳轉回首頁。 | (API 端點) |

### 使用者帳號

您可以使用以下帳號進行測試：

*   **一般使用者:**
    *   **帳號:** `test`
    *   **密碼:** `test`
*   **惡意使用者 (用於 CSRF 模擬):**
    *   **帳號:** `bad_guy`
    *   **密碼:** `bad_guy`

### CSRF 攻擊模擬

本專案包含一個惡意網站範例 (`csrf_serve/bad_site.html`)，用於演示 CSRF 攻擊如何運作。

**模擬步驟：**
1.  **啟動主應用程式：** 參考章節 [C.2.3.](#c23-最新的-api-編程包含了-jwt-及-csrf-token-的練習) 的啟動步驟
2.  **執行模擬：**
    *   在瀏覽器中訪問 `http://localhost:8081/` 並使用**一般使用者** (`test`/`test`) 登入。
    *   登入後，在同一個瀏覽器中打開一個新分頁，訪問惡意網站 `http://localhost:8002/bad_site.html`。
    *   惡意網站的頁面會自動嘗試向主應用程式發送一個轉帳請求。
    *   觀察主應用程式的終端機輸出，您會看到轉帳是否成功，藉此了解 CSRF 保護機制的實際效果。


## F. 參考資源

### 常用指令參考
```shell
# 以下的指令可以確保模組安裝的版本與目的地皆與當前所使用的 Python 版本環境相容
python3 -m pip install
python3 -m pip install -r requirements.txt

# 把當前依賴模組列與其版本寫在 ``requirements.txt`` 這個檔案中
pip freeze > requirements.txt

# 簡單架設 Python Http server 的指令
python3 -m http.server 8002
```

### 其他有用資源
1. Jinja 的管網及使用說明 [[連結](https://jinja.palletsprojects.com/en/stable/)]
2. 三方伺服器 Logging 管理服務：Centralize / elastic search
3. Flask 官網上關於模組化應用的描述 [[連結](https://flask.palletsprojects.com/en/stable/blueprints/)]
4. Json Web Token (JWT) Debugger [[連結](https://jwt.io)]
