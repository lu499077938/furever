<template>
  <PetCard :padding="false" :margin="false" class="post-card" @click="goDetail">
    <view class="cover-wrapper">
      <image class="cover" :src="post.cover_thumb_url" mode="aspectFill" />
      <view class="cover-overlay"></view>
    </view>
    <view class="content">
      <text class="title">{{ post.title }}</text>
      <view class="meta">
        <Avatar :src="post.author_avatar" size="small" />
        <text class="name">{{ post.author_nickname }}</text>
        <view class="likes">
          <text class="like-icon">♥</text>
          <text class="like-count">{{ post.like_count }}</text>
        </view>
      </view>
    </view>
  </PetCard>
</template>

<script setup>
import Avatar from "./Avatar.vue";
import PetCard from "./PetCard.vue";

const props = defineProps({
  post: { type: Object, required: true },
});

function goDetail() {
  uni.navigateTo({ url: `/pages/post-detail/index?id=${props.post.id}` });
}
</script>

<style lang="scss" scoped>
.post-card {
  margin: $spacing-xs;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.cover-wrapper {
  position: relative;
  width: 100%;
  height: 280rpx;
}

.cover {
  width: 100%;
  height: 100%;
  background-color: $bg-color-gray;
}

.cover-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 60rpx;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.1), transparent);
  pointer-events: none;
}

.content {
  padding: $spacing-base;
  display: flex;
  flex-direction: column;
  gap: $spacing-sm;
}

.title {
  font-size: $font-size-base;
  font-weight: $font-weight-semibold;
  color: $text-color-primary;
  line-height: $line-height-base;
  @include text-ellipsis(2);
}

.meta {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  margin-top: auto;
}

.name {
  flex: 1;
  color: $text-color-secondary;
  font-size: $font-size-sm;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.likes {
  display: flex;
  align-items: center;
  gap: 6rpx;
  padding: 6rpx 16rpx;
  background: linear-gradient(135deg, rgba($primary-color, 0.1) 0%, rgba($secondary-color, 0.1) 100%);
  border-radius: $border-radius-full;
}

.like-icon {
  font-size: 22rpx;
  color: $primary-color;
}

.like-count {
  font-size: $font-size-sm;
  color: $primary-color;
  font-weight: $font-weight-medium;
}
</style>
