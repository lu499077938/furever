import { request } from "./request";

export function uploadImageApi(filePath) {
  const token = uni.getStorageSync("token");
  return new Promise((resolve, reject) => {
    uni.uploadFile({
      url: "http://127.0.0.1:8000/api/v1/upload/image",
      filePath,
      name: "file",
      header: token ? { Authorization: `Bearer ${token}` } : {},
      success(res) {
        const payload = JSON.parse(res.data || "{}");
        if (payload.code !== 0) {
          reject(new Error(payload.msg || "上传失败"));
          return;
        }
        resolve(payload.data);
      },
      fail: reject,
    });
  });
}
