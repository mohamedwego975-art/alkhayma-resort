<template>
  <div class="chat-bubble-container">
    <!-- Chat Toggle Button -->
    <button
      @click="toggleChat"
      class="chat-toggle-btn"
      :aria-label="isOpen ? $t('chat.close') : $t('chat.open')"
    >
      <span v-if="!isOpen" class="icon">💬</span>
      <span v-else class="icon">✕</span>
      <span v-if="unreadCount > 0 && !isOpen" class="badge">{{ unreadCount }}</span>
    </button>

    <!-- Chat Window -->
    <Transition name="slide-up">
      <div v-if="isOpen" class="chat-window">
        <!-- Header -->
        <div class="chat-header">
          <div class="header-info">
            <span class="bot-avatar">🤖</span>
            <div class="header-text">
              <h3>{{ $t('chat.title') }}</h3>
              <span class="status" :class="{ online: isConnected }">
                {{ isConnected ? $t('chat.online') : $t('chat.offline') }}
              </span>
            </div>
          </div>
          <button @click="toggleChat" class="close-btn" aria-label="Close chat">
            ✕
          </button>
        </div>

        <!-- Messages -->
        <div ref="messagesContainer" class="messages-container">
          <div
            v-for="(message, index) in messages"
            :key="index"
            class="message"
            :class="{ user: message.role === 'user', assistant: message.role === 'assistant' }"
          >
            <div class="message-avatar">
              {{ message.role === 'user' ? '👤' : '🤖' }}
            </div>
            <div class="message-content">
              <p>{{ message.content }}</p>
              <span class="message-time">{{ formatTime(message.timestamp) }}</span>
            </div>
          </div>

          <!-- Typing Indicator -->
          <div v-if="isTyping" class="message assistant typing">
            <div class="message-avatar">🤖</div>
            <div class="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>

        <!-- Suggested Questions -->
        <div v-if="suggestedQuestions.length > 0 && !isTyping" class="suggested-questions">
          <button
            v-for="(question, index) in suggestedQuestions"
            :key="index"
            @click="sendMessage(question)"
            class="suggestion-btn"
          >
            {{ question }}
          </button>
        </div>

        <!-- Input -->
        <div class="chat-input-container">
          <input
            v-model="newMessage"
            @keyup.enter="sendMessage(newMessage)"
            type="text"
            :placeholder="$t('chat.placeholder')"
            class="chat-input"
            :disabled="isTyping"
          />
          <button
            @click="sendMessage(newMessage)"
            class="send-btn"
            :disabled="!newMessage.trim() || isTyping"
          >
            ➤
          </button>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

interface Message {
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

// State
const isOpen = ref(false)
const messages = ref<Message[]>([
  {
    role: 'assistant',
    content: t('chat.welcome'),
    timestamp: new Date()
  }
])
const newMessage = ref('')
const isTyping = ref(false)
const isConnected = ref(true)
const unreadCount = ref(0)
const messagesContainer = ref<HTMLDivElement>()

// Suggested questions
const suggestedQuestions = computed(() => [
  t('chat.suggestions.rooms'),
  t('chat.suggestions.pricing'),
  t('chat.suggestions.amenities'),
  t('chat.suggestions.booking')
])

// Methods
const toggleChat = () => {
  isOpen.value = !isOpen.value
  if (isOpen.value) {
    unreadCount.value = 0
    scrollToBottom()
  }
}

const formatTime = (date: Date): string => {
  return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
}

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

const sendMessage = async (content: string) => {
  if (!content.trim() || isTyping.value) return

  // Add user message
  messages.value.push({
    role: 'user',
    content: content.trim(),
    timestamp: new Date()
  })

  newMessage.value = ''
  isTyping.value = true
  scrollToBottom()

  try {
    // Call AI service
    const response = await fetch('http://localhost:8001/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: content.trim(),
        session_id: 'web-chat',
        language: localStorage.getItem('locale') || 'en'
      })
    })

    if (!response.ok) throw new Error('Failed to get response')

    const data = await response.json()

    // Add assistant response
    messages.value.push({
      role: 'assistant',
      content: data.response || t('chat.fallback'),
      timestamp: new Date()
    })
  } catch (error) {
    console.error('Chat error:', error)
    messages.value.push({
      role: 'assistant',
      content: t('chat.error'),
      timestamp: new Date()
    })
  } finally {
    isTyping.value = false
    scrollToBottom()
  }
}

// Auto-scroll on new messages
watch(messages, scrollToBottom, { deep: true })

// Track unread messages when chat is closed
watch(messages, () => {
  if (!isOpen.value) {
    unreadCount.value++
  }
}, { deep: true })

onMounted(() => {
  // Check AI service health
  fetch('http://localhost:8001/health')
    .then(() => { isConnected.value = true })
    .catch(() => { isConnected.value = false })
})
</script>

<style scoped>
.chat-bubble-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
}

.chat-toggle-btn {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
  transition: transform 0.3s, box-shadow 0.3s;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chat-toggle-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
}

.badge {
  position: absolute;
  top: -5px;
  right: -5px;
  background: #ff4757;
  color: white;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  font-size: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

.chat-window {
  position: absolute;
  bottom: 80px;
  right: 0;
  width: 350px;
  height: 500px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chat-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.bot-avatar {
  font-size: 28px;
}

.header-text h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
}

.status {
  font-size: 12px;
  opacity: 0.8;
}

.status.online {
  color: #2ecc71;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 20px;
  cursor: pointer;
  padding: 4px;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  background: #f8f9fa;
}

.message {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
  align-items: flex-start;
}

.message.user {
  flex-direction: row-reverse;
}

.message-avatar {
  font-size: 20px;
  flex-shrink: 0;
}

.message-content {
  max-width: 70%;
  padding: 12px;
  border-radius: 16px;
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.message.user .message-content {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.message-time {
  font-size: 11px;
  opacity: 0.6;
  margin-top: 4px;
  display: block;
}

.typing-indicator {
  display: flex;
  gap: 4px;
  padding: 12px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  background: #667eea;
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out both;
}

.typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
.typing-indicator span:nth-child(2) { animation-delay: -0.16s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

.suggested-questions {
  padding: 8px 16px;
  background: white;
  border-top: 1px solid #eee;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.suggestion-btn {
  background: #f0f0f0;
  border: none;
  padding: 8px 12px;
  border-radius: 16px;
  font-size: 12px;
  cursor: pointer;
  transition: background 0.2s;
}

.suggestion-btn:hover {
  background: #667eea;
  color: white;
}

.chat-input-container {
  display: flex;
  padding: 16px;
  background: white;
  border-top: 1px solid #eee;
  gap: 8px;
}

.chat-input {
  flex: 1;
  border: 1px solid #ddd;
  border-radius: 24px;
  padding: 12px 16px;
  font-size: 14px;
  outline: none;
}

.chat-input:focus {
  border-color: #667eea;
}

.send-btn {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: white;
  font-size: 18px;
  cursor: pointer;
  transition: transform 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.send-btn:hover:not(:disabled) {
  transform: scale(1.05);
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Transitions */
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.3s ease;
}

.slide-up-enter-from,
.slide-up-leave-to {
  opacity: 0;
  transform: translateY(20px);
}
</style>
