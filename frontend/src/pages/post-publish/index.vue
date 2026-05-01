<template>
  <view class="container">
    <PetCard class="form-card" radius="xl">
      <view class="image-uploader">
        <view class="image-list">
          <view 
            v-for="(img, idx) in previewImages" 
            :key="idx" 
            class="image-item"
          >
            <image :src="img" class="thumb" mode="aspectFill" />
            <view class="delete-btn" @click.stop="removeImage(idx)">
              <text>✕</text>
            </view>
          </view>
          
          <view 
            v-if="previewImages.length < 9" 
            class="upload-btn" 
            @click="chooseImages"
          >
            <text class="plus-icon">📷</text>
            <text class="upload-text">选图</text>
          </view>
        </view>
        <text class="image-tip">🐾 最多可上传 9 张图片</text>
      </view>

      <view class="text-inputs">
        <PetInput 
          v-model="title" 
          placeholder="输入标题（1-50字）" 
          :maxlength="50"
        />
        
        <view class="textarea-wrapper" :class="{ 'is-focused': isTextareaFocused }">
          <textarea 
            v-model="content" 
            class="pet-textarea"
            placeholder="分享今天和毛孩子的故事吧..." 
            placeholder-class="pet-placeholder"
            :maxlength="1000"
            @focus="isTextareaFocused = true"
            @blur="isTextareaFocused = false"
          />
        </view>
      </view>

      <view class="action-group">
        <PetButton 
          class="submit-btn" 
          type="primary" 
          :loading="locked" 
          :disabled="locked" 
          @click="submit"
        >
          🐾 发布
        </PetButton>
      </view>
    </PetCard>
  </view>
</template>

<script setup>
import { ref } from "vue";
import { uploadImageApi } from "../../api/upload";
import { createPostApi } from "../../api/post";
import { createClientId } from "../../utils/uuid";
import { useButtonLock } from "../../composables/useButtonLock";
import PetCard from "../../components/PetCard.vue";
import PetInput from "../../components/PetInput.vue";
import PetButton from "../../components/PetButton.vue";

const title = ref("");
const content = ref("");
const images = ref([]);
const previewImages = ref([]);
const thumbImages = ref([]);
const { locked, run } = useButtonLock();

const isTextareaFocused = ref(false);

function chooseImages() {
  uni.chooseImage({
    count: 9 - previewImages.value.length,
    success: async (res) => {
      const files = res.tempFilePaths || [];
      for (const path of files) {
        const uploaded = await uploadImageApi(path);
        images.value.push(uploaded.url);
        thumbImages.value.push(uploaded.thumb_url);
        previewImages.value.push(uploaded.thumb_url);
      }
    },
  });
}

function removeImage(index) {
  images.value.splice(index, 1);
  thumbImages.value.splice(index, 1);
  previewImages.value.splice(index, 1);
}

function submit() {
  run(async () => {
    if (!title.value || !content.value || images.value.length === 0) {
      uni.showToast({ title: "请填写完整内容并上传图片", icon: "none" });
      return;
    }
    await createPostApi({
      title: title.value,
      content: content.value,
      images: images.value,
      thumb_images: thumbImages.value,
      client_id: createClientId(),
    });
    uni.showToast({ title: "发布成功", icon: "success" });
    setTimeout(() => {
      uni.switchTab({ url: "/pages/index/index" });
    }, 1000);
  });
}
</script>

<style lang="scss" scoped>
.container {
  padding: $spacing-base;
  min-height: 100vh;
}

.form-card {
  padding: $spacing-lg;
  display: flex;
  flex-direction: column;
  gap: $spacing-xl;
}

.image-uploader {
  display: flex;
  flex-direction: column;
  gap: $spacing-sm;
}

.image-list {
  display: flex;
  flex-wrap: wrap;
  gap: $spacing-base;
}

.image-item {
  position: relative;
  width: 200rpx;
  height: 200rpx;
  border-radius: $border-radius-lg;
  overflow: hidden;
  box-shadow: $box-shadow-sm;
  border: $border-width-thick solid $border-color;
}

.thumb {
  width: 100%;
  height: 100%;
}

.delete-btn {
  position: absolute;
  top: 8rpx;
  right: 8rpx;
  width: 44rpx;
  height: 44rpx;
  background: linear-gradient(135deg, rgba(0, 0, 0, 0.6) 0%, rgba(0, 0, 0, 0.4) 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  
  text {
    color: $text-color-inverse;
    font-size: $font-size-sm;
  }
}

.upload-btn {
  width: 200rpx;
  height: 200rpx;
  background: $bg-color-warm;
  border-radius: $border-radius-lg;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: $border-width-thick dashed $border-color;
  transition: all $transition-base;
  
  &:active {
    background: $bg-color-gray;
    transform: scale(0.98);
  }

  .plus-icon {
    font-size: 48rpx;
    margin-bottom: $spacing-xs;
  }

  .upload-text {
    font-size: $font-size-sm;
    color: $text-color-secondary;
    font-weight: $font-weight-medium;
  }
}

.image-tip {
  font-size: $font-size-xs;
  color: $text-color-muted;
  padding-left: $spacing-xs;
}

.text-inputs {
  display: flex;
  flex-direction: column;
  gap: $spacing-base;
}

.textarea-wrapper {
  background: $bg-color-gray;
  border-radius: $border-radius-lg;
  padding: $spacing-base;
  border: $border-width-thick solid transparent;
  transition: all $transition-base;

  &.is-focused {
    background: $bg-color-card;
    border-color: $primary-color;
    box-shadow: 0 0 0 6rpx rgba($primary-color, 0.1);
  }
}

.pet-textarea {
  width: 100%;
  min-height: 240rpx;
  font-size: $font-size-base;
  color: $text-color-primary;
  line-height: $line-height-relaxed;
}

.pet-placeholder {
  color: $text-color-placeholder;
}

.action-group {
  display: flex;
  justify-content: center;
}

.submit-btn {
  min-width: 320rpx;
  font-size: $font-size-lg;
  font-weight: $font-weight-bold;
  box-shadow: 0 10rpx 28rpx rgba(255, 140, 66, 0.35);
}
</style>
