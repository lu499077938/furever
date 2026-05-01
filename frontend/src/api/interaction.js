import { request } from "./request";

export const toggleLikeApi = (postId) => request({ url: `/posts/${postId}/like`, method: "POST" });
export const toggleCollectApi = (postId) => request({ url: `/posts/${postId}/collect`, method: "POST" });
