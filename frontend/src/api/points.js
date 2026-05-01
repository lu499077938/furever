import { request } from "./request";

export const pointsOverviewApi = () => request({ url: "/points", method: "GET" });
export const pointsLogsApi = (params) => request({ url: "/points/logs", method: "GET", data: params });
