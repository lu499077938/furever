import { request } from "./request";

export const loginApi = (payload) => request({ url: "/auth/login", method: "POST", data: payload });
export const registerApi = (payload) => request({ url: "/auth/register", method: "POST", data: payload });
