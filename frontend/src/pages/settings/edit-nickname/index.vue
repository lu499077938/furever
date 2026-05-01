<template>
  <view class="container">
    <PetCard class="form-card" radius="xl">
      <view class="field">
        <text class="field-label">✏️ 新昵称</text>
        <input
          v-model="nickname"
          class="field-input"
          placeholder="请输入新昵称"
          maxlength="20"
          :focus="true"
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
import { onLoad } from "@dcloudio/uni-app";
import PetCard from "../../../components/PetCard.vue";
import PetButton from "../../../components/PetButton.vue";
import { meApi, updateNicknameApi } from "../../../api/user";
import { useUserStore } from "../../../stores/user";

const userStore = useUserStore();
const nickname = ref("");
const saving = ref(false);

async function init() {
  try {
    const me = await meApi();
    nickname.value = me.nickname || "";
  } catch {
    // 静默失败，保持空值
  }
}

async function save() {
  const trimmed = nickname.value.trim();
  if (!trimmed) {
    uni.showToast({ title: "昵称不能为空", icon: "none" });
    return;
  }
  if (saving.value) return;
  saving.value = true;
  try {
    await updateNicknameApi({ nickname: trimmed });
    const me = await meApi();
    userStore.setProfile(me);
    uni.showToast({ title: "昵称已更新", icon: "success" });
    setTimeout(() => uni.navigateBack(), 1500);
  } catch (error) {
    const msg = error?.message || error?.errMsg || "保存失败，请重试";
    uni.showToast({ title: msg, icon: "none" });
  } finally {
    saving.value = false;
  }
}

onLoad(() => init());
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

.action-wrap {
  padding: 0 $spacing-base;
}
</style>
