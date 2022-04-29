```javascript
// 소켓 100개 생성 (= 방에 유저 100명 접속)
let sockets = [];
for (let i = 0; i < 100; i++) {
    const socket = new WebSocket('ws://localhost:8080/ws/chat/my_room/');
    socket.onmessage = (e) => {
        const data = JSON.parse(e.data);
        console.log(data);
    }
    sockets.push(socket);
}

// 무작위로 30개 소켓을 고른 후 메시지 전송
for (let i = 0; i < 30; i++) {
    const index = Math.floor(Math.random() * 100);
    const socket = sockets[index];
    socket.send(JSON.stringify({
        'type': 'send_message',
        'message': `Hello, I am user ${index}!`
    }));
}

// 모든 소켓 해제
for (let i = 0; i < 100; i++) {
    const socket = sockets[i];
    socket.close();
}
```
