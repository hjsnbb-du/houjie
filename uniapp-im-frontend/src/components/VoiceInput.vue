<template>
  <view class="voice-input">
    <button
      class="voice-btn"
      :class="{ recording: isRecording }"
      @touchstart="startRecording"
      @touchend="stopRecording"
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
      recorderManager: null
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
    if (typeof window !== 'undefined' && window.webkitSpeechRecognition) {
      this.recognition = new window.webkitSpeechRecognition()
      this.recognition.continuous = false
      this.recognition.interimResults = false
      this.recognition.lang = 'zh-CN'

      this.recognition.onresult = (event) => {
        const text = event.results[0][0].transcript
        this.recognizedText = text
        this.$emit('onRecognized', text)
      }
    }
    // #endif
  },
  methods: {
    startRecording() {
      this.isRecording = true

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
        this.recognition.start()
      } else {
        uni.showToast({
          title: '当前浏览器不支持语音识别',
          icon: 'none'
        })
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
    stopRecording() {
      this.isRecording = false

      // #ifdef APP-PLUS
      plus.speech.stopRecognize()
      // #endif

      // #ifdef H5
      if (this.recognition) {
        this.recognition.stop()
      }
      // #endif

      // #ifdef MP-WEIXIN
      this.recorderManager.stop()
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
