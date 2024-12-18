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
        console.log('Attempting login with:', {
          username: this.username,
          password: '***'
        });

        const response = await uni.request({
          url: `${this.API_URL}/token`,
          method: 'POST',
          header: {
            'Content-Type': 'application/x-www-form-urlencoded'
          },
          data: `username=${encodeURIComponent(this.username)}&password=${encodeURIComponent(this.password)}`
        });

        console.log('Login response:', {
          statusCode: response.statusCode,
          data: response.data
        });

        if (response.statusCode === 200 && response.data.access_token) {
          this.token = response.data.access_token;
          this.isLoggedIn = true;
          await this.connectWebSocket();
          uni.showToast({ title: '登录成功', icon: 'success' });
        } else {
          throw new Error('Invalid login response');
        }
      } catch (error) {
        console.error('Login error:', error);
        uni.showToast({
          title: '登录失败，请重试',
          icon: 'none',
          duration: 2000
        });
        this.isLoggedIn = false;
        this.token = '';
      }
    },

    async register() {
      try {
        // Input validation
        if (!this.username || !this.password) {
          uni.showToast({
            title: '用户名和密码不能为空',
            icon: 'none'
          });
          return;
        }

        console.log('Attempting registration with:', {
          username: this.username,
          password: '***'
        });

        const response = await uni.request({
          url: `${this.API_URL}/register`,
          method: 'POST',
          header: {
            'Content-Type': 'application/json'
          },
          data: JSON.stringify({
            username: this.username,
            password: this.password
          })
        });

        console.log('Registration response:', {
          statusCode: response.statusCode,
          data: response.data
        });

        if (response.statusCode === 200) {
          uni.showToast({ title: '注册成功', icon: 'success' });
          await this.login(); // Automatically login after successful registration
        } else {
          const errorMsg = response.data?.detail || '注册失败';
          console.error('Registration failed:', errorMsg);
          uni.showToast({
            title: errorMsg,
            icon: 'none',
            duration: 2000
          });
        }
      } catch (error) {
        console.error('Registration error:', error);
        uni.showToast({
          title: '注册失败，请重试',
          icon: 'none',
          duration: 2000
        });
      }
    },

    connectWebSocket() {
      return new Promise((resolve, reject) => {
        if (!this.token) {
          console.error('No token available');
          uni.showToast({
            title: '未登录，请先登录',
            icon: 'none'
          });
          this.isLoggedIn = false;
          reject(new Error('No token available'));
          return;
        }

        console.log('Connecting WebSocket with token:', this.token.substring(0, 10) + '...');

        this.ws = uni.connectSocket({
          url: `${this.WS_URL}/ws/general?token=${this.token}`,
          header: {
            'Authorization': `Bearer ${this.token}`
          },
          complete: () => {
            console.log('WebSocket connection attempt completed');
          }
        });

        this.ws.onOpen(() => {
          console.log('WebSocket connection opened successfully');
          resolve();
        });

        this.ws.onError((error) => {
          console.error('WebSocket error:', error);
          this.isLoggedIn = false;
          reject(error);
        });

        this.ws.onMessage((res) => {
          try {
            const message = JSON.parse(res.data);
            this.messages.push(message);
            this.scrollToBottom();
          } catch (error) {
            console.error('Error parsing message:', error);
          }
        });

        this.ws.onClose((event) => {
          console.log('WebSocket connection closed with code:', event.code);
          // Only show reconnection message for unexpected closures
          if (event.code !== 1000) {
            uni.showToast({
              title: '连接断开，正在重新连接',
              icon: 'none',
              duration: 1000
            });
            // Attempt immediate reconnection for voice chat
            if (this.isLoggedIn) {
              this.connectWebSocket().catch(error => {
                console.error('Reconnection failed:', error);
              });
            }
          }
        });
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
