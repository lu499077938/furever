<template>
  <view class="container">
    <PetCard class="menu-card" radius="xl" :padding="false">
      <view class="menu-item" @click="go('/pages/settings/edit-nickname/index')">
        <text class="menu-icon">✏️</text>
        <text class="menu-label">修改昵称</text>
        <text class="menu-arrow">›</text>
      </view>
      <view class="menu-item menu-item--last" @click="go('/pages/settings/edit-password/index')">
        <text class="menu-icon">🔐</text>
        <text class="menu-label">修改密码</text>
        <text class="menu-arrow">›</text>
      </view>
    </PetCard>

    <view class="logout-wrap">
      <PetButton type="danger" block @click="logout">🚪 退出登录</PetButton>
    </view>
  </view>
</template>

<script setup>
import PetCard from "../../components/PetCard.vue";
import PetButton from "../../components/PetButton.vue";
import { useUserStore } from "../../stores/user";

const userStore = useUserStore();

function go(url) {
  uni.navigateTo({ url });
}

function logout() {
  uni.showModal({
    title: "退出登录",
    content: "确定要退出登录吗？",
    confirmColor: "#ff4d4f",
    success(res) {
      if (res.confirm) {
        userStore.logout();
        uni.reLaunch({ url: "/pages/login/index" });
      }
    },
  });
}
</script>

<style lang="scss" scoped>
.container {
  padding: $spacing-base;
  display: flex;
  flex-direction: column;
  gap: $spacing-lg;
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

.menu-arrow {
  font-size: $font-size-xl;
  color: $text-color-muted;
}

.logout-wrap {
  padding: $spacing-base 0;
}
</style>
