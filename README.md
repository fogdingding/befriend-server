# Befriend Server API (後端部分)

本專案為 Befriend 的 Server API，提供各個 Endpoint 進行操作，是以 Async 架構為主的 FastAPI 為框架來開發。

## API 文件

* **FastAPI 官方文件**：<https://fastapi.tiangolo.com/>

## 使用方式

##### 建置 Model 設定檔(無需操作)
使用者在啟用服務前，須先至 src/app/model/sqlite/base.py 中，第一次呼叫會確認是否含有資料庫檔案，沒有會建置。


##### 安裝 Python3 套件

請在目錄中，輸入以下的指令，本專案需確保 Python 版本 >= 3.12.0 ，其中 3.12.0 版本為本專案運行成功之版本。

```shell
$ python3 -m pip install -r requirements.txt
```

##### 啟動服務

在專案目錄中，輸入以下的指令，就會在 Localhost 啟動 API Server 服務，如果需要自訂 HOST:PORT，可以藉由使用 --host 及 --port 來設置。

```shell
$ uvicorn src.app.main:app --proxy-headers --forwarded-allow-ips='*'
```

當啟動本地端預設服務時，使用者可以在 <http://127.0.0.1:8000/docs> 中看到 Swagger API 文件。當作業系統為 Linux 時，如在 localhost 設置服務且用 Docker 設置運行，此時 Host 需設定成 172.17.0.1。

## Docker 建置（容器運行）

進入 src 資料夾後，輸入以下指令來建立 Docker Image。

```shell
$ docker build -t server-api . --no-cache
```

之後回到專案目錄下執行指令（退出 src 資料夾）<http://127.0.0.1:8000/docs>。可以在 docker-compose.yml 中調整參數以及 docker 中對應出來的 PORT，最後利用 docker-compose up 啟動服務。

```shell
$ docker-compose up -d --build
```


# Befriend Web (前端部分)
本專案為 Befriend 的 Web 是以 React 搭配 TypeScript 進行開發，但因時間問題並沒有在前端呈現做太多。

## 安裝 Node 套件
請在`/web`目錄中，輸入以下的指令，本專案需確保 Node 版本 >= v18.17.1 ，其中 v18.17.1 版本為本專案運行成功之版本。

```shell
$ npm i
```
### 運行服務
請在`/web`目錄中，輸入以下的指令
```shell
$ npm start
```

如果後端使用 docker 運行的話，請要修改 `/web/package.json` 原內容 `proxy: http://127.0.0.1:8000`,
```json
"proxy": "http://api:8000",
```
使前端之API能正常打到後端。



