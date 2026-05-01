<template>
  <view class="container">
    <PetCard class="form-card" radius="xl">
      <view class="field">
        <text class="field-label">🔐 旧密码</text>
        <input
          v-model="oldPassword"
          class="field-input"
          type="password"
          placeholder="请输入当前密码"
        />
      </view>
      <view class="divider" />
      <view class="field">
        <text class="field-label">🔑 新密码</text>
        <input
          v-model="newPassword"
          class="field-input"
          type="password"
          placeholder="请输入新密码（至少6位）"
        />
      </view>
      <view class="divider" />
      <view class="field">
        <text class="field-label">🔑 确认新密码</text>
        <input
          v-model="confirmPassword"
          class="field-input"
          type="password"
          placeholder="再次输入新密码"
        />
      </view>
    </PetCard>

    <view class="action-wrap">
      <PetButton type="primary" block :loading="saving" :disabled="saving" @click="save">
        保存
      </PetButton>
    </view>
  </view>
</template>

<script setup>
import { ref } from "vue";
import PetCard from "../../../components/PetCard.vue";
import PetButton from "../../../components/PetButton.vue";
import { updatePasswordApi } from "../../../api/user";
import { useUserStore } from "../../../stores/user";

const userStore = useUserStore();
const oldPassword = ref("");
const newPassword = ref("");
const confirmPassword = ref("");
const saving = ref(false);

async function save() {
  if (!oldPassword.value) {
    uni.showToast({ title: "请输入旧密码", icon: "none" });
    return;
  }
  if (!newPassword.value || newPassword.value.length < 6) {
    uni.showToast({ title: "新密码至少6位", icon: "none" });
    return;
  }
  if (newPassword.value !== confirmPassword.value) {
    uni.showToast({ title: "两次密码不一致", icon: "none" });
    return;
  }
  if (saving.value) return;
  saving.value = true;
  try {
    const data = await updatePasswordApi({
      old_password: oldPassword.value,
      new_password: newPassword.value,
    });
    userStore.setLogin(data.token, userStore.profile);
    uni.showToast({ title: "密码已更新", icon: "success" });
    setTimeout(() => uni.navigateBack(), 1500);
  } catch (error) {
    const msg = error?.message || error?.errMsg || "保存失败，请重试";
    uni.showToast({ title: msg, icon: "none" });
  } finally {
    saving.value = false;
  }
}
</script>

<style lang="scss" scoped>
.container {
  padding: $spacing-base;
  display: flex;
  flex-direction: column;
  gap: $spacing-lg;
}

.form-card {
  padding: $spacing-lg;
}

.field {
  display: flex;
  flex-direction: column;
  gap: $spacing-sm;
}

.field-label {
  font-size: $font-size-base;
  font-weight: $font-weight-semibold;
  color: $text-color-primary;
}

.field-input {
  background: $bg-color-gray;
  border-radius: $border-radius-lg;
  padding: $spacing-base;
  font-size: $font-size-base;
  color: $text-color-primary;
  border: $border-width-thick solid $border-color;
  transition: all $transition-base;

  &:focus {
    border-color: $primary-color;
    box-shadow: 0 0 0 6rpx rgba($primary-color, 0.1);
  }
}

.divider {
  height: $border-width-thin;
  background: $border-color;
  margin: $spacing-base 0;
}

.action-wrap {
  padding: 0 $spacing-base;
}
</style>
