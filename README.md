# The Server part in Mahjong Game of OOAD Project

## 介绍
- 一个使用Python搭建的，利用Socket通讯，应用于课程面向对象设计基础Project麻将游戏的简易多线程服务器
- 主要逻辑判断均在该服务器上进行，并且使用状态模式更新游戏进度
- 前端链接: [SUSTechMahjong](https://github.com/Pino444/SUSTechMahjong)

## 环境
- Python 3.7
- Windows/Linux/MacOS

## 运行
- 命令提示符/终端 输入 *python3 server.py* 即可运行

## 工程结构
- [server.py](https://github.com/DiogerChen/OOAD_Project/blob/master/server.py)
    - [Room.py](https://github.com/DiogerChen/OOAD_Project/blob/master/Room.py)
        - [GameStates.py](https://github.com/DiogerChen/OOAD_Project/blob/master/GameStates.py)
        - [Logic.py](https://github.com/DiogerChen/OOAD_Project/blob/master/Logic.py)
        - [User.py](https://github.com/DiogerChen/OOAD_Project/blob/master/User.py)

### 其他文件
- ~~[Server](https://github.com/DiogerChen/OOAD_Project/tree/master/Server)~~
    - ~~[client.py](https://github.com/DiogerChen/OOAD_Project/blob/master/Server/client.py)~~   
    自建简单服务器时，创建的简单的客户端用于测试可用性，目前已弃用

- Logs  
    服务器初次运行时会建立该文件夹，并在其目录下存放每次运行的日志文件。文件[.gitignore](https://github.com/DiogerChen/OOAD_Project/blob/master/.gitignore)中已将该文件夹忽略

## 文档
- [MsgContent_v2.0.md](https://github.com/DiogerChen/OOAD_Project/blob/master/MsgContent_v2.0.md)  
目前作为参考的前后端通信规则文档

- ~~[MsgContent.md](https://github.com/DiogerChen/OOAD_Project/blob/master/MsgContent.md)~~  
已经弃用的第一代文档，在制定目前使用的文档时作为重要参考


## 服务器端实现清单
 - [x] 房间的创建，加入，以及房间内人员情况(准备，离开)的实时更新
 - [x] 导师选择环节
 - [x] 积分选课环节
 - [ ] 正常打牌环节(等待测试)
 - [x] 创建日志文件，记录服务器与客户端之间通讯内容以便于Debug
 - [ ] 优化代码结构
