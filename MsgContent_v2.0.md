# MsgContent

客户端通讯的JSON格式:

    "type": 请求类型，如name, create等

    "socket_id": 客户端连接服务器后，服务器会将会话存入数组中，返回该会话的index + 1(可以理解为account)。如果是服务器发送的请求，socket_id设为0。

    "room": 所在的房间号。如果没有加入房间，默认值为-1

    "room_id": 所在房间内的顺序，范围是[-1,1,2,3,4]。其中-1代表没有加入房间时的默认值

    "content": 请求内容。考虑到某些请求会携带多个内容，所以设为一个数组

    {"type":"STRING", "socket_id":"STRING", "room":"STRING", "room_id":"STRING", "content":"STRING"}

服务器通讯的JSON格式:
    没有"socket_id"这一项。


#
具体请求类型列举：

大厅界面

    id              # 初次连接回复: 服务器发送，content为socket_id。
    例：{"type":"id", "room":-1, "room_id":-1, "content":"2"}

    // name			# 起名字:客户端发送，content为名字。
    例：{"type":"name", "socket_id":"22", "room":"-1", "room_id":"-1", "content":"Pony"}

	createroom		# 建立房间:客户端发送，content为空，服务器会返回roominfo(见下)
    例：{"type":"create", "socket_id":"22", "room":"-1", "room_id":"-1", "content":"8"}

	joinroom		# 进入房间: 客户端发送，这个时候的room就是要加入的房间号，content为自己的名字，客户端需要根据回复的roominfo来存一下自己的的房间号和房间内的ID(1,2,3,4)
    例: {"type":"joinroom", "socket_id":"23", "room":"-1", "room_id":"-1", "content":"8"}

    roomnotfound    # 房间不存在: 服务器发送
    例: {"type":"roomnotfound"}
    
	ready   		# 游戏准备: 客户端发送，content为空。当同一房间四个同样的ready消息发出，服务器才会开始这个房间的游戏
    例: {"type":"ready", "socket_id":"23", "room":"8", "room_id":"2", "content":null}

    cancelready     # 取消准备: 客户端发送，content为空(ready--)
    例: {"type":"cancelready", "socket_id":"23", "room":"8", "room_id":"2", "content":null}

	quitroom		# 退出房间：客户端发送，content为空。
    例: {"type":"quitroom", "socket_id":"23", "room":"8", "room_id":"2", "content":null}
    
    roominfo        # 房间信息: 服务器发送，room_id为该客户端房间内ID，content为name和ready情况。没有人的地方名字用_代替。
    例: {"type":"roominfo", "socket_id":"0", "room":"8", "room_id":"2", "name":"Pony Sam _ _", "ready":"1 0 0 0"}
    
#
游戏界面

    college         # 书院类型发送: 服务器发送，content为两个不上场的的书院ID(1~6)。
    在此之后，游戏需要出现选导师界面，玩家需要发送自己的选择
    例: {"type":"college", "room":"8", "room_id":"1", "content":"1 3"}
    
    supervisor      # 导师选择发送: 客户端发送，content为导师ID。
    例: {"type":"supervisor", "room":"8", "room_id":"1", "content":"1"}

    askcard         # 请求打牌: 服务器发送，请求客户端打出一张牌。content为需要打牌的玩家
    例: {"type":"askcard", "room":"8", "room_id":"1", "content":"1"}

    playcard		# 打牌：客户端发送，content为牌的ID。
    例: {"type":"playcard", "socket_id":"22", "room":"8", "room_id":"1", "content":"66"}

    initcard            # 发初始牌: 服务器发送，当游戏刚刚开始的时候，发送含有4*9个数字的字符串。前9个默认为1的，接着9个为2的，再9个为3的，最后9个为4的
    例: {"type":"initcard", "room":"8", "room_id":"1", "content":"66 21..."}

    card            # 发牌：服务器向四个客户端发送，"player"为客户端ID，"card"为一/两张牌的ID。
    我对前端想法：积分选课的话，有人选走了牌之后，收到这个消息，客户端直接移牌到那个玩家的牌堆里，这样就相当于更新了一下剩下的卡组。
    例: {"type":"card", "room":"8", "room_id":"1", "player":"3", "content":"66 21"}

    pair            # 发送牌组供大家积分选择: 服务器发送，content为5对麻将牌ID组成的数组
    例: {"type":"pair", "room":"8", "room_id":"1", "content":"23 64 12 99 89 105 14 68 84 27"}

    score           # 提交积分: 客户端发送，content为数字1~4(共5分)

    askchoice       # 请求选择: 服务器发送，content为需要做出选择的玩家房间ID。别的玩家可以根据个ID更新UI

    choice          # 提交选择：客户端发送，content为那对牌的index

    specialope      # 特殊情况: 指吃碰杠胡，content返回一个含有字典的数组, 字典内含有两个内容:ope和cards。
        peng    		# 碰牌：服务器发送，以询问是否碰，cards为三张牌的ID组成的数组，其中第一张为打出来的牌，另外两张为手牌

        chi         	# 吃牌：服务器发送，以询问是否吃。吃可能存在多种吃法

	    gang        	# 杠牌：服务器发送，以询问是否杠。
        content中有四张牌，第一张依然是场上的牌

	    hu  			# 胡牌：服务器发送，以询问是否胡

	    zimo			# 自摸：服务器发送，以询问是否自摸

        极端例子:
        {
            "type":"specialope",
            "room":8,
            "room_id":1,
            "chi1":"32 36 40",
            "chi2":"28 32 36",
            "chi3": null,
            "peng": null,
            "gang": null,
            "hu":"0"
        }

    opereply          # 确定特殊操作：客户端发送，以回复确定特殊操作。content为0~6的数字。
        0：不做任何操作
        1；吃的第一种情况
        2：吃的第二种情况
        3：吃的第三种情况
        4：碰
        5：杠
        6：胡
    例: {"type":"opereply", "socket_id":22, "room":8, "room_id":1, "content":"0"}

	play		# 客户端打牌：服务器发送，content为玩家在房间里的ID和牌ID
    例: {"type":"play", "room":8, "room_id":1, "player":"2", "card":"66"}

	cpg    	# 客户端吃碰杠牌：服务器发送，kind为"c"，"p"或"g"，content为玩家在房间里的ID，和他吃碰杠的三/四张牌的ID(因为是直接显示，所以先不管怎么出)
    例: {"type":"cpg", "room":"8", "room_id":"2", "player":"1", "kind":"c" ,"card":"66 69 73"}

	hu     	# 他人胡牌：服务器发送给其他所有玩家，"player"就是和牌玩家，"score"就是总分，"content"就是胡的牌型
    例: {"type":"hu", "room":"8", "room_id":"2", "player":"1", "score"："3000", "content": "段幺+1000 平胡+1000 退课警告+1000"}
    New: {"type":"hu", "room":"8", "room_id":"2", "player":"player1name", "score"："3000", "content": "段幺+1000 平胡+1000 退课警告+1000","card":"1 2 3 4 5 6 7 8 9 10 11 12 13 14"}

    end     # 结束游戏：服务器发送给其他所有玩家，"player"是玩家由高到低的分数，"score"是对应的分数
    例: {"type":"end", "room":"8", "room_id":"2", "player":"c a b d", "score": "1000 800 790 20"}
    
    mook    # 嘲讽：服务器发送给其他所有玩家，"player"是发起嘲讽的人，"content" 是嘲讽内容的ID
    例: {"type":"mook", "room":"8", "room_id":"2", "player":"1", "content": "1"}