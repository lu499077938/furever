import { request } from "./request";

export const meApi = () => request({ url: "/users/me", method: "GET" });
export const updateNicknameApi = (payload) => request({ url: "/users/me/nickname", method: "PUT", data: payload });
export const updatePasswordApi = (payload) => request({ url: "/users/me/password", method: "PUT", data: payload });
export const updateAvatarApi = (avatar) => request({ url: "/users/me/avatar", method: "PUT", data: { avatar } });
