import { request } from "./request";

export function toggleFollowApi(targetUserId) {
  return request({
    url: `/users/${targetUserId}/follow`,
    method: "POST",
  });
}
