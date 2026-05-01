import { defineStore } from "pinia";

export const useUserStore = defineStore("user", {
  state: () => ({
    token: uni.getStorageSync("token") || "",
    profile: null,
  }),
  actions: {
    setLogin(token, profile) {
      this.token = token;
      this.profile = profile;
      uni.setStorageSync("token", token);
    },
    setProfile(profile) {
      this.profile = profile;
    },
    logout() {
      this.token = "";
      this.profile = null;
      uni.removeStorageSync("token");
    },
  },
});
