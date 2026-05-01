<template>
  <view class="container">
    <view v-for="item in list" :key="item.id" class="message-card" @click="goDetail(item.related_id)">
      <view class="message-icon">
        <text>{{ getMessageIcon(item.type) }}</text>
      </view>
      <view class="message-content">
        <text class="message-text">{{ item.content }}</text>
        <view class="message-meta">
          <text class="message-time">{{ formatTime(item.created_at) }}</text>
          <text v-if="!item.is_read" class="unread-badge">新</text>
        </view>
      </view>
    </view>
    <Loading v-if="loading" />
    <Empty v-else-if="list.length === 0" text="暂无消息 📭" />
  </view>
</template>

<script setup>
import { ref } from "vue";
import { onLoad } from "@dcloudio/uni-app";
import Loading from "../../components/Loading.vue";
import Empty from "../../components/Empty.vue";
import { notificationsApi, readAllApi } from "../../api/notification";
import { formatTime } from "../../utils/format";

const list = ref([]);
const loading = ref(false);

async function load() {
  loading.value = true;
  try {
    await readAllApi();
    const data = await notificationsApi({ page: 1, page_size: 50 });
    list.value = data.items || [];
  } finally {
    loading.value = false;
  }
}

function goDetail(postId) {
  uni.navigateTo({ url: `/pages/post-detail/index?id=${postId}` });
}

function getMessageIcon(type) {
  const icons = {
    comment: "💬",
    like: "❤️",
    follow: "👥",
    system: "🔔",
  };
  return icons[type] || "🔔";
}

onLoad(() => load());
</script>

<style lang="scss" scoped>
.container {
  padding: $spacing-base;
  display: flex;
  flex-direction: column;
  gap: $spacing-base;
}

.message-card {
  display: flex;
  gap: $spacing-base;
  padding: $spacing-base;
  background: $bg-color-card;
  border-radius: $border-radius-xl;
  border: $border-width-thick solid $border-color;
  box-shadow: $box-shadow-sm;
  transition: all $transition-fast;

  &:active {
    transform: scale(0.98);
    background: $bg-color-gray;
  }
}

.message-icon {
  width: 80rpx;
  height: 80rpx;
  border-radius: $border-radius-lg;
  background: $bg-color-warm;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 36rpx;
  flex-shrink: 0;
}

.message-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: $spacing-xs;
  min-width: 0;
}

.message-text {
  font-size: $font-size-base;
  color: $text-color-primary;
  line-height: $line-height-relaxed;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.message-meta {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
}

.message-time {
  font-size: $font-size-sm;
  color: $text-color-muted;
}

.unread-badge {
  padding: 2rpx $spacing-sm;
  background: linear-gradient(135deg, $primary-color 0%, $secondary-color 100%);
  color: $text-color-inverse;
  font-size: $font-size-2xs;
  font-weight: $font-weight-bold;
  border-radius: $border-radius-full;
}
</style>
