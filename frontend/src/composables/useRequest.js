import { ref } from "vue";

import { request as baseRequest } from "../api/request";

export function useRequest() {
  const loading = ref(false);
  const error = ref("");

  async function request(options) {
    loading.value = true;
    error.value = "";
    try {
      return await baseRequest(options);
    } catch (err) {
      error.value = err?.message || "请求失败";
      throw err;
    } finally {
      loading.value = false;
    }
  }

  return { loading, error, request };
}
