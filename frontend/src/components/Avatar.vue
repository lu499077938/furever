<script setup>
const props = defineProps({
  src: { type: String, default: "" },
  size: { 
    type: String, 
    default: "medium",
    validator: (v) => ['small', 'medium', 'large'].includes(v)
  }
});

const fallback = "https://placehold.co/80x80/FFF7ED/F97316?text=🐾";
</script>

<template>
  <view class="avatar-wrapper" :class="`avatar--${size}`">
    <image 
      class="avatar" 
      :src="src || fallback" 
      mode="aspectFill" 
    />
    <view class="avatar-border"></view>
  </view>
</template>

<style lang="scss" scoped>
.avatar-wrapper {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.avatar {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: $bg-color-gray;
}

.avatar-border {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  border: $border-width-thick solid $border-color;
  pointer-events: none;
}

.avatar--small {
  width: 56rpx;
  height: 56rpx;
}

.avatar--medium {
  width: 80rpx;
  height: 80rpx;
}

.avatar--large {
  width: 120rpx;
  height: 120rpx;
}
</style>
