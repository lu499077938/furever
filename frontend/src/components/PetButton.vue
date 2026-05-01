<script setup>
import { computed } from 'vue';

const props = defineProps({
  type: {
    type: String,
    default: 'primary',
  },
  size: {
    type: String,
    default: 'medium',
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  loading: {
    type: Boolean,
    default: false,
  },
  block: {
    type: Boolean,
    default: false,
  },
  round: {
    type: Boolean,
    default: true,
  }
});

const emit = defineEmits(['click']);

const handleClick = (e) => {
  if (props.disabled || props.loading) return;
  emit('click', e);
};

const buttonClasses = computed(() => {
  return [
    'pet-btn',
    `pet-btn--${props.type}`,
    `pet-btn--${props.size}`,
    {
      'pet-btn--disabled': props.disabled,
      'pet-btn--loading': props.loading,
      'pet-btn--block': props.block,
      'pet-btn--round': props.round,
    }
  ];
});
</script>

<template>
  <button :class="buttonClasses" @click="handleClick" :disabled="disabled">
    <view v-if="loading" class="pet-btn__loading">
      <view class="pet-btn__spinner"></view>
    </view>
    <slot></slot>
  </button>
</template>

<style lang="scss" scoped>
.pet-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  box-sizing: border-box;
  margin: 0;
  padding: 0;
  font-family: $font-family-base;
  font-weight: $font-weight-semibold;
  text-align: center;
  white-space: nowrap;
  cursor: pointer;
  transition: all $transition-base;
  border: none;
  outline: none;
  position: relative;
  overflow: hidden;

  &::after {
    border: none;
  }

  &--small {
    height: 64rpx;
    padding: 0 $spacing-lg;
    font-size: $font-size-sm;
    border-radius: $border-radius-lg;
  }

  &--medium {
    height: 88rpx;
    padding: 0 $spacing-xl;
    font-size: $font-size-base;
    border-radius: $border-radius-xl;
  }

  &--large {
    height: 104rpx;
    padding: 0 $spacing-2xl;
    font-size: $font-size-lg;
    border-radius: $border-radius-xl;
  }

  &--round {
    border-radius: $border-radius-full;
  }

  &--block {
    display: flex;
    width: 100%;
  }

  &--primary {
    background: linear-gradient(135deg, $primary-color 0%, $primary-color-dark 100%);
    color: $text-color-inverse;
    box-shadow: $clay-shadow;
    border: $border-width-thick solid rgba(255, 255, 255, 0.2);

    &:active {
      background: linear-gradient(135deg, $primary-color-dark 0%, darken($primary-color-dark, 5%) 100%);
      box-shadow: $clay-shadow-active;
      transform: scale(0.98);
    }
  }

  &--secondary {
    background: linear-gradient(135deg, $secondary-color 0%, $primary-color 100%);
    color: $text-color-inverse;
    box-shadow: 
      0 8rpx 24rpx rgba(251, 146, 60, 0.25),
      inset 0 2rpx 4rpx rgba(255, 255, 255, 0.6);
    border: $border-width-thick solid rgba(255, 255, 255, 0.2);

    &:active {
      box-shadow: $clay-shadow-active;
      transform: scale(0.98);
    }
  }

  &--outline {
    background-color: transparent;
    color: $primary-color;
    border: $border-width-thick solid $primary-color;
    box-shadow: none;

    &:active {
      background-color: $primary-color-pale;
      transform: scale(0.98);
    }
  }

  &--text {
    background-color: transparent;
    color: $text-color-secondary;
    box-shadow: none;

    &:active {
      color: $primary-color;
    }
  }

  &--disabled {
    cursor: not-allowed;
    opacity: 0.5;
    
    &:active {
      transform: none;
    }
  }

  &--loading {
    pointer-events: none;
  }

  &__loading {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: $spacing-xs;
  }

  &__spinner {
    width: 32rpx;
    height: 32rpx;
    border: 4rpx solid rgba(255, 255, 255, 0.3);
    border-top-color: #fff;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>
