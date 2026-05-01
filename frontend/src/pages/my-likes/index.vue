<template>
  <view class="page">
    <view class="posts-list">
      <PostCard v-for="item in list" :key="item.id" :post="item" />
    </view>
    <Loading v-if="loading" />
    <Empty v-else-if="list.length === 0" text="还没有点赞记录 ❤️" />
  </view>
</template>

<script setup>
import { ref } from "vue";
import { onLoad, onReachBottom } from "@dcloudio/uni-app";
import PostCard from "../../components/PostCard.vue";
import Loading from "../../components/Loading.vue";
import Empty from "../../components/Empty.vue";
import { myLikesApi } from "../../api/post";

const page = ref(1);
const total = ref(0);
const list = ref([]);
const loading = ref(false);

async function load(reset = false) {
  if (loading.value) return;
  if (!reset && total.value > 0 && list.value.length >= total.value) return;
  loading.value = true;
  if (reset) {
    page.value = 1;
    list.value = [];
  }
  try {
    const data = await myLikesApi({ page: page.value, page_size: 20 });
    total.value = data.total || 0;
    list.value = list.value.concat(data.items || []);
    page.value += 1;
  } finally {
    loading.value = false;
  }
}

onLoad(() => load(true));
onReachBottom(() => load(false));
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background: $bg-color-warm;
  padding: $spacing-base;
}

.posts-list {
  display: flex;
  flex-direction: column;
  gap: $spacing-base;
}
</style>
