<template>
  <view class="comment-reply">
    <text v-if="replyTo" class="reply-to">🐾 回复 @{{ replyTo.user_nickname }}：</text>
    <view class="reply-input-box">
      <PetInput v-model="content" placeholder="写评论..." maxlength="500" />
      <view class="reply-actions">
        <PetButton size="small" @click="$emit('cancel')">取消</PetButton>
        <PetButton size="small" type="primary" @click="handleSubmit" :disabled="!content.trim()">发送</PetButton>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref } from "vue";
import PetButton from "./PetButton.vue";
import PetInput from "./PetInput.vue";

const props = defineProps({
  replyTo: { type: Object, default: null },
});

const emit = defineEmits(["submit", "cancel"]);

const content = ref("");

function handleSubmit() {
  if (!content.value.trim()) return;
  emit("submit", content.value);
  content.value = "";
}
</script>

<style lang="scss" scoped>
.comment-reply {
  display: flex;
  flex-direction: column;
  gap: $spacing-xs;
}

.reply-to {
  font-size: $font-size-sm;
  color: $text-color-secondary;
  font-weight: $font-weight-medium;
}

.reply-input-box {
  display: flex;
  flex-direction: column;
  gap: $spacing-base;
}

.reply-actions {
  display: flex;
  justify-content: flex-end;
  gap: $spacing-base;
}
</style>
