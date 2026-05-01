import { ref } from "vue";

export function useButtonLock() {
  const isLocked = ref(false);

  const runWithLock = async (fn) => {
    if (isLocked.value) return;
    isLocked.value = true;
    try {
      await fn();
    } finally {
      isLocked.value = false;
    }
  };

  return {
    // 兼容旧命名与页面现有用法
    locked: isLocked,
    run: runWithLock,
    isLocked,
    runWithLock,
  };
}
