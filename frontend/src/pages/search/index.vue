<template>
  <view class="page">
    <view class="search-box">
      <view class="search-input-wrap">
        <text class="search-icon">🔍</text>
        <input v-model="keyword" placeholder="搜索标题或内容" class="search-input" @input="onInput" />
      </view>
    </view>
    
    <view v-if="showHistory" class="history-section">
      <view class="history-header">
        <text class="history-title">🐾 历史搜索</text>
        <text class="history-clear" @tap="clearHistory">清空</text>
      </view>
      <view class="history-list">
        <view v-for="item in historyList" :key="item" class="history-item" @tap="searchByHistory(item)">
          <text class="history-keyword">{{ item }}</text>
          <text class="history-delete" @tap.stop="removeKeyword(item)">✕</text>
        </view>
      </view>
    </view>
    
    <view v-else class="results-section">
      <PostCard v-for="item in list" :key="item.id" :post="item" />
      <Loading v-if="loading" />
      <Empty v-else-if="showEmpty" text="没有找到相关内容 🐱" />
    </view>
  </view>
</template>

<script setup>
import { computed, ref } from "vue";
import { onReachBottom } from "@dcloudio/uni-app";
import PostCard from "../../components/PostCard.vue";
import Loading from "../../components/Loading.vue";
import Empty from "../../components/Empty.vue";
import { debounce } from "../../utils/debounce";
import { searchPostsApi } from "../../api/post";

const SEARCH_HISTORY_KEY = "search_history";
const SEARCH_HISTORY_LIMIT = 10;

const keyword = ref("");
const page = ref(1);
const list = ref([]);
const total = ref(0);
const loading = ref(false);
const historyList = ref([]);

const showHistory = computed(() => !keyword.value.trim() && historyList.value.length > 0);
const showEmpty = computed(() => !loading.value && list.value.length === 0 && !!keyword.value.trim());

function resetSearchState() {
  list.value = [];
  page.value = 1;
  total.value = 0;
}

function loadHistory() {
  const raw = uni.getStorageSync(SEARCH_HISTORY_KEY);
  if (!raw) {
    historyList.value = [];
    return;
  }
  try {
    const parsed = Array.isArray(raw) ? raw : JSON.parse(raw);
    historyList.value = Array.isArray(parsed)
      ? parsed.filter((item) => typeof item === "string").slice(0, SEARCH_HISTORY_LIMIT)
      : [];
  } catch {
    historyList.value = [];
  }
}

function updateHistory(nextHistory) {
  historyList.value = nextHistory;
  if (nextHistory.length === 0) {
    uni.removeStorageSync(SEARCH_HISTORY_KEY);
    return;
  }
  uni.setStorageSync(SEARCH_HISTORY_KEY, JSON.stringify(nextHistory));
}

function saveKeyword(kw) {
  const normalizedKeyword = kw.trim();
  if (!normalizedKeyword) return;
  const nextHistory = [normalizedKeyword, ...historyList.value.filter((item) => item !== normalizedKeyword)].slice(
    0,
    SEARCH_HISTORY_LIMIT,
  );
  updateHistory(nextHistory);
}

function removeKeyword(kw) {
  updateHistory(historyList.value.filter((item) => item !== kw));
}

function clearHistory() {
  updateHistory([]);
}

function searchByHistory(kw) {
  keyword.value = kw;
  search(true);
}

async function search(reset = false) {
  const trimmedKeyword = keyword.value.trim();
  if (!trimmedKeyword) {
    resetSearchState();
    return;
  }
  if (loading.value) return;
  if (!reset && total.value > 0 && list.value.length >= total.value) return;
  const requestKeyword = trimmedKeyword;
  loading.value = true;
  if (reset) {
    resetSearchState();
  }
  try {
    const data = await searchPostsApi({ q: requestKeyword, page: page.value, page_size: 20 });
    if (requestKeyword !== keyword.value.trim()) return;
    total.value = data.total || 0;
    list.value = list.value.concat(data.items || []);
    page.value += 1;
    saveKeyword(requestKeyword);
  } finally {
    loading.value = false;
  }
}

const onInput = debounce(() => search(true), 300);

loadHistory();
onReachBottom(() => search(false));
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background: $bg-color-warm;
}

.search-box {
  padding: $spacing-base;
  background: $bg-color-card;
  border-bottom: $border-width-thick solid $border-color;
}

.search-input-wrap {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  background: $bg-color-gray;
  border-radius: $border-radius-full;
  padding: $spacing-sm $spacing-base;
  border: $border-width-thick solid $border-color;
  transition: all $transition-base;

  &:focus-within {
    border-color: $primary-color;
    box-shadow: 0 0 0 6rpx rgba($primary-color, 0.1);
  }
}

.search-icon {
  font-size: 32rpx;
}

.search-input {
  flex: 1;
  font-size: $font-size-base;
  color: $text-color-primary;
}

.history-section {
  padding: $spacing-base;
}

.history-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: $spacing-base;
}

.history-title {
  color: $text-color-primary;
  font-size: $font-size-base;
  font-weight: $font-weight-semibold;
}

.history-clear {
  color: $text-color-muted;
  font-size: $font-size-sm;
  padding: $spacing-xs $spacing-sm;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: $spacing-sm;
}

.history-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: $bg-color-card;
  border-radius: $border-radius-xl;
  padding: $spacing-base $spacing-lg;
  border: $border-width-thick solid $border-color;
  box-shadow: $box-shadow-sm;
  transition: all $transition-fast;

  &:active {
    transform: scale(0.98);
    background: $bg-color-gray;
  }
}

.history-keyword {
  color: $text-color-primary;
  font-size: $font-size-base;
  font-weight: $font-weight-medium;
}

.history-delete {
  color: $text-color-muted;
  font-size: $font-size-sm;
  padding: $spacing-xs;
}

.results-section {
  padding: $spacing-base;
}
</style>
