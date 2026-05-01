<template>
  <view class="page">
    <view class="hero">
      <text class="pet-peek">🐾</text>
      <text class="hero-title">萌宠签到领好礼</text>
      <text class="hero-sub">连续打卡，给主子攒口粮～</text>

      <view class="hero-deco">
        <text class="deco deco--a">🦴</text>
        <text class="deco deco--b">🐟</text>
        <text class="deco deco--c">🎾</text>
        <text class="deco deco--d">🍖</text>
        <text class="deco deco--e">🐾</text>
      </view>
    </view>

    <view class="card">
      <view class="ribbon"><text class="ribbon-text">萌宠福利</text></view>

      <view class="streak-row">
        <text class="streak-label">已连续打卡</text>
        <text class="streak-num">{{ status.streak_days || 0 }}</text>
        <text class="streak-label">天</text>
      </view>

      <view class="grid">
        <view
          v-for="day in 7"
          :key="day"
          class="grid-cell"
          :class="{
            'grid-cell--done': day <= completedInCycle,
            'grid-cell--pop': celebrateDay === day,
          }"
        >
          <view class="cell-inner">
            <text v-if="day <= completedInCycle" class="paw-mark">🐾</text>
            <text v-else class="reward-ico">{{ rewardIconForDay(day) }}</text>
          </view>
          <text class="day-label">{{ day }}天</text>
        </view>
      </view>

      <view v-if="status.checked_in_today && status.today_fortune" class="fortune-strip">
        <view class="fortune-head">
          <text class="fortune-level" :class="{ 'fortune-level--best': isBestFortune }">
            {{ status.today_fortune.level }}
          </text>
          <text v-if="displayPoints > 0" class="fortune-points">+{{ displayPoints }} 积分</text>
          <text v-else class="fortune-points fortune-points--muted">奖励已领</text>
        </view>
        <text class="fortune-desc">{{ status.today_fortune.content }}</text>
      </view>

      <PetButton
        class="cta"
        block
        size="large"
        :type="status.checked_in_today ? 'secondary' : 'primary'"
        :disabled="locked || status.checked_in_today"
        :loading="animating"
        @click="doCheckin"
      >
        {{ status.checked_in_today ? "今日已打卡" : "打卡领奖励" }}
      </PetButton>
    </view>
  </view>
</template>

<script setup>
import { ref, computed } from "vue";
import { onShow } from "@dcloudio/uni-app";
import { checkinApi, checkinStatusApi } from "../../api/checkin";
import { useButtonLock } from "../../composables/useButtonLock";
import PetButton from "../../components/PetButton.vue";

const status = ref({});
const lastPoints = ref(0);
const animating = ref(false);
const celebrateDay = ref(0);
const { locked, run } = useButtonLock();

const isBestFortune = computed(() => status.value.today_fortune?.level === "上上签");

const displayPoints = computed(() => {
  const fromStatus = status.value.points_earned_today;
  if (typeof fromStatus === "number" && fromStatus > 0) return fromStatus;
  return lastPoints.value > 0 ? lastPoints.value : 0;
});

const completedInCycle = computed(() => {
  const s = status.value.streak_days || 0;
  if (s === 0) return 0;
  const mod = s % 7;
  return mod === 0 ? 7 : mod;
});

function rewardIconForDay(day) {
  if (day === 3 || day === 6) return "🎁";
  if (day === 4 || day === 5 || day === 7) return "⭐";
  return "🦴";
}

async function refresh() {
  try {
    status.value = await checkinStatusApi();
  } catch (_e) {
    status.value = { checked_in_today: false, streak_days: 0 };
  }
}

function doCheckin() {
  run(async () => {
    animating.value = true;
    celebrateDay.value = 0;
    await new Promise((resolve) => setTimeout(resolve, 450));
    try {
      const data = await checkinApi();
      status.value = data;
      lastPoints.value = Math.max(1, data.points_earned || 1);
      const s = data.streak_days || 0;
      const mod = s % 7;
      celebrateDay.value = mod === 0 ? 7 : mod;
      setTimeout(() => {
        celebrateDay.value = 0;
      }, 600);
    } finally {
      animating.value = false;
    }
  });
}

onShow(() => refresh());
</script>

<style lang="scss" scoped>
@import "@/uni.scss";

.page {
  min-height: 100vh;
  padding: $spacing-xl $spacing-lg calc(#{$spacing-lg} + env(safe-area-inset-bottom));
  box-sizing: border-box;
  background: linear-gradient(
    180deg,
    $checkin-gradient-top 0%,
    $checkin-gradient-mid 42%,
    $checkin-gradient-bottom 100%
  );
}

.hero {
  position: relative;
  text-align: center;
  padding: $spacing-base 0 120rpx;
}

.pet-peek {
  display: block;
  font-size: 64rpx;
  line-height: 1.2;
  margin-bottom: $spacing-xs;
  filter: drop-shadow(0 6rpx 0 rgba(0, 0, 0, 0.08));
}

.hero-title {
  display: block;
  font-size: $font-size-3xl;
  font-weight: $font-weight-extrabold;
  color: $text-color-inverse;
  letter-spacing: 2rpx;
  text-shadow: 0 6rpx 0 rgba(214, 119, 48, 0.45), 0 10rpx 24rpx rgba(0, 0, 0, 0.12);
}

.hero-sub {
  display: block;
  margin-top: $spacing-sm;
  font-size: $font-size-sm;
  color: $checkin-hero-muted;
}

.hero-deco {
  position: absolute;
  left: 0;
  right: 0;
  bottom: $spacing-base;
  height: 100rpx;
  pointer-events: none;
}

.deco {
  position: absolute;
  font-size: 44rpx;
  opacity: 0.95;
  animation: floaty 3s ease-in-out infinite;
}

.deco--a { left: 8%; bottom: 0; animation-delay: 0s; }
.deco--b { left: 28%; bottom: 20rpx; animation-delay: 0.4s; }
.deco--c { left: 50%; margin-left: -22rpx; bottom: 0; animation-delay: 0.2s; }
.deco--d { right: 28%; bottom: 18rpx; animation-delay: 0.6s; }
.deco--e { right: 8%; bottom: 4rpx; animation-delay: 0.3s; }

@keyframes floaty {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10rpx); }
}

.card {
  position: relative;
  margin-top: -72rpx;
  background: $bg-color-card;
  border-radius: $border-radius-2xl;
  border: $border-width-thick solid $checkin-card-border;
  padding: $spacing-2xl $spacing-lg $spacing-xl;
  box-sizing: border-box;
  box-shadow: $clay-shadow;
}

.ribbon {
  position: absolute;
  top: 0;
  left: $spacing-base;
  background: linear-gradient(135deg, $checkin-ribbon-bg 0%, $primary-color 100%);
  color: $text-color-inverse;
  padding: $spacing-xs $spacing-lg $spacing-sm;
  border-radius: 0 0 $border-radius-sm $border-radius-sm;
  box-shadow: 0 6rpx 12rpx rgba(0, 0, 0, 0.12);
}

.ribbon-text {
  font-size: $font-size-xs;
  font-weight: $font-weight-bold;
}

.streak-row {
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: $spacing-xs;
  margin-bottom: $spacing-lg;
  padding-top: $spacing-xs;
}

.streak-label {
  font-size: $font-size-base;
  color: $text-color-primary;
  font-weight: $font-weight-semibold;
}

.streak-num {
  font-size: 48rpx;
  font-weight: $font-weight-extrabold;
  color: $primary-color-dark;
}

.grid {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  gap: $spacing-xs;
  margin-bottom: $spacing-lg;
}

.grid-cell {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 0;
}

.cell-inner {
  width: 100%;
  aspect-ratio: 1;
  max-height: 88rpx;
  border-radius: $border-radius-lg;
  display: flex;
  align-items: center;
  justify-content: center;
  background: $checkin-cell-todo;
  border: $border-width-thick solid rgba(255, 154, 86, 0.35);
  box-shadow: $box-shadow-inner-sm;
  box-sizing: border-box;
  transition: all $transition-base;
}

.grid-cell--done .cell-inner {
  background: linear-gradient(135deg, $checkin-cell-done 0%, #FFE066 100%);
  border-color: rgba(255, 193, 7, 0.65);
  box-shadow: 
    0 4rpx 12rpx rgba(255, 193, 7, 0.3),
    inset 0 2rpx 4rpx rgba(255, 255, 255, 0.5);
}

.grid-cell--pop .cell-inner {
  animation: cellPop 0.55s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes cellPop {
  0% { transform: scale(1); }
  45% { transform: scale(1.15); }
  100% { transform: scale(1); }
}

.paw-mark {
  font-size: 36rpx;
  line-height: 1;
}

.reward-ico {
  font-size: 32rpx;
  line-height: 1;
  opacity: 0.92;
}

.day-label {
  margin-top: $spacing-xs;
  font-size: $font-size-2xs;
  color: $text-color-secondary;
}

.fortune-strip {
  background: linear-gradient(180deg, $primary-color-pale 0%, $bg-color-card 100%);
  border-radius: $border-radius-xl;
  padding: $spacing-base;
  margin-bottom: $spacing-lg;
  border: $border-width-thick solid $border-color;
}

.fortune-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: $spacing-sm;
}

.fortune-level {
  font-size: $font-size-xl;
  font-weight: $font-weight-extrabold;
  color: $primary-color-dark;
}

.fortune-level--best {
  color: #E65100;
}

.fortune-points {
  font-size: $font-size-sm;
  font-weight: $font-weight-bold;
  color: $primary-color-dark;
  background: linear-gradient(135deg, rgba(255, 213, 128, 0.55) 0%, rgba(255, 179, 128, 0.55) 100%);
  padding: $spacing-xs $spacing-sm;
  border-radius: $border-radius-full;
}

.fortune-points--muted {
  font-weight: $font-weight-semibold;
  color: $text-color-muted;
  background: $bg-color-gray;
}

.fortune-desc {
  font-size: $font-size-base;
  color: $text-color-secondary;
  line-height: $line-height-relaxed;
}

.cta {
  width: 100%;
  min-height: 104rpx;
  font-size: $font-size-lg;
  font-weight: $font-weight-bold;
  box-shadow: 0 10rpx 28rpx rgba(255, 140, 66, 0.35);
}
</style>
