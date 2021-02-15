＃ 目標

串接dynamodb-local的container

## 流程

製作docker-compose.yml，裡面設有dynamodb的container，並啟用

requirements.txt 更新

啟用python的 venv虛擬環境

設置本地環境變數，供後續開發使用

製作一個本地腳本，模擬串聯dynamodb

將該腳本引入app.py內

封裝，模擬調度

## 在專案根目錄下製作docker-compose.yml，內容如下

```
# Use root/example as user/password credentials
version: '3.8'

services:
  dynamodb:
    container_name: cxcxc-db
    image: amazon/dynamodb-local
    ports:
      - 8000:8000

networks:
  default:
    name: cxcxc-sam

```

## 安裝並啟用docker-compose

```
sudo curl -L "https://github.com/docker/compose/releases/download/1.28.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose up -d
```

## requirements.txt 更新

```
requests
boto3
boto3-stubs[s3,dynamodb]
mypy-boto3-builder
```

## 啟用虛擬環境，並安裝套件
```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## 為cloud9指定額外的套件路徑

點擊左上角cloud9 icon，找到Preferences 選項

找到python support，找到裡面的PYTHONPATH，在最後方打上冒號，輸入下方位置

```
:/home/ec2-user/environment/aws_serverless_tutorial/venv/lib/python37/site-packages

```
## 新建一個python script，dynamodb_demo.py，用來即時開發，觀察效果的python檔案

先設置環境變數
```
export DYNAMODB_LOCAL_PATH=http://localhost:8000
```

執行程式碼觀看結果
```
python3 dynamodb_demo.py
```

## 改寫進app.py，而後打包，本地模擬調度，此次必須指定docker network，與dynamodb 位於同一網路
```
sam build
sam local start-api --env-vars env.json --docker-network cxcxc-sam
curl http://localhost:3000/hello
```





