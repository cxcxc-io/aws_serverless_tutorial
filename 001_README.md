# 目標

##

## 生成專案

```
sam init
  1 - AWS Quick Start Templates
    2 - Image (artifact is an image uploaded to an ECR image repository)
      4 - amazon/python3.7-base
        Project name: aws_serverless_tutorial
```

## 資料夾整理

將hello_world資料夾的內容，抽至專案資料夾頂層，以利後續編寫程式，並移除資料夾

當前專案資料夾狀況如下

```
events/
tests/
.gitignore
app.py
Dockerfile
README.md
requirements.txt
template.yaml

```

## 修改Dockerfile內容，COPY原始碼的部分

```
FROM public.ecr.aws/lambda/python:3.7
COPY . "./"
RUN python3.7 -m pip install -r requirements.txt -t .
# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambda_handler"]
```

## 修改template.yaml，找到Metadata的位置，修改DockerContext指定的位置

修改後內容如下
```
    Metadata:
      DockerTag: python3.7-v1
      DockerContext: .
      Dockerfile: Dockerfile
```

## 調整硬碟大小

切換回ec2 console，找到背景執行的EC2 Instance，修改EBS空間大小，建議為25G

切換回cloud9，重新調整系統內硬碟大小

```
sudo growpart /dev/xvda 1
```

## 第一次本地模擬調度

```
cd aws_serverless_tutorial
sam build
sam local start-api
curl http://localhost:3000/hello
```

# 使開發時，程式碼可讀取環境變數

流程如下
更新template.yaml
追加設定一個env.json
app.py程式碼編寫

## 在template.yaml上方追加Parameter大項

```
Parameters:
  DYNAMODB_LOCAL_PATH:
    Type: String
    Description: My SomeVar
    Default: default value
```

## 在template.yaml內的Resource的HelloWorldFunction下追加Environment

```
Resources:
  HelloWorldFunction:
    Type: AWS::Serverless::Function # More info about Function Resource: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
    Properties:
      PackageType: Image
      Events:
        HelloWorld:
          Type: Api # More info about API Event Source: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api
          Properties:
            Path: /hello
            Method: post
      Environment:
        Variables:
          DYNAMODB_LOCAL_PATH: !Ref DYNAMODB_LOCAL_PATH
```

## 編寫env.json

```
{
  "HelloWorldFunction":{
    "DYNAMODB_LOCAL_PATH":"http://cxcxc-db:8000"
  }
}

```

## 編輯程式碼

參照app.py

## 第二次本地模擬調度

```
# cd aws_serverless_tutorial
sam build
sam local start-api --env-vars env.json 
curl http://localhost:3000/hello
```
