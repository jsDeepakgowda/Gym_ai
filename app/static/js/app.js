class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        }

        this.state = false;
        this.messages = [];
    }

    display() {
        const { openButton, chatBox, sendButton } = this.args;

        openButton.addEventListener('click', () => this.toggleState(chatBox));
        sendButton.addEventListener('click', () => this.onSendButton(chatBox));

        const node = chatBox.querySelector('input');
        node.addEventListener("keyup", ({ key }) => {
            if (key === "Enter") {
                this.onSendButton(chatBox);
            }
        });
    }

    toggleState(chatbox) {
        this.state = !this.state;
        if (this.state) {
            chatbox.classList.add('chatbox--active');
            chatbox.querySelector('input').focus();  
        } else {
            chatbox.classList.remove('chatbox--active');
        }
    }

    onSendButton(chatbox) {
        var textField = chatbox.querySelector('input');
        let text1 = textField.value;

        if (text1 === "") {
            return;
        }

        // Add user's message
        let msg1 = { name: "User", message: text1 };
        this.messages.push(msg1);

        // Send the message to the backend API
        fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            body: JSON.stringify({ message: text1 }),
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json'
            },
        })
        .then(r => r.json())
        .then(r => {
            let msg2 = { name: "Sam", message: r.answer };  // Assuming `r.answer` contains the bot's response
            this.messages.push(msg2);
            this.updateChatText(chatbox);
            textField.value = '';  // Clear the input field after sending message
        })
        .catch((error) => {
            console.error('Error:', error);
            let msg2 = { name: "Sam", message: "Sorry, I didn't understand that." };
            this.messages.push(msg2);
            this.updateChatText(chatbox);
            textField.value = '';  // Clear the input field even on error
        });
    }

    updateChatText(chatbox) {
        var html = '';
        
        // Iterate through all messages and display them correctly
        this.messages.forEach((item) => {
            if (item.name === "Sam") {
                html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>';
            } else {
                html += '<div class="messages__item messages__item--operator">' + item.message + '</div>';
            }
        });

        const chatMessageContainer = chatbox.querySelector('.chatbox__messages');
        chatMessageContainer.innerHTML = html;
    }
}

// Usage
const chatbox = new Chatbox();
chatbox.display();
