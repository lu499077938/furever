<script setup>
</script>

<template>
</template>

<style lang="scss">
@import "@/uni.scss";

page {
  background: $bg-color;
  color: $text-color-primary;
  font-size: $font-size-base;
  font-family: $font-family-base;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.card {
  @include clay-card;
  padding: $spacing-base;
  margin-bottom: $spacing-base;
}

::-webkit-scrollbar {
  display: none;
  width: 0 !important;
  height: 0 !important;
  -webkit-appearance: none;
  background: transparent;
}

button {
  font-family: $font-family-base;
  
  &::after {
    border: none;
  }
}

input, textarea {
  font-family: $font-family-base;
}
</style>
