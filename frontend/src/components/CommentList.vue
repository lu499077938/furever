<template>
  <view class="comment-list">
    <view v-for="comment in comments" :key="comment.id">
      <CommentItem
        :comment="comment"
        :post-id="postId"
        @reply="handleCommentReply"
        @like="handleCommentLike"
        @delete="handleCommentDelete"
        @edit="handleCommentEdit"
      />
    </view>
    <Empty v-if="comments.length === 0" text="还没有评论，快来抢沙发 🐱" />
  </view>
</template>

<script setup>
import CommentItem from "./CommentItem.vue";
import Empty from "./Empty.vue";

const props = defineProps({
  comments: { type: Array, required: true },
  postId: { type: Number, required: true },
});

const emit = defineEmits(["reply", "like", "delete", "edit"]);

function handleCommentReply(data) {
  emit("reply", data);
}

function handleCommentLike(data) {
  emit("like", data);
}

function handleCommentDelete(data) {
  emit("delete", data);
}

function handleCommentEdit(data) {
  emit("edit", data);
}
</script>

<style lang="scss" scoped>
.comment-list {
  display: flex;
  flex-direction: column;
}
</style>
