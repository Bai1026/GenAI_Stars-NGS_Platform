// document.addEventListener('DOMContentLoaded', function() {
//     document.getElementById('chat-form').addEventListener('submit', async function(event) {
//         event.preventDefault();
//         const messageInput = document.getElementById('message-input');
//         const message = messageInput.value;
//         messageInput.value = '';

//         // 添加用户消息到聊天窗口
//         const messagesDiv = document.getElementById('messages');
//         const userMessageDiv = document.createElement('div');
//         userMessageDiv.className = 'message user';
//         userMessageDiv.textContent = message;
//         messagesDiv.appendChild(userMessageDiv);

//         try {
//             // 发送请求到服务器
//             const response = await fetch('/chat/', {
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/json',
//                     'X-CSRFToken': getCookie('csrftoken')
//                 },
//                 body: JSON.stringify({ message: message })
//             });

//             const data = await response.json();

//             if (response.ok) {
//                 // 添加机器人回复到聊天窗口
//                 const botMessageDiv = document.createElement('div');
//                 botMessageDiv.className = 'message bot';
//                 botMessageDiv.textContent = data.response;
//                 messagesDiv.appendChild(botMessageDiv);
//             } else {
//                 console.error(data.error || 'An error occurred');
//                 // 处理错误响应
//                 const errorMessageDiv = document.createElement('div');
//                 errorMessageDiv.className = 'message error';
//                 errorMessageDiv.textContent = data.error || 'An error occurred';
//                 messagesDiv.appendChild(errorMessageDiv);
//             }

//         } catch (error) {
//             console.error('Error:', error);
//             // 处理网络错误
//             const errorMessageDiv = document.createElement('div');
//             errorMessageDiv.className = 'message error';
//             errorMessageDiv.textContent = 'A network error occurred';
//             messagesDiv.appendChild(errorMessageDiv);
//         }

//         // 滚动到最新消息
//         messagesDiv.scrollTop = messagesDiv.scrollHeight;
//     });
// });

// // 获取 CSRF 令牌的函数
// function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         const cookies = document.cookie.split(';');
//         for (let i = 0; i < cookies.length; i++) {
//             const cookie = cookies[i].trim();
//             // 判断这个 cookie 是否以 name 开头
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }


function toggleNav() {
    const sidebar = document.getElementById("sidebar");
    const content = document.getElementById("mainContent");

    if (sidebar.style.width === "200px") {
        sidebar.style.width = "0";
        content.classList.remove("active");
    } else {
        sidebar.style.width = "200px";
        content.classList.add("active");
    }
}

