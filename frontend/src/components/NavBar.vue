<script setup>
defineProps({
  title: { type: String, default: "宠光" },
  background: { type: Boolean, default: false },
  fixed: { type: Boolean, default: false }
});

defineEmits(['title-click']);
</script>

<template>
  <view class="navbar-wrapper" :class="{ 'is-fixed': fixed }">
    <view class="navbar" :class="{ 'has-background': background }">
      <view class="title-area" @click="$emit('title-click')">
        <slot name="title">
          <view class="default-title">
            <text class="title-icon">🐾</text>
            <text class="title-text">{{ title }}</text>
          </view>
        </slot>
      </view>
      <view class="actions">
        <slot />
      </view>
    </view>
    <view v-if="fixed" class="navbar-placeholder"></view>
  </view>
</template>

<style lang="scss" scoped>
.navbar-wrapper {
  width: 100%;
}

.is-fixed {
  .navbar {
    position: fixed;
    top: var(--window-top, 0);
    left: 0;
    right: 0;
    z-index: $z-index-fixed;
  }
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: $spacing-base $spacing-lg;
  box-sizing: border-box;
  transition: all $transition-base;

  &.has-background {
    background: $bg-color-warm;
    border-bottom: $border-width-thick solid $border-color;
    box-shadow: $box-shadow-sm;
  }
}

.title-area {
  display: flex;
  align-items: center;
}

.default-title {
  display: flex;
  align-items: center;
  gap: $spacing-xs;
}

.title-icon {
  font-size: 36rpx;
}

.title-text {
  font-size: $font-size-xl;
  font-weight: $font-weight-bold;
  color: $primary-color;
}

.actions {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
}

.navbar-placeholder {
  height: 104rpx;
}
</style>
