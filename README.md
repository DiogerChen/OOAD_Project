# The Server part in Mahjong Game of OOAD Project

## 介绍
- 一个使用Python搭建的，利用Socket通讯，应用于课程面向对象设计基础Project麻将游戏的简易多线程服务器
- 主要逻辑判断均在该服务器上进行，并且使用状态模式更新游戏进度
- 前端链接: [喜迎 SUSTechMahjong v1.0 发布！！！](https://github.com/Pino444/SUSTechMahjong)

## 环境
- Python 3.7
- Windows/Linux/MacOS

## 运行
- 命令提示符 输入ipconfig /终端 输入 ifconfig 后获得IP地址，修改[server.py](https://github.com/DiogerChen/OOAD_Project/blob/master/server.py)中server类下的servername为服务器IP地址
- 命令提示符/终端 输入 *python3 server.py* 打开服务器
- 请确保客户端与服务器在同一网络环境下运行，打开游戏客户端，输入服务器IP地址进行连接

## 工程结构
- [server.py](https://github.com/DiogerChen/OOAD_Project/blob/master/server.py)
    server总的内容，负责存储所有连接，玩家，游戏的信息，以及收发消息的方法声明
    - [Room.py](https://github.com/DiogerChen/OOAD_Project/blob/master/Room.py)
        包含以下代码中一些方法的汇总引用，方便逻辑的实现
        - [GameStates.py](https://github.com/DiogerChen/OOAD_Project/blob/master/GameStates.py)
            游戏的时间顺序逻辑，将一局游戏分为多个状态，每次收到消息之后，执行State下的changeToNextState方法以改变游戏
        - [HuCalculator.py](https://github.com/DiogerChen/OOAD_Project/blob/master/HuCalculator.py)
            根据玩家ID和书院导师选择，计算和牌的分数
        - [Logic.py](https://github.com/DiogerChen/OOAD_Project/blob/master/Logic.py)
            Player类和Game类的声明，内含游戏的判断逻辑，包含吃碰杠和打牌等判断
        - [User.py](https://github.com/DiogerChen/OOAD_Project/blob/master/User.py)
            玩家加入房间之后只视为User，里面只有一些个人基本信息。游戏开始之后视为Player

### 其他文件
- ~~[Server](https://github.com/DiogerChen/OOAD_Project/tree/master/Server)~~
    - ~~[server.py](https://github.com/DiogerChen/OOAD_Project/tree/master/Server/server.py)~~   
    早期自建的简易多线程服务器，目前主目录下的[server.py](https://github.com/DiogerChen/OOAD_Project/blob/master/server.py)沿用了该文件的大部分内容
    - ~~[client.py](https://github.com/DiogerChen/OOAD_Project/blob/master/Server/client.py)~~   
    自建的简易客户端，用于测试服务器可用性，目前已弃用

- Logs  
    服务器初次运行时会建立该文件夹，并在其目录下存放每次运行的日志文件。文件[.gitignore](https://github.com/DiogerChen/OOAD_Project/blob/master/.gitignore)中已将该文件夹忽略

## 文档
- [MsgContent_v2.0.md](https://github.com/DiogerChen/OOAD_Project/blob/master/MsgContent_v2.0.md)  
目前作为参考的前后端通信规则文档

- [导师和技能.txt](https://github.com/DiogerChen/OOAD_Project/blob/master/%E5%AF%BC%E5%B8%88%E5%92%8C%E6%8A%80%E8%83%BD.txt)
介绍导师和技能作用和分数计算方式的文档

- ~~[MsgContent.md](https://github.com/DiogerChen/OOAD_Project/blob/master/MsgContent.md)~~  
已经弃用的第一代文档，在制定目前使用的通信规则文档时作为重要参考


## 服务器端实现清单
 - [x] 房间的创建，加入，以及房间内人员情况(准备，离开)的实时更新
 - [x] 导师选择环节
 - [x] 积分选课环节
 - [x] 正常打牌环节
 - [x] 得分结算环节
 - [x] 创建日志文件，记录服务器与客户端之间通讯内容以便于Debug
 - [ ] 重构/优化代码结构(尚未完全完成)
