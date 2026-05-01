<script setup>
defineProps({
  points: { type: Number, default: 0 },
  size: { 
    type: String, 
    default: 'medium',
    validator: (v) => ['small', 'medium', 'large'].includes(v)
  }
});
</script>

<template>
  <view class="points-badge" :class="`points-badge--${size}`">
    <text class="points-icon">✦</text>
    <text class="points-value">{{ points }}</text>
  </view>
</template>

<style lang="scss" scoped>
.points-badge {
  display: inline-flex;
  align-items: center;
  gap: 6rpx;
  background: linear-gradient(135deg, $primary-color 0%, $secondary-color 100%);
  border-radius: $border-radius-full;
  box-shadow: 
    0 4rpx 12rpx rgba($primary-color, 0.3),
    inset 0 2rpx 4rpx rgba(255, 255, 255, 0.3);
  border: 2rpx solid rgba(255, 255, 255, 0.2);
}

.points-icon {
  color: rgba(255, 255, 255, 0.9);
  font-size: 20rpx;
}

.points-value {
  color: $text-color-inverse;
  font-weight: $font-weight-bold;
}

.points-badge--small {
  padding: 6rpx 14rpx;
  
  .points-icon { font-size: 18rpx; }
  .points-value { font-size: $font-size-xs; }
}

.points-badge--medium {
  padding: 8rpx 18rpx;
  
  .points-icon { font-size: 20rpx; }
  .points-value { font-size: $font-size-sm; }
}

.points-badge--large {
  padding: 12rpx 24rpx;
  
  .points-icon { font-size: 24rpx; }
  .points-value { font-size: $font-size-base; }
}
</style>
