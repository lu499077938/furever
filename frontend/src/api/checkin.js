import { request } from "./request";

export const checkinApi = () => request({ url: "/checkin", method: "POST" });
export const checkinStatusApi = () => request({ url: "/checkin/status", method: "GET" });
