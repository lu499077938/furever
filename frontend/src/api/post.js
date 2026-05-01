import { request } from "./request";

export const listPostsApi = (params) => request({ url: "/posts", method: "GET", data: params });
export const searchPostsApi = (params) => request({ url: "/posts/search", method: "GET", data: params });
export const postDetailApi = (id) => request({ url: `/posts/${id}`, method: "GET" });
export const createPostApi = (payload) => request({ url: "/posts", method: "POST", data: payload });
export const myPostsApi = (params) => request({ url: "/users/me/posts", method: "GET", data: params });
export const myCollectsApi = (params) => request({ url: "/users/me/collects", method: "GET", data: params });
export const myLikesApi = (params) => request({ url: "/users/me/likes", method: "GET", data: params });
