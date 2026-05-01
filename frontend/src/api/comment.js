import { request } from "./request";

export const listCommentsApi = (postId, params) => request({ url: `/posts/${postId}/comments`, method: "GET", data: params });
export const createCommentApi = (postId, payload) => request({ url: `/posts/${postId}/comments`, method: "POST", data: payload });
export const replyCommentApi = (postId, commentId, payload) => request({ url: `/posts/${postId}/comments/${commentId}/reply`, method: "POST", data: payload });
export const updateCommentApi = (postId, commentId, payload) => request({ url: `/posts/${postId}/comments/${commentId}`, method: "PUT", data: payload });
export const deleteCommentApi = (postId, commentId) => request({ url: `/posts/${postId}/comments/${commentId}`, method: "DELETE" });
export const toggleCommentLikeApi = (postId, commentId, clientId) => request({ url: `/posts/${postId}/comments/${commentId}/like?client_id=${clientId}`, method: "POST" });
export const getCommentRepliesApi = (postId, commentId, params) => request({ url: `/posts/${postId}/comments/${commentId}/replies`, method: "GET", data: params });
export const getCommentLikesApi = (postId, commentId, params) => request({ url: `/posts/${postId}/comments/${commentId}/likes`, method: "GET", data: params });
