<template>
  <view class="container">
    <view class="decoration">
      <text class="deco deco--1">🐾</text>
      <text class="deco deco--2">🐱</text>
      <text class="deco deco--3">🐶</text>
      <text class="deco deco--4">🐾</text>
    </view>
    
    <PetCard class="form-card" radius="2xl">
      <view class="header">
        <text class="title-icon">🐾</text>
        <text class="title">欢迎来到宠光</text>
        <text class="subtitle">记录与毛孩子的每一刻温暖</text>
      </view>

      <view class="form-group">
        <PetInput 
          v-model="form.username" 
          placeholder="请输入用户名" 
          clearable
        />
        <PetInput 
          v-model="form.password" 
          type="password" 
          placeholder="请输入密码" 
          clearable
        />
      </view>

      <view class="action-group">
        <PetButton 
          class="btn" 
          type="primary" 
          size="large"
          :loading="locked" 
          :disabled="locked" 
          @click="submit"
        >
          登录
        </PetButton>
        <PetButton 
          class="btn" 
          type="outline" 
          size="large"
          :disabled="locked" 
          @click="goRegister"
        >
          注册新账号
        </PetButton>
      </view>
    </PetCard>
  </view>
</template>

<script setup>
import { reactive, ref } from "vue";
import { onLoad } from "@dcloudio/uni-app";
import { loginApi } from "../../api/auth";
import { useUserStore } from "../../stores/user";
import { useButtonLock } from "../../composables/useButtonLock";
import { meApi } from "../../api/user";
import PetCard from "../../components/PetCard.vue";
import PetInput from "../../components/PetInput.vue";
import PetButton from "../../components/PetButton.vue";

const form = reactive({ username: "", password: "" });
const userStore = useUserStore();
const { locked, run } = useButtonLock();
const redirectUrl = ref("");

onLoad((options) => {
  if (options.redirect) {
    redirectUrl.value = decodeURIComponent(options.redirect);
  }
});

function goRegister() {
  uni.navigateTo({ url: "/pages/register/index" });
}

function submit() {
  if (!form.username || !form.password) {
    uni.showToast({ title: "请输入用户名和密码", icon: "none" });
    return;
  }
  run(async () => {
    const data = await loginApi(form);
    userStore.setLogin(data.token, data.user);
    const me = await meApi();
    userStore.setProfile(me);
    
    if (redirectUrl.value) {
      uni.redirectTo({ url: redirectUrl.value });
    } else {
      uni.switchTab({ url: "/pages/index/index" });
    }
  });
}
</script>

<style lang="scss" scoped>
.container {
  padding: $spacing-3xl $spacing-lg;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.decoration {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.deco {
  position: absolute;
  font-size: 48rpx;
  opacity: 0.15;
  animation: float 4s ease-in-out infinite;
}

.deco--1 { top: 15%; left: 10%; animation-delay: 0s; }
.deco--2 { top: 25%; right: 15%; animation-delay: 1s; }
.deco--3 { bottom: 20%; left: 15%; animation-delay: 2s; }
.deco--4 { bottom: 30%; right: 10%; animation-delay: 0.5s; }

@keyframes float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-20rpx) rotate(5deg); }
}

.form-card {
  padding: $spacing-2xl $spacing-xl;
  position: relative;
  z-index: 1;
}

.header {
  margin-bottom: $spacing-2xl;
  text-align: center;

  .title-icon {
    display: block;
    font-size: 64rpx;
    margin-bottom: $spacing-base;
  }

  .title {
    display: block;
    font-size: $font-size-2xl;
    font-weight: $font-weight-bold;
    color: $primary-color;
    margin-bottom: $spacing-sm;
  }

  .subtitle {
    font-size: $font-size-base;
    color: $text-color-secondary;
  }
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: $spacing-base;
  margin-bottom: $spacing-2xl;
}

.action-group {
  display: flex;
  flex-direction: column;
  gap: $spacing-base;
  
  .btn {
    width: 100%;
  }
}
</style>
