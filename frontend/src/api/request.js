const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api/v1";
const pendingRequests = new Map();

function requestKey(options = {}) {
  const method = (options.method || "GET").toUpperCase();
  return `${method}:${options.url}`;
}

export function apiRequest(options = {}) {
  const key = requestKey(options);
  if (pendingRequests.has(key)) {
    return Promise.reject(new Error("请求进行中，请勿重复提交"));
  }

  pendingRequests.set(key, true);
  const token = uni.getStorageSync("token");

  return new Promise((resolve, reject) => {
    uni.request({
      ...options,
      url: `${BASE_URL}${options.url}`,
      header: {
        ...(options.header || {}),
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      success: (res) => {
        console.log("Response:", res);
        const payload = res.data || {};
        if (payload.code !== 0) {
          uni.showToast({ title: payload.msg || "请求失败", icon: "none" });
          reject(new Error(payload.msg || "请求失败"));
          return;
        }
        resolve(payload.data);
      },
      fail: (err) => {
        console.error("Request failed:", err);
        uni.showToast({ title: "网络异常，请稍后再试", icon: "none" });
        reject(err);
      },
      complete: () => pendingRequests.delete(key),
    });
  });
}

export function getPendingRequestCount() {
  return pendingRequests.size;
}

export function request(options = {}) {
  return apiRequest(options);
}
