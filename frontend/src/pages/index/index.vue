<template>
  <view class="container">
    <NavBar :background="true" :fixed="true">
      <template #title>
        <view class="refresh-btn" @click="handleRefresh" :class="{ 'is-rotating': isRefreshing }">
          <text class="refresh-icon">↻</text>
        </view>
      </template>
      <view class="actions">
        <PetButton size="small" type="outline" @click="goSearch">
          <text>搜索</text>
        </PetButton>
        <PetButton 
          size="small" 
          :type="checkinStatus.checked_in_today ? 'secondary' : 'primary'"
          @click="goCheckin"
        >
          <text>{{ checkinStatus.checked_in_today ? "已签到" : `签到 ${checkinStatus.streak_days || 0}天` }}</text>
        </PetButton>
      </view>
    </NavBar>

    <view class="waterfall">
      <view class="col">
        <PostCard v-for="item in left" :key="item.id" :post="item" />
      </view>
      <view class="col">
        <PostCard v-for="item in right" :key="item.id" :post="item" />
      </view>
    </view>
    
    <Loading v-if="loading" />
    <Empty v-else-if="list.length === 0" text="还没有帖子，去发布第一条吧" />
  </view>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { onLoad, onReachBottom, onShow } from "@dcloudio/uni-app";
import NavBar from "../../components/NavBar.vue";
import PostCard from "../../components/PostCard.vue";
import Loading from "../../components/Loading.vue";
import Empty from "../../components/Empty.vue";
import PetButton from "../../components/PetButton.vue";
import { listPostsApi } from "../../api/post";
import { checkinStatusApi } from "../../api/checkin";

const page = ref(1);
const loading = ref(false);
const list = ref([]);
const total = ref(0);
const checkinStatus = ref({});
const isRefreshing = ref(false);

async function handleRefresh() {
  if (isRefreshing.value) return;
  isRefreshing.value = true;
  await loadPosts(true);
  await loadCheckinStatus();
  setTimeout(() => {
    isRefreshing.value = false;
  }, 500);
}

const left = computed(() => list.value.filter((_, idx) => idx % 2 === 0));
const right = computed(() => list.value.filter((_, idx) => idx % 2 === 1));

async function loadPosts(reset = false) {
  if (loading.value) return;
  if (!reset && total.value > 0 && list.value.length >= total.value) return;
  loading.value = true;
  if (reset) {
    page.value = 1;
    list.value = [];
  }
  try {
    const data = await listPostsApi({ page: page.value, page_size: 20 });
    total.value = data.total || 0;
    list.value = list.value.concat(data.items || []);
    page.value += 1;
  } finally {
    loading.value = false;
  }
}

async function loadCheckinStatus() {
  try {
    checkinStatus.value = await checkinStatusApi();
  } catch (_error) {
    checkinStatus.value = { checked_in_today: false, streak_days: 0 };
  }
}

function goSearch() {
  uni.navigateTo({ url: "/pages/search/index" });
}

function goCheckin() {
  uni.navigateTo({ url: "/pages/checkin/index" });
}

onLoad(() => {
  loadPosts(true);
});

onMounted(() => {
  if (list.value.length === 0) {
    loadPosts(true);
  }
});

onShow(() => {
  loadCheckinStatus();
});

onReachBottom(() => {
  loadPosts(false);
});
</script>

<style lang="scss" scoped>
.container {
  min-height: 100vh;
  @include safe-area-bottom;
}

.refresh-btn {
  @include flex-center;
  width: 64rpx;
  height: 64rpx;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba($primary-color, 0.1) 0%, rgba($secondary-color, 0.1) 100%);
  border: $border-width-thick solid $border-color;
  transition: all $transition-base;
  
  &:active {
    background: linear-gradient(135deg, rgba($primary-color, 0.2) 0%, rgba($secondary-color, 0.2) 100%);
    transform: scale(0.95);
  }
}

.refresh-icon {
  font-size: 32rpx;
  color: $primary-color;
  font-weight: $font-weight-bold;
}

.is-rotating .refresh-icon {
  animation: spin 1s linear infinite;
}

.actions {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
}

.waterfall {
  display: flex;
  padding: $spacing-base $spacing-xs $spacing-xs;
  box-sizing: border-box;
}

.col {
  flex: 1;
  display: flex;
  flex-direction: column;
  width: 50%;
}
</style>
