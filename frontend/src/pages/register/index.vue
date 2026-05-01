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
        <text class="title-icon">✨</text>
        <text class="title">加入宠光</text>
        <text class="subtitle">创建您的宠物社区账号</text>
      </view>

      <view class="form-group">
        <PetInput 
          v-model="form.username" 
          placeholder="用户名（4-20位字母数字）" 
          clearable
        />
        <PetInput 
          v-model="form.nickname" 
          placeholder="昵称" 
          clearable
        />
        <PetInput 
          v-model="form.password" 
          type="password" 
          placeholder="密码" 
          clearable
        />
        <PetInput 
          v-model="confirmPassword" 
          type="password" 
          placeholder="确认密码" 
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
          注册
        </PetButton>
        <PetButton 
          class="btn" 
          type="text" 
          size="large"
          :disabled="locked" 
          @click="goLogin"
        >
          已有账号？去登录
        </PetButton>
      </view>
    </PetCard>
  </view>
</template>

<script setup>
import { reactive, ref } from "vue";
import { registerApi } from "../../api/auth";
import { useUserStore } from "../../stores/user";
import { useButtonLock } from "../../composables/useButtonLock";
import PetCard from "../../components/PetCard.vue";
import PetInput from "../../components/PetInput.vue";
import PetButton from "../../components/PetButton.vue";

const form = reactive({ username: "", nickname: "", password: "" });
const confirmPassword = ref("");
const userStore = useUserStore();
const { locked, run } = useButtonLock();

function goLogin() {
  uni.navigateBack();
}

function submit() {
  if (!form.username || !form.nickname || !form.password) {
    uni.showToast({ title: "请填写完整信息", icon: "none" });
    return;
  }
  if (form.password !== confirmPassword.value) {
    uni.showToast({ title: "两次密码不一致", icon: "none" });
    return;
  }
  run(async () => {
    const data = await registerApi(form);
    userStore.setLogin(data.token, data.user);
    uni.switchTab({ url: "/pages/index/index" });
  });
}
</script>

<style lang="scss" scoped>
.container {
  padding: $spacing-2xl $spacing-lg;
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

.deco--1 { top: 10%; left: 8%; animation-delay: 0s; }
.deco--2 { top: 20%; right: 12%; animation-delay: 1s; }
.deco--3 { bottom: 25%; left: 12%; animation-delay: 2s; }
.deco--4 { bottom: 15%; right: 8%; animation-delay: 0.5s; }

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
