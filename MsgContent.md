MsgContent_v2.0
#
客户端JSON格式:

    type: 请求类型，如name, create等

    socket_id: 客户端连接服务器后，服务器会将会话存入数组中，返回该会话的index + 1(可以理解为account)。如果是服务器发送的请求，socket_id设为0。

    "room": 所在的房间号。如果没有加入房间，默认值为-1

    "room_id": 所在房间内的顺序，范围是[-1,1,2,3,4]。其中-1代表没有加入房间时的默认值

    "content": 请求内容。考虑到某些请求会携带多个内容，所以设为一个数组

    {"type":"STRING", "socket_id":INT, "room":INT, "room_id":INT, "content":[ARRAY]}

#
具体请求类型列举：

大厅界面

    name			# 起名字:客户端发送，content为名字。
    例：{"type":"name", "socket_id":22, "room":-1, "room_id":-1, "content":["Pony"]}

	create		    # 建立房间:客户端发送，content为房间号
    例：{"type":"create", "socket_id":22, "room":-1, "room_id":-1, "content":[8]}

	joinroom		# 进入房间: 客户端发送，content为房间号，客户端需要存一下自己的的房间号和房间内的ID(1,2,3,4),这么做是为了方便两边交互
    例: {"type":"joinroom", "socket_id":23, "room":-1, "room_id":-1, "content":[8]}

	ready   		# 游戏准备: 客户端发送，content为空。当同一房间四个同样的ready消息发出，服务器才会开始这个房间的游戏(ready++, startgame if ready==4)
    例: {"type":"ready", "socket_id":23, "room":8, "room_id":2, "content":[]}

    cancelready     # 取消准备: 客户端发送，content为空(ready--)
    例: {"type":"cancelready", "socket_id":23, "room":8, "room_id":2, "content":[]}

	quitroom		# 退出房间：客户端发送，content为空。
    例: {"type":"quitroom", "socket_id":23, "room":8, "room_id":2, "content":[]}
    
    roominfo        # 房间信息: 服务器发送，room_id为该客户端房间内ID，content为房间内玩家的信息。由两个字典构成，第一个字典是玩家名称，如果没有人就是空string，第二个字典是准备情况，没准备好就是空string。
    这条消息是房间内所有人都会收到的，只要有人加入或者退出房间，准备或者取消准备，服务器就会发送一遍
    例: {"type":"roominfo", "socket_id":0, "room":8, "room_id":2, "content":[{1:"Pony",2:"Sam",3:"",4:""},{1:"ready",2:"",3:"",4:""}]}
    
#
游戏界面

    wait            # 等待: 服务器发送，请求客户端等待，客户端UI可根据该条消息显示倒计时(60s)。
    等待选牌，等待打牌，等待吃碰杠胡同三种情况均使用该请求
    如果是等待选牌和等待出牌，则content内有当前玩家的房间ID(1~4)
    如果是吃碰杠胡，则content为空
    例: {"type":"wait", "socket_id":0, "room":8, "room_id":1, "content":[]}

    askcard         # 请求打牌: 服务器发送，请求客户端打出一张牌。content为空
    例: {"type":"askcard", "socket_id":0, "room":8, "room_id":1, "content":[]}

    playcard		# 打牌：客户端发送，content为牌的ID。
    例: {"type":"playcard", "socket_id":22, "room":8, "room_id":1, "content":[66]}


    card            # 发牌: 服务器发送，content为标有麻将牌ID的数组。
        -当游戏刚刚开始的时候，发送长度为9的数组。
        -当积分选牌完成之后，发送长度为2的数组。
        -当每回合发牌的时候，发送长度为1的数组。
    例: {"type":"card", "socket_id":0, "room":8, "room_id":1, "content":[66]}

    pair            # 发送牌组供大家积分选择: 服务器发送，content为5对麻将牌ID组成的数组
    例: {"type":"pair", "socket_id":0, "room":8, "room_id":1, "content":[[23,64],[12,99],[89,105],[14,68],[84,27]]}

    score           # 提交积分: 客户端发送，content为数字1~4(共5分)

    askchoice       # 请求选择: 服务器发送，content为空

    choice          # 提交选择：客户端发送，content为那对牌的index

    specialope      # 特殊情况: 指吃碰杠胡，content返回一个含有字典的数组, 字典内含有两个内容:ope和cards。
        peng    		# 碰牌：服务器发送，以询问是否碰，cards为三张牌的ID组成的数组，其中第一张为打出来的牌，另外两张为手牌

        chi         	# 吃牌：服务器发送，以询问是否吃。吃可能存在多种吃法，服务器会发送多次请求。客户端如何实现同时显示多种吃法比较麻烦，这一点暂定为选做吧)

	    gang        	# 杠牌：服务器发送，以询问是否杠。
        content中有四张牌，第一张依然是场上的牌

	    hu  			# 胡牌：服务器发送，以询问是否胡

	    zimo			# 自摸：服务器发送，以询问是否自摸

        极端例子:
        {
            "type":"specialope",
            "socket_id":0,
            "room":8,
            "room_id":1,
            "content":[{"ope":"chi","cards":[[66,69,74], [60,63,66]]},
                        {"ope":"peng","cards":[13,14,16]},
                        {"ope":"gang","cards":[13,14,15,16]}]
        }

    yes          # 确定特殊操作：客户端发送，以回复确定特殊操作。content为选择吃第几组, content为一个长度为5的数组，分别代表 [吃 碰 杠 胡 自摸]
    吃 的范围为[0,1,2,3]，0代表不做这个操作，别的代表选择吃的选项。
    碰 杠 胡 自摸 的范围均为[0,1]，0代表不做这个操作，别的代表做这个操作。
    例: {"type":"yes", "socket_id":22, "room":8, "room_id":1, "content":[2,0,0,0,0]}

    no				# 拒绝：客户端发送，以拒绝吃碰杠胡
    例: {"type":"no", "socket_id":22, "room":8, "room_id":1, "content":[]}


	otherplay		# 他人打牌：服务器发送，content为包含一个字典的数组，分别为玩家在房间里的ID和牌ID
    例: {"type":"otherplay", "socket_id":0, "room":8, "room_id":1, "content":[{player:2, card:66}]}

	otherchi    	# 他人吃牌：服务器发送，content为包含一个字典的数组，分别为玩家在房间里的ID，和他吃的三张牌的ID(就是chi里面传递的三张牌)
    例: {"type":"otherplay", "socket_id":0, "room":8, "room_id":2, "content":[{player:1, card:[66,69,73]}]}

	otherpeng   	# 他人碰牌：服务器发送

	othergang       # 他人杠牌：服务器发送

	otherhu     	# 他人胡牌：服务器发送
