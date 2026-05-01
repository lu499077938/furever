<script setup>
const props = defineProps({
  text: { type: String, default: "加载中..." }
});
</script>

<template>
  <view class="loading-state">
    <view class="loading-spinner">
      <view class="spinner-dot" v-for="i in 3" :key="i"></view>
    </view>
    <text class="loading-text">{{ text }}</text>
  </view>
</template>

<style lang="scss" scoped>
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: $spacing-xl;
}

.loading-spinner {
  display: flex;
  gap: 12rpx;
  margin-bottom: $spacing-sm;
}

.spinner-dot {
  width: 16rpx;
  height: 16rpx;
  border-radius: 50%;
  background: linear-gradient(135deg, $primary-color 0%, $secondary-color 100%);
  animation: bounce 1.4s ease-in-out infinite;

  &:nth-child(1) { animation-delay: 0s; }
  &:nth-child(2) { animation-delay: 0.2s; }
  &:nth-child(3) { animation-delay: 0.4s; }
}

.loading-text {
  font-size: $font-size-sm;
  color: $text-color-muted;
}

@keyframes bounce {
  0%, 80%, 100% {
    transform: scale(0.8);
    opacity: 0.5;
  }
  40% {
    transform: scale(1.2);
    opacity: 1;
  }
}
</style>
