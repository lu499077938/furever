<template>
  <view class="container">
    <PetCard class="overview-card" radius="xl">
      <view class="overview-header">
        <text class="overview-title">🐾 我的积分</text>
      </view>
      <view class="points-display">
        <text class="points-num">{{ overview.total_points || 0 }}</text>
        <text class="points-unit">积分</text>
      </view>
      <view class="streak-info">
        <text class="streak-icon">🔥</text>
        <text class="streak-text">连续签到 {{ overview.streak_days || 0 }} 天</text>
      </view>
      <PetButton class="exchange-btn" type="secondary" disabled @click="soon">
        🎁 兑换（即将上线）
      </PetButton>
    </PetCard>

    <PetCard class="logs-card" radius="xl">
      <text class="section-title">积分明细</text>
      <view class="log-list">
        <view v-for="item in logs" :key="item.created_at + item.source" class="log-item">
          <view class="log-info">
            <text class="log-icon">{{ getLogIcon(item.source) }}</text>
            <text class="log-remark">{{ item.remark || item.source }}</text>
          </view>
          <text class="log-amount">+{{ item.amount }}</text>
        </view>
      </view>
      <Loading v-if="loading" />
      <Empty v-else-if="logs.length === 0" text="暂无积分明细 📝" />
    </PetCard>
  </view>
</template>

<script setup>
import { ref } from "vue";
import { onLoad, onReachBottom } from "@dcloudio/uni-app";
import Loading from "../../components/Loading.vue";
import Empty from "../../components/Empty.vue";
import PetCard from "../../components/PetCard.vue";
import PetButton from "../../components/PetButton.vue";
import { pointsOverviewApi, pointsLogsApi } from "../../api/points";

const overview = ref({});
const logs = ref([]);
const page = ref(1);
const total = ref(0);
const loading = ref(false);

async function loadOverview() {
  overview.value = await pointsOverviewApi();
}

async function loadLogs(reset = false) {
  if (loading.value) return;
  if (!reset && total.value > 0 && logs.value.length >= total.value) return;
  loading.value = true;
  if (reset) {
    logs.value = [];
    page.value = 1;
  }
  try {
    const data = await pointsLogsApi({ page: page.value, page_size: 20 });
    total.value = data.total || 0;
    logs.value = logs.value.concat(data.items || []);
    page.value += 1;
  } finally {
    loading.value = false;
  }
}

function soon() {
  uni.showToast({ title: "兑换功能即将上线，敬请期待~", icon: "none" });
}

function getLogIcon(source) {
  const icons = {
    checkin: "📅",
    post: "📝",
    comment: "💬",
    like: "❤️",
  };
  return icons[source] || "⭐";
}

onLoad(() => {
  loadOverview();
  loadLogs(true);
});
onReachBottom(() => loadLogs(false));
</script>

<style lang="scss" scoped>
.container {
  padding: $spacing-base;
  display: flex;
  flex-direction: column;
  gap: $spacing-base;
}

.overview-card {
  text-align: center;
  padding: $spacing-xl $spacing-lg;
}

.overview-header {
  margin-bottom: $spacing-base;
}

.overview-title {
  font-size: $font-size-base;
  color: $text-color-secondary;
  font-weight: $font-weight-medium;
}

.points-display {
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: $spacing-xs;
  margin-bottom: $spacing-base;
}

.points-num {
  font-size: 72rpx;
  font-weight: $font-weight-extrabold;
  color: $primary-color-dark;
  line-height: 1;
}

.points-unit {
  font-size: $font-size-base;
  color: $text-color-secondary;
}

.streak-info {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: $spacing-xs;
  margin-bottom: $spacing-lg;
}

.streak-icon {
  font-size: 28rpx;
}

.streak-text {
  font-size: $font-size-sm;
  color: $text-color-secondary;
}

.exchange-btn {
  width: 100%;
}

.logs-card {
  padding: $spacing-lg;
}

.section-title {
  display: block;
  font-size: $font-size-lg;
  font-weight: $font-weight-semibold;
  color: $text-color-primary;
  margin-bottom: $spacing-base;
}

.log-list {
  display: flex;
  flex-direction: column;
}

.log-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: $spacing-base 0;
  border-bottom: $border-width-thin solid $border-color;

  &:last-child {
    border-bottom: none;
  }
}

.log-info {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
}

.log-icon {
  font-size: 28rpx;
}

.log-remark {
  font-size: $font-size-base;
  color: $text-color-primary;
}

.log-amount {
  font-size: $font-size-base;
  font-weight: $font-weight-bold;
  color: $primary-color-dark;
}
</style>
