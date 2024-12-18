<template>
  <view class="content">
    <view v-if="!isLoggedIn" class="auth-container">
      <view class="form-group">
        <input type="text" v-model="username" placeholder="用户名" class="input" />
        <input type="password" v-model="password" placeholder="密码" class="input" />
        <button @tap="login" class="btn">登录</button>
        <button @tap="register" class="btn register">注册</button>
      </view>
    </view>

    <view v-else class="chat-container">
      <scroll-view class="message-list" scroll-y="true" :scroll-top="scrollTop">
        <view v-for="(msg, index) in messages" :key="index" class="message"
              :class="{ 'message-self': msg.sender === username }">
          <view class="message-sender">{{ msg.sender }}</view>
          <view class="message-content">{{ msg.content }}</view>
          <view class="message-time">{{ formatTime(msg.timestamp) }}</view>
        </view>
      </scroll-view>

      <view class="input-area">
        <input type="text" v-model="currentMessage" placeholder="输入消息..."
               class="message-input" @confirm="sendMessage" />
        <VoiceInput @onRecognized="handleVoiceRecognition" />
        <button @tap="sendMessage" class="send-btn">发送</button>
      </view>
    </view>
  </view>
</template>

<script>
import VoiceInput from '@/components/VoiceInput.vue'

export default {
  components: {
    VoiceInput
  },
  data() {
    return {
      username: '',
      password: '',
      isLoggedIn: false,
      token: '',
      messages: [],
      currentMessage: '',
      scrollTop: 0,
      ws: null,
      API_URL: 'https://app-efsgzpzt.fly.dev',
      WS_URL: 'wss://app-efsgzpzt.fly.dev'
    }
  },
  methods: {
    async login() {
      try {
        const response = await uni.request({
          url: `${this.API_URL}/token`,
          method: 'POST',
          header: {
            'Content-Type': 'application/x-www-form-urlencoded'
          },
          data: `username=${encodeURIComponent(this.username)}&password=${encodeURIComponent(this.password)}`
        });

        if (response.statusCode === 200) {
          this.token = response.data.access_token;
          this.isLoggedIn = true;
          this.connectWebSocket();
          uni.showToast({ title: '登录成功', icon: 'success' });
        }
      } catch (error) {
        uni.showToast({ title: '登录失败', icon: 'none' });
      }
    },

    async register() {
      try {
        const response = await uni.request({
          url: `${this.API_URL}/register`,
          method: 'POST',
          data: {
            username: this.username,
            password: this.password
          }
        });

        if (response.statusCode === 200) {
          uni.showToast({ title: '注册成功', icon: 'success' });
        }
      } catch (error) {
        uni.showToast({ title: '注册失败', icon: 'none' });
      }
    },

    connectWebSocket() {
      this.ws = uni.connectSocket({
        url: `${this.WS_URL}/ws/general?token=${this.token}`,
        success: () => {
          console.log('WebSocket connected');
        }
      });

      this.ws.onMessage((res) => {
        const message = JSON.parse(res.data);
        this.messages.push(message);
        this.scrollToBottom();
      });

      this.ws.onClose(() => {
        setTimeout(() => this.connectWebSocket(), 1000);
      });
    },

    sendMessage() {
      if (this.currentMessage.trim() && this.ws) {
        this.ws.send({
          data: this.currentMessage,
          success: () => {
            this.currentMessage = '';
          }
        });
      }
    },

    scrollToBottom() {
      setTimeout(() => {
        const query = uni.createSelectorQuery();
        query.select('.message-list').boundingClientRect();
        query.exec((res) => {
          if (res[0]) {
            this.scrollTop = res[0].height;
          }
        });
      }, 100);
    },

    formatTime(timestamp) {
      return new Date(timestamp).toLocaleTimeString();
    },

    handleVoiceRecognition(text) {
      this.currentMessage = text
      this.sendMessage()
    }
  }
}
</script>

<style>
.content {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.auth-container {
  padding: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.input {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.btn {
  padding: 10px;
  background-color: #007AFF;
  color: white;
  border: none;
  border-radius: 4px;
}

.btn.register {
  background-color: #5856D6;
}

.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.message-list {
  flex: 1;
  padding: 10px;
}

.message {
  margin-bottom: 10px;
  max-width: 80%;
}

.message-self {
  margin-left: auto;
  text-align: right;
}

.message-sender {
  font-size: 12px;
  color: #666;
}

.message-content {
  background-color: #f0f0f0;
  padding: 8px 12px;
  border-radius: 8px;
  margin: 4px 0;
}

.message-self .message-content {
  background-color: #007AFF;
  color: white;
}

.message-time {
  font-size: 10px;
  color: #999;
}

.input-area {
  padding: 10px;
  border-top: 1px solid #eee;
  display: flex;
  gap: 10px;
  align-items: center;
}

.message-input {
  flex: 1;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.send-btn {
  padding: 8px 16px;
  background-color: #007AFF;
  color: white;
  border: none;
  border-radius: 4px;
}
</style>
