# 使用具有Node v18.17.1的官方Node.js鏡像作為基礎鏡像
FROM node:18.17.1

# 設置工作目錄
WORKDIR /usr/src/app

# 複製 package.json 和 package-lock.json 文件到容器中
COPY package*.json ./

# 安裝依賴
RUN npm install

# 複製應用程序的其他文件到容器中
COPY . .

# 設置容器啟動時要運行的命令
CMD ["npm", "start"]
