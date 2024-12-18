<template>
  <view class="voice-input">
    <button
      class="voice-btn"
      :class="{ recording: isRecording }"
      @mousedown="startRecording"
      @mouseup="stopRecording"
      @touchstart.prevent="startRecording"
      @touchend.prevent="stopRecording"
    >
      {{ isRecording ? '松开结束' : '按住说话' }}
    </button>
    <text v-if="recognizedText" class="recognized-text">{{ recognizedText }}</text>
  </view>
</template>

<script>
export default {
  name: 'VoiceInput',
  data() {
    return {
      isRecording: false,
      recognizedText: '',
      recognition: null,
      recorderManager: null,
      isTestMode: process.env.NODE_ENV === 'development' // Add test mode flag
    }
  },
  created() {
    this.recorderManager = uni.getRecorderManager()

    // Setup recorder manager events
    this.recorderManager.onStart(() => {
      console.log('开始录音')
    })

    this.recorderManager.onStop((res) => {
      // #ifdef MP-WEIXIN
      uni.showLoading({ title: '识别中...' })

      // Use WeChat's built-in recognition
      uni.uploadFile({
        url: 'https://api.weixin.qq.com/cgi-bin/media/voice/translatecontent',
        filePath: res.tempFilePath,
        name: 'voice',
        success: (uploadRes) => {
          const result = JSON.parse(uploadRes.data)
          if (result.result) {
            this.recognizedText = result.result
            this.$emit('onRecognized', result.result)
          }
        },
        fail: (error) => {
          console.error('语音识别失败：', error)
          uni.showToast({
            title: '语音识别失败',
            icon: 'none'
          })
        },
        complete: () => {
          uni.hideLoading()
        }
      })
      // #endif
    })

    this.recorderManager.onError((res) => {
      console.error('录音失败：', res)
      uni.showToast({
        title: '录音失败',
        icon: 'none'
      })
    })

    // #ifdef H5
    if (typeof window !== 'undefined') {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (SpeechRecognition) {
        try {
          this.recognition = new SpeechRecognition();
          this.recognition.continuous = false;
          this.recognition.interimResults = false;
          this.recognition.lang = 'zh-CN';

          this.recognition.onresult = (event) => {
            if (event.results && event.results[0] && event.results[0][0]) {
              const text = event.results[0][0].transcript;
              this.recognizedText = text;
              this.$emit('onRecognized', text);
              console.log('Speech recognized:', text);
            }
          };

          this.recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            uni.showToast({
              title: '语音识别出错',
              icon: 'none'
            });
            this.isRecording = false;
          };

          this.recognition.onend = () => {
            console.log('Speech recognition ended');
            this.isRecording = false;
          };
        } catch (error) {
          console.error('Failed to initialize speech recognition:', error);
        }
      }
    }
    // #endif
  },
  methods: {
    simulateVoiceRecognition() {
      console.log('Simulating voice recognition...');
      // Simulate processing time
      setTimeout(() => {
        const simulatedText = '这是一条测试语音消息';
        this.recognizedText = simulatedText;
        this.$emit('onRecognized', simulatedText);
        this.isRecording = false;
        console.log('Simulated voice recognition completed:', simulatedText);
      }, 1500);
    },
    startRecording(event) {
      if (event && event.preventDefault) {
        event.preventDefault();
      }
      this.isRecording = true;

      // #ifdef MP-WEIXIN
      uni.authorize({
        scope: 'scope.record',
        success: () => {
          this.recorderManager.start({
            duration: 60000,
            sampleRate: 16000,
            numberOfChannels: 1,
            encodeBitRate: 48000,
            format: 'mp3'
          })
        },
        fail: () => {
          uni.showToast({
            title: '请授权使用麦克风',
            icon: 'none'
          })
        }
      })
      // #endif

      // #ifdef H5
      if (this.recognition) {
        try {
          // In test mode, bypass microphone checks
          if (this.isTestMode) {
            console.log('Running in test mode - simulating voice input');
            this.simulateVoiceRecognition();
            return;
          }

          // Check for mediaDevices API support first
          if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            throw new Error('浏览器不支持音频输入');
          }

          // Check for available audio devices
          navigator.mediaDevices.enumerateDevices()
            .then(devices => {
              const hasAudioInput = devices.some(device => device.kind === 'audioinput');
              if (!hasAudioInput) {
                throw new Error('未检测到麦克风设备');
              }

              // If audio device exists, proceed with permission check
              return navigator.mediaDevices.getUserMedia({ audio: true });
            })
            .then(stream => {
              // Stop the stream immediately as we only needed it for permission
              stream.getTracks().forEach(track => track.stop());

              // Start voice recognition
              try {
                this.recognition.start();
                console.log('Voice recognition started');
              } catch (error) {
                console.error('Failed to start voice recognition:', error);
                this.isRecording = false;
                uni.showToast({
                  title: '语音识别启动失败，请重试',
                  icon: 'none'
                });
              }
            })
            .catch(error => {
              console.error('Microphone error:', error);
              this.isRecording = false;

              // Show appropriate error message based on the error
              let message = '麦克风权限检查失败';
              if (error.message === '未检测到麦克风设备') {
                message = '未检测到麦克风设备';
              } else if (error.message === '浏览器不支持音频输入') {
                message = '浏览器不支持音频输入';
              } else if (error.name === 'NotAllowedError') {
                message = '请允许使用麦克风';
              }

              uni.showToast({
                title: message,
                icon: 'none'
              });
            });
        } catch (error) {
          console.error('Voice recognition error:', error);
          this.isRecording = false;
          uni.showToast({
            title: '语音识别启动失败',
            icon: 'none'
          });
        }
      } else {
        this.isRecording = false;
        uni.showToast({
          title: '当前浏览器不支持语音识别',
          icon: 'none'
        });
      }
      // #endif

      // #ifdef APP-PLUS
      plus.speech.startRecognize({
        engine: 'local',
        lang: 'zh-cn',
        success: (text) => {
          this.recognizedText = text
          this.$emit('onRecognized', text)
        },
        error: (e) => {
          console.error('语音识别失败:', e)
          uni.showToast({
            title: '语音识别失败',
            icon: 'none'
          })
        }
      })
      // #endif
    },
    stopRecording(event) {
      if (event && event.preventDefault) {
        event.preventDefault();
      }
      this.isRecording = false;

      // #ifdef APP-PLUS
      plus.speech.stopRecognize();
      // #endif

      // #ifdef H5
      if (this.recognition) {
        try {
          this.recognition.stop();
          console.log('Speech recognition stopped');
        } catch (error) {
          console.error('Error stopping recognition:', error);
        }
      }
      // #endif

      // #ifdef MP-WEIXIN
      this.recorderManager.stop();
      // #endif
    }
  }
}
</script>

<style>
.voice-input {
  padding: 10px;
}

.voice-btn {
  width: 200rpx;
  height: 80rpx;
  line-height: 80rpx;
  text-align: center;
  background-color: #f0f0f0;
  border-radius: 40rpx;
  font-size: 28rpx;
}

.voice-btn.recording {
  background-color: #e0e0e0;
}

.recognized-text {
  margin-top: 20rpx;
  font-size: 28rpx;
  color: #666;
}
</style>
