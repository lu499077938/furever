<script setup>
import { ref } from 'vue';

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: '',
  },
  placeholder: {
    type: String,
    default: '请输入...',
  },
  type: {
    type: String,
    default: 'text',
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  clearable: {
    type: Boolean,
    default: false,
  },
  maxlength: {
    type: Number,
    default: 140,
  }
});

const emit = defineEmits(['update:modelValue', 'focus', 'blur', 'confirm']);

const isFocused = ref(false);

const handleInput = (e) => {
  emit('update:modelValue', e.detail.value);
};

const handleFocus = (e) => {
  isFocused.value = true;
  emit('focus', e);
};

const handleBlur = (e) => {
  isFocused.value = false;
  emit('blur', e);
};

const handleConfirm = (e) => {
  emit('confirm', e);
};

const handleClear = () => {
  emit('update:modelValue', '');
};
</script>

<template>
  <view class="pet-input-wrapper" :class="{ 'is-focused': isFocused, 'is-disabled': disabled }">
    <slot name="prefix"></slot>
    <input
      class="pet-input"
      :value="modelValue"
      :type="type"
      :placeholder="placeholder"
      :placeholder-class="'pet-input-placeholder'"
      :disabled="disabled"
      :maxlength="maxlength"
      @input="handleInput"
      @focus="handleFocus"
      @blur="handleBlur"
      @confirm="handleConfirm"
    />
    <view 
      v-if="clearable && modelValue && !disabled" 
      class="pet-input-clear" 
      @click.stop="handleClear"
    >
      <text class="clear-icon">×</text>
    </view>
    <slot name="suffix"></slot>
  </view>
</template>

<style lang="scss" scoped>
.pet-input-wrapper {
  display: flex;
  align-items: center;
  background-color: $bg-color-gray;
  border-radius: $border-radius-xl;
  padding: 0 $spacing-base;
  height: 96rpx;
  border: $border-width-thick solid transparent;
  box-shadow: $box-shadow-inner-sm;
  transition: all $transition-base;

  &.is-focused {
    background-color: $bg-color-card;
    border-color: $primary-color-light;
    box-shadow: 
      0 0 0 6rpx rgba($primary-color, 0.15),
      $box-shadow-base;
  }

  &.is-disabled {
    opacity: 0.5;
    background-color: $bg-color-muted;
    cursor: not-allowed;
  }
}

.pet-input {
  flex: 1;
  height: 100%;
  font-size: $font-size-base;
  color: $text-color-primary;
  background: transparent;
  border: none;
  outline: none;
  padding: 0 $spacing-xs;
}

.pet-input-placeholder {
  color: $text-color-muted;
  font-size: $font-size-base;
}

.pet-input-clear {
  @include flex-center;
  width: 44rpx;
  height: 44rpx;
  border-radius: 50%;
  background-color: rgba($primary-color, 0.1);
  transition: all $transition-fast;

  &:active {
    background-color: rgba($primary-color, 0.2);
    transform: scale(0.9);
  }
}

.clear-icon {
  color: $primary-color;
  font-size: 28rpx;
  font-weight: $font-weight-bold;
  line-height: 1;
}
</style>
