import { defineStore } from "pinia";
import { ref } from "vue";
import { pointsOverviewApi } from "../api/points";

export const usePointsStore = defineStore("points", () => {
  const totalPoints = ref(0);

  function setTotalPoints(value) {
    totalPoints.value = Number(value) || 0;
  }

  const fetchPoints = async () => {
    try {
      const data = await pointsOverviewApi();
      setTotalPoints(data.total_points);
    } catch (e) {
      console.error(e);
    }
  };

  return {
    totalPoints,
    setTotalPoints,
    fetchPoints,
  };
});
