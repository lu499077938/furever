import { request } from "./request";

export const notificationsApi = (params) => request({ url: "/notifications", method: "GET", data: params });
export const unreadCountApi = () => request({ url: "/notifications/unread-count", method: "GET" });
export const readAllApi = () => request({ url: "/notifications/read-all", method: "PUT" });
