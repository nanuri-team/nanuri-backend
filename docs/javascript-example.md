```javascript
// 소켓 100개 생성 (= 방에 유저 100명 접속)
let sockets = [];
for (let i = 0; i < 100; i++) {
    const socket = new WebSocket('ws://localhost:8080/ws/chat/my_room/?token=...');
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
        'message': `Hello, I am user ${index}!`,
        'format': 'text/plain',
    }));
}

// 모든 소켓 해제
for (let i = 0; i < 100; i++) {
    const socket = sockets[i];
    socket.close();
}
```

```javascript
const socket = new WebSocket('ws://localhost:8080/ws/chat/my_room/?token=...')
socket.onmessage = (e) => {
    const data = JSON.parse(e.data);
    console.log(data);
}
socket.send(JSON.stringify({
    'type': 'send_message',
    'message': '/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCABkAGQDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD5/ooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooA//2Q==',
    'format': 'image/jpeg',
}));
socket.close();
```
