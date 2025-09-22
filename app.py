<!-- templates/index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>📄 Resume Assistant</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" />
    <style>
        .chat-container {
            max-width: 480px;
            margin: 20px auto;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
            background-color: white;
            font-family: 'Segoe UI', sans-serif;
        }
        .header {
            background: #9d50ff;
            color: white;
            padding: 16px 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-weight: 600;
        }
        .avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: white;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #9d50ff;
            font-size: 20px;
        }
        .status {
            font-size: 12px;
            color: #4ade80;
            margin-top: 4px;
            display: flex;
            align-items: center;
        }
        .status::before {
            content: "•";
            margin-right: 4px;
            background: #4ade80;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            display: inline-block;
        }
        .close-btn {
            font-size: 18px;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .close-btn:hover {
            transform: scale(1.1);
        }
        .message-group {
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 16px;
            height: calc(100vh - 200px);
            overflow-y: auto;
        }
        .user-message {
            align-self: flex-end;
        }
        .bot-message {
            align-self: flex-start;
        }
        .message-bubble {
            padding: 14px 18px;
            border-radius: 20px;
            max-width: 70%;
            word-wrap: break-word;
            font-size: 14px;
            line-height: 1.4;
            animation: fadeIn 0.3s ease-out;
        }
        .user-bubble {
            background: #9d50ff;
            color: white;
            align-self: flex-end;
        }
        .bot-bubble {
            background: #f1f1f1;
            color: #333;
            align-self: flex-start;
        }
        .input-area {
            padding: 16px;
            border-top: 1px solid #eee;
            display: flex;
            gap: 10px;
            background: #f8f9fa;
        }
        input[type="text"] {
            flex-grow: 1;
            padding: 12px 16px;
            border: none;
            border-radius: 20px;
            font-size: 14px;
            outline: none;
            background: white;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        button {
            background: #9d50ff;
            color: white;
            border: none;
            padding: 120px 20px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 44px;
            transition: background 0.2s;
            block-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        button:hover {
            background: #8b3df5;
        }
        .footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 12px;
            color: #999;
            margin-top: 8px;
            padding: 0 16px 12px;
        }
        .logo {
            font-weight: 600;
            color: #9d50ff;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .typing-indicator {
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 12px 16px;
            background: #f1f1f1;
            border-radius: 20px;
            max-width: 70%;
            margin-bottom: 12px;
        }
        .typing-dots {
            display: flex;
            gap: 4px;
        }
        .dot {
            width: 6px;
            height: 6px;
            background: #999;
            border-radius: 50%;
            animation: bounce 1.4s infinite ease-in-out;
        }
        .dot:nth-child(2) {
            animation-delay: 0.2s;
        }
        .dot:nth-child(3) {
            animation-delay: 0.4s;
        }
        @keyframes bounce {
            0%, 80%, 100% { transform: translateY(0); }
            40% { transform: translateY(-8px); }
        }
    </style>
</head>
<body class="bg-gray-100 min-h-screen flex items-center justify-center p-4">
    <div class="chat-container">
        <!-- Header -->
        <div class="header">
            <div class="flex items-center gap-3">
                <div class="avatar">
                    <i class="fas fa-robot"></i>
                </div>
                <div>
                    <div>Resume Assistant</div>
                    <div class="status">Online Now</div>
                </div>
            </div>
            <button class="close-btn">×</button>
        </div>

        <!-- Messages -->
        <div id="chatbox" class="message-group">
            <div class="bot-message">
                <div class="flex items-start gap-3">
                    <div class="avatar">
                        <i class="fas fa-robot"></i>
                    </div>
                    <div class="message-bubble bot-bubble">
                        Hi! I'm your Resume Assistant. Ask me about skills, experience, or projects.
                    </div>
                </div>
            </div>
        </div>

        <!-- Input Area -->
        <div class="input-area">
            <input type="text" id="userInput" placeholder="Type your question..." />
            <button onclick="sendMessage()">Send</button>
        </div>

        <!-- Footer -->
        <div class="footer">
            <div class="logo">Resume Assistant</div>
            <div>Powered by LangChain & Gemini</div>
    </div>

    <script>
        const chatbox = document.getElementById('chatbox');
        const userInput = document.getElementById('userInput');

        function addMessage(text, isUser) {
            const div = document.createElement('div');
            div.className = `message-group ${isUser ? 'user-message' : 'bot-message'}`;
            
            const bubble = document.createElement('div');
            bubble.className = `message-bubble ${isUser ? 'user-bubble' : 'bot-bubble'}`;
            bubble.textContent = text;

            div.appendChild(bubble);
            chatbox.appendChild(div);
            chatbox.scrollTop = chatbox.scrollHeight;
        }

        function showTyping() {
            const typingDiv = document.createElement('div');
            typingDiv.className = 'typing-indicator';
            typingDiv.innerHTML = '<div class="typing-dots"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>';
            chatbox.appendChild(typingDiv);
            chatbox.scrollTop = chatbox.scrollHeight;
        }

        function removeTyping() {
            const typingIndicator = chatbox.querySelector('.typing-indicator');
            if (typingIndicator) typingIndicator.remove();
        }

        function sendMessage() {
            const msg = userInput.value.trim();
            if (!msg) return;

            addMessage(msg, true);
            userInput.value = '';
            showTyping();

            fetch('/get', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: `msg=${encodeURIComponent(msg)}`
            })
            .then(response => response.text())
            .then(data => {
                removeTyping();
                addMessage(data, false);
            })
            .catch(err => {
                removeTyping();
                addMessage("Error: " + err, false);
            });
        }

        // Add Enter key support
        userInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') sendMessage();
        });
    </script>
</body>
</html>
