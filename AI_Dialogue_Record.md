# AI 協作開發對話紀錄 (AI Dialogue Record)

本文件紀錄了在實作 **DIC4 MVC Web-MySQL-DB-Flask AIoT Demo** 過程中，人類與 AI (Antigravity 系統) 協作開發的完整流程摘要。

---

## 階段一：建立底層 AIoT 基礎專案架構
*   **User 需求**：在指定路徑建立一個本地端的 Python AIoT 模擬專案。要求包含：`esp32_sim.py` (模擬產生溫濕度與 WiFi 數據每 5 秒利用 HTTP POST 發送)、`app.py` (Flask 後端 API，將接收到的資料存入 SQLite3)、與 `dashboard.py` (Streamlit 讀取 SQLite 表單並即時顯示折線圖、KPI 與 Dataframe)。且要求「拒絕加入網路延遲與封包遺失模擬」。
*   **AI 執行**：撰寫並建立了四大核心檔案 (`requirements.txt`, `app.py`, `dashboard.py`, `esp32_sim.py`)。自動透過 `venv` 建立虛擬環境、下載相依套件並在背景啟動了所有伺服器 API。測試 `/health` 並確認成功完成資料庫寫入機制。

## 階段二：整合 Notion DIC4 授課目標 (HTML/JS Web Simulator)
*   **User 需求**：要求實作 **DIC4 目標** 1~3：
    1. 隨機每 2 秒透過 HTML JS Web 網頁生成溫溼度數據。
    2. 將生成的數據傳送到 `sensors` Table 寫入 SQLite3 `aiotdb.db`。
    3. 利用 Streamlit **動態 (Dynamic)** 劃出資料庫數據圖表。
*   **AI 執行**：
    *   修改 Flask 的 `app.py`，新增 `/simulator` 路由。利用原生 JavaScript 的 `setInterval` 與 `fetch()` 發送 JSON 資料給後端 API。同時將 Flask 設定 CORS Headers。
    *   修改 Streamlit 的 `dashboard.py`，透過撰寫 `time.sleep(2)` 與 `st.rerun()`，達到「全自動動態定時重刷畫面」的效果。

## 階段三：自動化瀏覽器測試
*   **User 需求**：「幫我直接執行測試」
*   **AI 執行**：AI 呼叫內建的 Browser Subagent 打開隱形瀏覽器，先進入 `http://127.0.0.1:5000/simulator` 掛機 10 秒鐘讓 JS 不斷送出假資料；隨後立即操作瀏覽器開啟 `http://localhost:8501` 查看 Streamlit 儀表盤，確認圖表與數據在無人為操作下會每隔數秒跳動自動更新，並附上 `.webp` 結案錄影檔交付。

## 階段四：匯入 Notion 的課堂完整資源 (加入 Highcharts 與 README)
*   **User 需求**：提供一串 Notion 網址 (`Lecture 4: DIC4 MVC...`)，要求提取裡面提及的所有物件與功能加入專案，但「可以保留我們已經有的功能」。
*   **AI 執行**：
    *   **閱讀與提取**：AI 直接透過遠端控制瀏覽器抓取 Notion 內所有摺疊區塊與文檔。
    *   **Highcharts 實作**：達成課堂 (Step 4) 的 Data Visualization。我在 Flask 加入了 `@app.route('/api/data')` 來讓圖表要資料，並加入 `/highcharts` 提供原生的純前端圖表 (繪製最新的 20 筆折線圖與 25°C 以上/以下的溫度分佈圓餅圖 Pie Chart)。
    *   **README 與架構**：生成了符合授課要求的 `README.md` (包含 GitHub Repo 預留區與 Demo Link 區塊)。

## 階段五：版本控制 GitHub Push 與 Live Share 架設
*   **User 需求**：將完整專案推送到自己的 GitHub 帳號 (`andy19588/DIC4---using-command-to-complete-random-geneator-to-streamlit`)，並在 README 放上 Live Share 示範網址。
*   **AI 執行**：在背景執行 `git init`, `git add`, 與 `git commit` 以及帳號配置，順利將專案推上雲端。隨後利用 SSH 隧道 (`localhost.run`) 自動把本地 Port `8501` (Streamlit) 對外打穿在國際網際網路上，並把動態網址覆寫回 `README.md` 之中。

## 階段六：極簡化架構 (時間校正與移除 WiFi 欄位)
*   **User 需求**：要求將資料庫的紀錄時間「修正同步到本機的現在時間」，並且「只要溫度和濕度，刪除所有網站、資料庫上有關 WiFi 的一切參數」。
*   **AI 執行**：
    *   移除 `CURRENT_TIMESTAMP` 的 UTC 時差，改用 Python 在寫入時提取作業系統的 `datetime.now()` 作為最新當地時間。
    *   清空並廢棄了帶有舊綱要的舊 Database。重建 `sensors` Table 綱要，剔除所有 `wifi_ssid` 與 `wifi_rssi` 欄位。
    *   更新 JS Frontend、Streamlit Metrics 卡片與 `esp32_sim`。再次推送版控，達成 100% Focused 在「時間、溫度、濕度」的純淨版本，並替使用者重新建立最新的外部觀看 Live Share 連線。

*(紀錄完畢)*
