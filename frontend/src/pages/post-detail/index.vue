<template>
  <view v-if="detail.id" class="container">
    <view class="top-author-bar">
      <Avatar :src="detail.author_avatar" />
      <view class="author-info">
        <text class="author-name">{{ detail.author_nickname }}</text>
      </view>
      <button 
        v-if="detail.author_id !== userStore.profile?.id"
        size="mini" 
        :class="['follow-btn', detail.is_followed ? 'followed' : '']" 
        @click="toggleFollow"
      >
        {{ detail.is_followed ? '已关注' : '关注' }}
      </button>
    </view>

    <swiper class="swiper" indicator-dots circular>
      <swiper-item v-for="(img, idx) in detail.images" :key="idx">
        <image :src="img" mode="aspectFill" class="cover" />
      </swiper-item>
    </swiper>

    <PetCard class="detail-card" radius="xl">
      <text class="title">{{ detail.title }}</text>
      <text class="content">{{ detail.content }}</text>
      <text class="publish-time">{{ formatTime(detail.created_at) }}</text>
    </PetCard>

    <PetCard class="comments-card" radius="xl">
      <text class="section-title">评论 ({{ detail.comment_count || 0 }})</text>
      <CommentList 
        :comments="commentList" 
        :post-id="postId"
        @reply="handleCommentReply"
        @like="handleCommentLike"
        @delete="handleCommentDelete"
        @edit="handleCommentEdit"
      />
    </PetCard>
  </view>

  <view class="bottom-bar">
    <view class="action-btn" :class="{ active: detail.is_liked }" @click="toggleLike">
      <text class="action-icon">{{ detail.is_liked ? '❤️' : '🤍' }}</text>
      <text class="action-text">{{ detail.like_count || 0 }}</text>
    </view>
    <view class="action-btn" :class="{ active: detail.is_collected }" @click="toggleCollect">
      <text class="action-icon">{{ detail.is_collected ? '⭐' : '☆' }}</text>
      <text class="action-text">{{ detail.collect_count || 0 }}</text>
    </view>
    <view class="action-btn" @click="handleShare">
      <text class="action-icon">📤</text>
      <text class="action-text">分享</text>
    </view>
    <view class="comment-input-wrap">
      <input v-model="comment" placeholder="写评论..." class="comment-input" />
      <PetButton size="small" :disabled="locked" @click="sendComment">发送</PetButton>
    </view>
  </view>

  <canvas canvas-id="posterCanvas" class="poster-canvas" />

  <view v-if="showPosterModal" class="poster-overlay" @click.self="() => { showPosterModal = false; posterPath = ''; }">
    <view class="poster-modal">
      <image :src="posterPath" mode="aspectFit" class="poster-preview" />
      <view class="poster-actions">
        <PetButton size="medium" @click="savePoster">保存到相册</PetButton>
        <PetButton size="medium" type="outline" @click="() => { showPosterModal = false; posterPath = ''; }">取消</PetButton>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, getCurrentInstance } from "vue";
import { onLoad, onShareAppMessage, onShareTimeline } from "@dcloudio/uni-app";
import Avatar from "../../components/Avatar.vue";
import Empty from "../../components/Empty.vue";
import PetCard from "../../components/PetCard.vue";
import PetButton from "../../components/PetButton.vue";
import CommentList from "../../components/CommentList.vue";
import { postDetailApi } from "../../api/post";
import { 
  listCommentsApi, 
  createCommentApi, 
  replyCommentApi, 
  updateCommentApi, 
  deleteCommentApi,
  toggleCommentLikeApi
} from "../../api/comment";
import { toggleCollectApi, toggleLikeApi } from "../../api/interaction";
import { toggleFollowApi } from "../../api/follow";
import { createClientId } from "../../utils/uuid";
import { formatTime } from "../../utils/format";
import { useButtonLock } from "../../composables/useButtonLock";
import { useUserStore } from "../../stores/user";

const postId = ref(0);
const detail = ref({});
const comment = ref("");
const commentList = ref([]);
const { locked, run } = useButtonLock();
const userStore = useUserStore();
const posterPath = ref('');
const showPosterModal = ref(false);
const instance = getCurrentInstance();

async function loadDetail() {
  detail.value = await postDetailApi(postId.value);
}

async function loadComments() {
  const data = await listCommentsApi(postId.value, { page: 1, page_size: 50, load_replies: true });
  commentList.value = data.items || [];
}

function toggleLike() {
  run(async () => {
    const data = await toggleLikeApi(postId.value);
    detail.value.is_liked = data.active;
    detail.value.like_count = data.count;
  });
}

function toggleCollect() {
  run(async () => {
    const data = await toggleCollectApi(postId.value);
    detail.value.is_collected = data.active;
    detail.value.collect_count = data.count;
  });
}

function toggleFollow() {
  if (!userStore.token) {
    const pages = getCurrentPages();
    const currentPage = pages[pages.length - 1];
    const route = currentPage.route;
    const options = Object.entries(currentPage.options)
      .map(([key, value]) => `${key}=${value}`)
      .join('&');
    const fullPath = options ? `/${route}?${options}` : `/${route}`;
    const redirect = encodeURIComponent(fullPath);
    uni.navigateTo({ url: `/pages/login/index?redirect=${redirect}` });
    return;
  }

  if (detail.value.is_followed) {
    uni.showModal({
      title: `取消关注 @${detail.value.author_nickname}？`,
      success: (res) => {
        if (res.confirm) {
          executeToggleFollow();
        }
      }
    });
  } else {
    executeToggleFollow();
  }
}

function executeToggleFollow() {
  run(async () => {
    const prevState = detail.value.is_followed;
    detail.value.is_followed = !prevState;
    try {
      const data = await toggleFollowApi(detail.value.author_id);
      detail.value.is_followed = data.active;
    } catch (e) {
      detail.value.is_followed = prevState;
      uni.showToast({ title: '操作失败，请重试', icon: 'none' });
    }
  });
}

function sendComment() {
  run(async () => {
    if (!comment.value.trim()) {
      uni.showToast({ title: "评论不能为空", icon: "none" });
      return;
    }
    await createCommentApi(postId.value, { content: comment.value, client_id: createClientId() });
    comment.value = "";
    await loadComments();
    await loadDetail();
  });
}

function handleCommentReply({ commentId, content }) {
  run(async () => {
    await replyCommentApi(postId.value, commentId, { content, client_id: createClientId() });
    await loadComments();
    await loadDetail();
    uni.showToast({ title: "回复成功", icon: "success" });
  });
}

function handleCommentEdit({ commentId, content }) {
  run(async () => {
    await updateCommentApi(postId.value, commentId, { content });
    await loadComments();
    uni.showToast({ title: "编辑成功", icon: "success" });
  });
}

function handleCommentDelete({ commentId }) {
  run(async () => {
    await deleteCommentApi(postId.value, commentId);
    await loadComments();
    await loadDetail();
    uni.showToast({ title: "删除成功", icon: "success" });
  });
}

function handleCommentLike({ commentId }) {
  run(async () => {
    const clientId = createClientId();
    const data = await toggleCommentLikeApi(postId.value, commentId, clientId);
    const commentItem = findComment(commentList.value, commentId);
    if (commentItem) {
      commentItem.is_liked = data.liked;
      commentItem.like_count = data.like_count;
    }
  });
}

function findComment(list, id) {
  for (const item of list) {
    if (item.id === id) return item;
    if (item.replies) {
      const found = findComment(item.replies, id);
      if (found) return found;
    }
  }
  return null;
}

function handleShare() {
  uni.showActionSheet({
    itemList: ['转发给好友', '生成分享海报'],
    success: (res) => {
      if (res.tapIndex === 0) {
        uni.showToast({ title: '请点击右上角「…」→ 转发', icon: 'none', duration: 2000 });
      } else if (res.tapIndex === 1) {
        generatePoster();
      }
    },
  });
}

function generatePoster() {
  run(async () => {
    uni.showLoading({ title: '生成中...' });
    try {
      let localImagePath = '';
      if (detail.value.images?.length > 0) {
        try {
          const dlRes = await new Promise((resolve, reject) => {
            uni.downloadFile({
              url: detail.value.images[0],
              success: (res) => {
                if (res.statusCode === 200) {
                  resolve(res);
                } else {
                  reject(new Error(`download failed: ${res.statusCode}`));
                }
              },
              fail: reject,
            });
          });
          localImagePath = dlRes.tempFilePath;
        } catch {
          localImagePath = '';
        }
      }

      const ctx = uni.createCanvasContext('posterCanvas', instance.proxy);
      const W = 375, H = 500;
      const coverH = Math.floor(H * 0.67);
      const infoH = H - coverH;

      if (localImagePath) {
        ctx.drawImage(localImagePath, 0, 0, W, coverH);
      } else {
        ctx.setFillStyle('#ff6b81');
        ctx.fillRect(0, 0, W, coverH);
      }

      ctx.setFillStyle('#ffffff');
      ctx.fillRect(0, coverH, W, infoH);

      ctx.setFillStyle('#222222');
      ctx.setFontSize(16);
      ctx.setTextBaseline('top');
      const title = detail.value.title || '';
      const maxCharsPerLine = 16;
      const line1 = title.slice(0, maxCharsPerLine);
      const line2 = title.length > maxCharsPerLine
        ? title.slice(maxCharsPerLine, maxCharsPerLine * 2 - 1) + (title.length > maxCharsPerLine * 2 - 1 ? '…' : '')
        : '';
      ctx.fillText(line1, 16, coverH + 16);
      if (line2) ctx.fillText(line2, 16, coverH + 40);

      ctx.setFillStyle('#888888');
      ctx.setFontSize(12);
      const authorY = line2 ? coverH + 68 : coverH + 44;
      ctx.fillText(`@${detail.value.author_nickname || ''}`, 16, authorY);

      ctx.setFillStyle('#ff6b81');
      ctx.setFontSize(13);
      ctx.setTextAlign('right');
      ctx.fillText('宠光 PetGlow', W - 16, H - 22);

      await new Promise((resolve, reject) => {
        ctx.draw(false, () => {
          uni.canvasToTempFilePath({
            canvasId: 'posterCanvas',
            fileType: 'jpg',
            quality: 0.92,
            success: (res) => {
              posterPath.value = res.tempFilePath;
              resolve();
            },
            fail: reject,
          }, instance.proxy);
        });
      });

      uni.hideLoading();
      showPosterModal.value = true;
    } catch (e) {
      uni.hideLoading();
      uni.showToast({ title: '海报生成失败，请重试', icon: 'none' });
    }
  });
}

function savePoster() {
  run(async () => {
    await new Promise((resolve) => {
      uni.saveImageToPhotosAlbum({
        filePath: posterPath.value,
        success: () => {
          showPosterModal.value = false;
          posterPath.value = '';
          uni.showToast({ title: '已保存到相册', icon: 'success' });
          resolve();
        },
        fail: (err) => {
          const msg = err?.errMsg || '';
          const isPermissionError = msg.includes('auth') || msg.includes('authorize')
            || msg.includes('denied') || msg.includes('scope') || msg.includes('拒绝');
          if (isPermissionError) {
            uni.showModal({
              title: '需要相册权限',
              content: '保存海报需要访问您的相册，是否前往设置开启？',
              confirmText: '去设置',
              success: (res) => {
                if (res.confirm) uni.openSetting();
              },
            });
          } else {
            uni.showToast({ title: '保存失败，请重试', icon: 'none' });
          }
          resolve();
        },
      });
    });
  });
}

onLoad((options) => {
  postId.value = Number(options.id || 0);
  loadDetail();
  loadComments();
  uni.showShareMenu({ withShareTicket: true, menus: ['shareAppMessage', 'shareTimeline'] });
});

onShareAppMessage(() => {
  const coverImage = detail.value.images?.[0];
  return {
    title: detail.value.title || '来看看这个萌宠帖子',
    path: `/pages/post-detail/index?id=${postId.value}`,
    ...(coverImage ? { imageUrl: coverImage } : {}),
  };
});

onShareTimeline(() => {
  const coverImage = detail.value.images?.[0];
  return {
    title: detail.value.title || '来看看这个萌宠帖子',
    query: `id=${postId.value}`,
    ...(coverImage ? { imageUrl: coverImage } : {}),
  };
});
</script>

<style lang="scss" scoped>
.container {
  padding-bottom: 140rpx;
}

.top-author-bar {
  position: sticky;
  top: 0;
  z-index: $z-index-sticky;
  background: $bg-color-warm;
  padding: $spacing-base $spacing-lg;
  display: flex;
  align-items: center;
  gap: $spacing-base;
  border-bottom: $border-width-thick solid $border-color;
}

.author-info {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.author-name {
  font-size: $font-size-base;
  font-weight: $font-weight-semibold;
  color: $text-color-primary;
}

.publish-time {
  font-size: $font-size-sm;
  color: $text-color-muted;
  margin-top: $spacing-base;
}

.swiper {
  height: 500rpx;
}

.cover {
  width: 100%;
  height: 100%;
}

.detail-card,
.comments-card {
  margin: $spacing-base;
  display: flex;
  flex-direction: column;
  gap: $spacing-base;
}

.title {
  font-size: $font-size-xl;
  font-weight: $font-weight-bold;
  color: $text-color-primary;
}

.content {
  color: $text-color-secondary;
  font-size: $font-size-base;
  line-height: $line-height-relaxed;
}

.follow-btn {
  margin-left: auto;
  background: linear-gradient(135deg, $primary-color 0%, $secondary-color 100%);
  color: $text-color-inverse;
  border-radius: $border-radius-full;
  border: none;
  font-size: $font-size-sm;
  padding: $spacing-xs $spacing-base;
  
  &.followed {
    background: $bg-color-gray;
    color: $text-color-secondary;
  }
}

.section-title {
  font-weight: $font-weight-semibold;
  font-size: $font-size-lg;
  color: $text-color-primary;
}

.bottom-bar {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  padding: $spacing-base $spacing-lg;
  background: $bg-color-warm;
  border-top: $border-width-thick solid $border-color;
  box-shadow: 0 -4rpx 16rpx rgba(0, 0, 0, 0.05);
}

.action-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rpx;
  padding: $spacing-xs;
  transition: all $transition-fast;

  &.active {
    .action-text {
      color: $primary-color;
    }
  }

  &:active {
    transform: scale(0.95);
  }
}

.action-icon {
  font-size: 36rpx;
}

.action-text {
  font-size: $font-size-xs;
  color: $text-color-muted;
}

.comment-input-wrap {
  flex: 1;
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  background: $bg-color-gray;
  border-radius: $border-radius-full;
  padding: 0 $spacing-sm;
}

.comment-input {
  flex: 1;
  background: transparent;
  border-radius: $border-radius-full;
  padding: $spacing-sm;
  font-size: $font-size-sm;
}

.poster-canvas {
  position: fixed;
  left: -9999rpx;
  top: -9999rpx;
  width: 375px;
  height: 500px;
}

.poster-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: $z-index-modal;
}

.poster-modal {
  background: $bg-color-card;
  border-radius: $border-radius-xl;
  padding: $spacing-lg;
  width: 640rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: $spacing-base;
}

.poster-preview {
  width: 560rpx;
  height: 747rpx;
  border-radius: $border-radius-base;
}

.poster-actions {
  display: flex;
  gap: $spacing-base;
  width: 100%;
  justify-content: center;
}
</style>
