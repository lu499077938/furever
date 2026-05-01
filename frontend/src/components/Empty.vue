<script setup>
const props = defineProps({
  text: { type: String, default: "暂无内容" },
  icon: { type: String, default: "🐾" }
});
</script>

<template>
  <view class="empty-state">
    <view class="empty-icon">{{ icon }}</view>
    <text class="empty-text">{{ text }}</text>
  </view>
</template>

<style lang="scss" scoped>
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: $spacing-3xl $spacing-xl;
}

.empty-icon {
  font-size: 80rpx;
  margin-bottom: $spacing-base;
  animation: float 3s ease-in-out infinite;
}

.empty-text {
  font-size: $font-size-base;
  color: $text-color-muted;
  text-align: center;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-12rpx); }
}
</style>
