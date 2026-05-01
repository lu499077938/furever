<template>
  <view class="container">
    <PetCard class="user-card" radius="2xl">
      <view class="avatar-wrap" @click="onAvatarClick">
        <Avatar :src="user?.avatar" size="large" />
        <view class="avatar-mask">
          <text class="avatar-mask-text">{{ isAvatarUpdating ? "上传中" : "📷" }}</text>
        </view>
      </view>
      <view class="user-meta">
        <text class="name">{{ user?.nickname || "未登录" }}</text>
        <text class="sub">{{ user?.username || "请先登录" }}</text>
      </view>
    </PetCard>

    <PetCard class="points-card" radius="xl" @click="go('/pages/points/index')">
      <view class="points-content">
        <view class="points-info">
          <text class="points-label">我的积分</text>
          <text class="points-hint">点击查看明细 ›</text>
        </view>
        <PointsBadge :points="pointsStore.totalPoints" size="large" />
      </view>
    </PetCard>

    <PetCard class="menu-card" radius="xl" :padding="false">
      <view class="menu-item" @click="go('/pages/messages/index')">
        <text class="menu-icon">💬</text>
        <text class="menu-label">消息</text>
        <text v-if="unreadCount > 0" class="menu-badge">{{ unreadCount }}</text>
        <text class="menu-arrow">›</text>
      </view>
      <view class="menu-item" @click="go('/pages/my-posts/index')">
        <text class="menu-icon">📝</text>
        <text class="menu-label">我的发布</text>
        <text class="menu-arrow">›</text>
      </view>
      <view class="menu-item" @click="go('/pages/my-collects/index')">
        <text class="menu-icon">⭐</text>
        <text class="menu-label">我的收藏</text>
        <text class="menu-arrow">›</text>
      </view>
      <view class="menu-item" @click="go('/pages/my-likes/index')">
        <text class="menu-icon">❤️</text>
        <text class="menu-label">赞过</text>
        <text class="menu-arrow">›</text>
      </view>
      <view class="menu-item menu-item--last" @click="go('/pages/settings/index')">
        <text class="menu-icon">⚙️</text>
        <text class="menu-label">设置</text>
        <text class="menu-arrow">›</text>
      </view>
    </PetCard>
  </view>
</template>

<script setup>
import { computed, ref } from "vue";
import { onShow } from "@dcloudio/uni-app";
import Avatar from "../../components/Avatar.vue";
import PointsBadge from "../../components/PointsBadge.vue";
import PetCard from "../../components/PetCard.vue";
import { useButtonLock } from "../../composables/useButtonLock";
import { useUserStore } from "../../stores/user";
import { usePointsStore } from "../../stores/points";
import { meApi, updateAvatarApi } from "../../api/user";
import { pointsOverviewApi } from "../../api/points";
import { unreadCountApi } from "../../api/notification";
import { uploadImageApi } from "../../api/upload";

const userStore = useUserStore();
const pointsStore = usePointsStore();
const unreadCount = ref(0);
const user = computed(() => userStore.profile);
const { locked: isAvatarUpdating, run: runAvatarUpdate } = useButtonLock();

function go(url) {
  uni.navigateTo({ url });
}

async function refresh() {
  if (!userStore.token) {
    uni.navigateTo({ url: "/pages/login/index" });
    return;
  }
  const [me, points, unread] = await Promise.all([meApi(), pointsOverviewApi(), unreadCountApi()]);
  userStore.setProfile(me);
  pointsStore.setTotalPoints(points.total_points);
  unreadCount.value = unread.unread_count || 0;
}

function isChooseImageCanceled(error) {
  const rawMessage = error?.errMsg || error?.message || "";
  return rawMessage.toLowerCase().includes("cancel");
}

function resolveErrorMessage(error, fallbackText) {
  if (!error) return fallbackText;
  if (typeof error === "string") return error;
  return error.message || error.errMsg || fallbackText;
}

function chooseAvatarImage() {
  return new Promise((resolve, reject) => {
    uni.chooseImage({
      count: 1,
      sourceType: ["album", "camera"],
      success: resolve,
      fail: reject,
    });
  });
}

async function onAvatarClick() {
  if (isAvatarUpdating.value) return;
  let chooseResult;
  try {
    chooseResult = await chooseAvatarImage();
  } catch (error) {
    if (isChooseImageCanceled(error)) return;
    const message = resolveErrorMessage(error, "选择图片失败");
    uni.showToast({ title: message, icon: "none" });
    return;
  }

  const filePath = chooseResult?.tempFilePaths?.[0];
  if (!filePath) return;

  try {
    await runAvatarUpdate(async () => {
      const uploadResult = await uploadImageApi(filePath);
      const avatarUrl = uploadResult?.url;
      if (!avatarUrl) {
        throw new Error("上传失败，请重试");
      }
      await updateAvatarApi(avatarUrl);
      if (userStore.profile) {
        userStore.setProfile({ ...userStore.profile, avatar: avatarUrl });
      }
      uni.showToast({ title: "头像更新成功", icon: "success" });
    });
  } catch (error) {
    const message = resolveErrorMessage(error, "头像更新失败");
    uni.showToast({ title: message, icon: "none" });
  }
}

onShow(() => {
  refresh();
});
</script>

<style lang="scss" scoped>
.container {
  padding: $spacing-base;
  display: flex;
  flex-direction: column;
  gap: $spacing-base;
}

.user-card {
  display: flex;
  gap: $spacing-base;
  align-items: center;
}

.avatar-wrap {
  position: relative;
}

.avatar-mask {
  position: absolute;
  right: 0;
  bottom: 0;
  width: 44rpx;
  height: 44rpx;
  border-radius: 50%;
  background: linear-gradient(135deg, $primary-color 0%, $secondary-color 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: $box-shadow-sm;
}

.avatar-mask-text {
  color: $text-color-inverse;
  font-size: $font-size-2xs;
  line-height: 1;
}

.user-meta {
  display: flex;
  flex-direction: column;
  gap: $spacing-xs;
}

.name {
  font-size: $font-size-xl;
  font-weight: $font-weight-bold;
  color: $text-color-primary;
}

.sub {
  font-size: $font-size-sm;
  color: $text-color-secondary;
}

.points-card {
  cursor: pointer;
}

.points-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.points-info {
  display: flex;
  flex-direction: column;
  gap: $spacing-xs;
}

.points-label {
  font-size: $font-size-base;
  font-weight: $font-weight-semibold;
  color: $text-color-primary;
}

.points-hint {
  font-size: $font-size-sm;
  color: $text-color-muted;
}

.menu-card {
  overflow: hidden;
}

.menu-item {
  display: flex;
  align-items: center;
  padding: $spacing-lg $spacing-base;
  border-bottom: $border-width-thin solid $border-color;
  transition: all $transition-fast;

  &:active {
    background: $bg-color-gray;
  }

  &--last {
    border-bottom: none;
  }
}

.menu-icon {
  font-size: 36rpx;
  margin-right: $spacing-base;
}

.menu-label {
  flex: 1;
  font-size: $font-size-base;
  color: $text-color-primary;
  font-weight: $font-weight-medium;
}

.menu-badge {
  padding: $spacing-xs $spacing-sm;
  background: linear-gradient(135deg, $primary-color 0%, $secondary-color 100%);
  color: $text-color-inverse;
  font-size: $font-size-xs;
  font-weight: $font-weight-bold;
  border-radius: $border-radius-full;
  margin-right: $spacing-sm;
}

.menu-arrow {
  font-size: $font-size-xl;
  color: $text-color-muted;
}
</style>
