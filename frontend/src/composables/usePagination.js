import { ref } from "vue";

export function usePagination(pageSize = 20) {
  const page = ref(1);
  const total = ref(0);
  const items = ref([]);
  const loading = ref(false);

  async function load(fetcher, reset = false) {
    if (loading.value) {
      return;
    }
    loading.value = true;
    if (reset) {
      page.value = 1;
      items.value = [];
    }
    try {
      const data = await fetcher({ page: page.value, page_size: pageSize });
      total.value = data.total || 0;
      items.value = [...items.value, ...(data.items || [])];
      if (items.value.length < total.value) {
        page.value += 1;
      }
    } finally {
      loading.value = false;
    }
  }

  return { page, total, items, loading, load };
}
