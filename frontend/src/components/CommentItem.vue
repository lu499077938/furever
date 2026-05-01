<template>
  <view class="comment-item">
    <Avatar :src="comment.user_avatar" />
    <view class="comment-body">
      <view class="comment-header">
        <text class="user-name">{{ comment.user_nickname }}</text>
        <text v-if="comment.is_edited" class="edited-tag">已编辑</text>
      </view>
      <text class="comment-content">{{ comment.content }}</text>
      <view class="comment-footer">
        <text class="time">{{ formatTime(comment.created_at) }}</text>
        <view class="actions">
          <text v-if="canReply" class="action-btn" @click="handleReply">💬 回复</text>
          <text v-if="canEdit" class="action-btn" @click="handleEdit">✏️ 编辑</text>
          <text v-if="canDelete" class="action-btn delete" @click="handleDelete">🗑️ 删除</text>
          <text class="action-btn like" :class="{ active: comment.is_liked }" @click="handleLike">
            {{ comment.is_liked ? '❤️' : '🤍' }} {{ comment.like_count || '' }}
          </text>
        </view>
      </view>

      <view v-if="showReplyBox" class="reply-box">
        <CommentReply
          :reply-to="comment"
          @cancel="showReplyBox = false"
          @submit="handleReplySubmit"
        />
      </view>

      <view v-if="showEditBox" class="edit-box">
        <PetInput v-model="editContent" placeholder="编辑评论..." maxlength="500" />
        <view class="edit-actions">
          <PetButton size="small" @click="showEditBox = false">取消</PetButton>
          <PetButton size="small" type="primary" @click="handleEditSubmit" :disabled="!editContent.trim()">保存</PetButton>
        </view>
      </view>

      <view v-if="comment.replies && comment.replies.length > 0 && showReplies" class="replies">
        <CommentItem
          v-for="reply in comment.replies"
          :key="reply.id"
          :comment="reply"
          :post-id="postId"
          :level="level + 1"
          @reply="$emit('reply', $event)"
          @like="$emit('like', $event)"
          @delete="$emit('delete', $event)"
          @edit="$emit('edit', $event)"
        />
      </view>

      <text v-if="comment.reply_count > 0 && !showReplies" class="toggle-replies" @click="showReplies = true">
        🐾 查看 {{ comment.reply_count }} 条回复 ▼
      </text>
      <text v-if="comment.reply_count > 0 && showReplies" class="toggle-replies" @click="showReplies = false">
        收起回复 ▲
      </text>
    </view>
  </view>
</template>

<script setup>
import { ref, computed } from "vue";
import Avatar from "./Avatar.vue";
import PetButton from "./PetButton.vue";
import PetInput from "./PetInput.vue";
import CommentReply from "./CommentReply.vue";
import { formatTime } from "../utils/format";
import { useUserStore } from "../stores/user";

const props = defineProps({
  comment: { type: Object, required: true },
  postId: { type: Number, required: true },
  level: { type: Number, default: 1 },
});

const emit = defineEmits(["reply", "like", "delete", "edit"]);

const userStore = useUserStore();
const showReplies = ref(false);
const showReplyBox = ref(false);
const showEditBox = ref(false);
const editContent = ref("");

const canReply = computed(() => props.level < 3);
const canEdit = computed(() => props.comment.user_id === userStore.profile?.id);
const canDelete = computed(() => props.comment.user_id === userStore.profile?.id);

function handleReply() {
  showReplyBox.value = true;
}

function handleReplySubmit(content) {
  showReplyBox.value = false;
  emit("reply", { commentId: props.comment.id, content });
}

function handleEdit() {
  editContent.value = props.comment.content;
  showEditBox.value = true;
}

function handleEditSubmit() {
  if (!editContent.value.trim()) return;
  emit("edit", { commentId: props.comment.id, content: editContent.value });
  showEditBox.value = false;
}

function handleDelete() {
  uni.showModal({
    title: "删除评论",
    content: "确定要删除这条评论吗？",
    success: (res) => {
      if (res.confirm) {
        emit("delete", { commentId: props.comment.id });
      }
    },
  });
}

function handleLike() {
  emit("like", { commentId: props.comment.id });
}
</script>

<style lang="scss" scoped>
.comment-item {
  display: flex;
  gap: $spacing-base;
  padding: $spacing-base 0;
  border-bottom: $border-width-thin solid $border-color;
}

.comment-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: $spacing-xs;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: $spacing-xs;
}

.user-name {
  font-size: $font-size-base;
  font-weight: $font-weight-semibold;
  color: $text-color-primary;
}

.edited-tag {
  font-size: $font-size-2xs;
  color: $text-color-muted;
  background: $bg-color-gray;
  padding: 2rpx $spacing-xs;
  border-radius: $border-radius-sm;
}

.comment-content {
  font-size: $font-size-base;
  color: $text-color-primary;
  line-height: $line-height-relaxed;
}

.comment-footer {
  display: flex;
  align-items: center;
  gap: $spacing-base;
}

.time {
  font-size: $font-size-sm;
  color: $text-color-muted;
}

.actions {
  display: flex;
  align-items: center;
  gap: $spacing-base;
  margin-left: auto;
}

.action-btn {
  font-size: $font-size-sm;
  color: $text-color-muted;
  transition: all $transition-fast;

  &:active {
    transform: scale(0.95);
  }

  &.delete {
    color: $error-color;
  }

  &.like {
    display: flex;
    align-items: center;
    gap: 4rpx;

    &.active {
      color: $primary-color;
    }
  }
}

.reply-box,
.edit-box {
  margin-top: $spacing-sm;
  padding: $spacing-base;
  background: $bg-color-warm;
  border-radius: $border-radius-lg;
  border: $border-width-thick solid $border-color;
}

.edit-actions {
  display: flex;
  justify-content: flex-end;
  gap: $spacing-sm;
  margin-top: $spacing-sm;
}

.replies {
  margin-top: $spacing-sm;
  padding-left: $spacing-base;
  border-left: $border-width-thick solid $border-color;
}

.toggle-replies {
  margin-top: $spacing-sm;
  font-size: $font-size-sm;
  color: $primary-color;
  font-weight: $font-weight-medium;
}
</style>
