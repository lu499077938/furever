<template>
  <view class="pet-stick">
    <svg viewBox="0 0 100 300" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <!-- 签身 -->
      <path d="M 10 60 L 50 10 L 90 60 L 90 290 L 10 290 Z" :fill="isBest ? '#FFD700' : '#FFE066'" stroke="#D00000" stroke-width="4" stroke-linejoin="round" />
      
      <!-- 签文 -->
      <text x="50" y="100" font-size="36" font-family="STKaiti, KaiTi, serif" font-weight="bold" fill="#D00000" text-anchor="middle">
        <tspan v-for="(char, i) in text.split('')" :key="i" x="50" :dy="i === 0 ? 0 : 40">{{ char }}</tspan>
      </text>
    </svg>
  </view>
</template>

<script setup>
defineProps({
  text: {
    type: String,
    default: '签'
  },
  isBest: {
    type: Boolean,
    default: false
  }
});
</script>

<style scoped>
.pet-stick {
  width: 100%;
  height: 100%;
}
</style>
