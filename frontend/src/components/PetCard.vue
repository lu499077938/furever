<script setup>
const props = defineProps({
  padding: {
    type: Boolean,
    default: true,
  },
  margin: {
    type: Boolean,
    default: true,
  },
  shadow: {
    type: Boolean,
    default: true,
  },
  radius: {
    type: String,
    default: 'xl',
  },
  bgColor: {
    type: String,
    default: '',
  },
  hoverable: {
    type: Boolean,
    default: true,
  }
});
</script>

<template>
  <view
    class="pet-card"
    :class="[
      {
        'pet-card--padding': padding,
        'pet-card--margin': margin,
        'pet-card--shadow': shadow,
        'pet-card--hoverable': hoverable,
      },
      `pet-card--radius-${radius}`
    ]"
    :style="{ backgroundColor: bgColor || undefined }"
  >
    <slot></slot>
  </view>
</template>

<style lang="scss" scoped>
.pet-card {
  box-sizing: border-box;
  overflow: hidden;
  background-color: $bg-color-card;
  border: $border-width-thick solid $border-color;
  transition: all $transition-base;
  position: relative;

  &--padding {
    padding: $spacing-base;
  }

  &--margin {
    margin-bottom: $spacing-base;
  }

  &--shadow {
    box-shadow: $clay-shadow;
  }

  &--hoverable {
    &:active {
      box-shadow: $clay-shadow-active;
      transform: scale(0.99);
    }
  }

  &--radius-sm {
    border-radius: $border-radius-sm;
  }

  &--radius-base {
    border-radius: $border-radius-base;
  }

  &--radius-lg {
    border-radius: $border-radius-lg;
  }

  &--radius-xl {
    border-radius: $border-radius-xl;
  }

  &--radius-2xl {
    border-radius: $border-radius-2xl;
  }
}
</style>
