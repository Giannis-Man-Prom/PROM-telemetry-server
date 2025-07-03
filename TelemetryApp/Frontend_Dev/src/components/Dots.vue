<template>
  <div class="colored-dots-wrapper">
    <div class="header-section">
      <span class="header-text">{{ title }}</span>

      <button class="btn-style">
        <div>
          <span>Imax:</span>
          <br>
          <span>{{ currentValue1 }}</span>
        </div>
      </button>

      <button class="btn-style">
        <div>
          <span>actual inverter status:</span>
          <br>
          <span>{{ printActualInverterStatus(currentValue2) }}</span>
        </div>
      </button>
    </div>

    <div class="dots-container" :style="{ gap: gap }">
      <div
        v-for="(item, index) in currentBoolValues"
        :key="index"
        class="dot-wrapper"
      >
        <span :class="['dot', item.active ? 'green' : 'red']"></span>
        <span class="dot-label">{{ item.label }}</span>
      </div>
    </div>
  </div>
</template>


<script lang="ts">
interface BoolValue {
  active: boolean;
  label: string;
}
import { watch, ref } from 'vue';
export default {
  name: 'ColoredDots',
  props: {
    title: {
      type: String,
      required: true
    },
    bool_values: {
      type: Array as () => BoolValue[],
      required: true,
      validator: (arr: BoolValue[]) =>
        arr.every(
          (i) => typeof i.active === 'boolean' && typeof i.label === 'string'
        ),
    },
    gap: {
      type: String,
      default: '50px'
    },
    value1: {
      type: Number,
      required: true
    },
    value2: {
      type: Number,
      required: true
    }
  },
  setup(props) {
    // If you want to store local copies (e.g., for animations or transitions), use refs:
    const currentValue1 = ref(props.value1);
    const currentValue2 = ref(props.value2);
    const currentBoolValues = ref([...props.bool_values]);

    const printActualInverterStatus = (ind: number): string => {
      const messages = [
        'INVERTER_DISABLE', // 0
        'INVERTER_ENABLE'   // 1
      ];
      return messages[ind] ?? 'Not available';
    };

    // Watch value1
    watch(
      () => props.value1,
      (newVal, oldVal) => {
        currentValue1.value = newVal;
      },
      { immediate: true }
    );

    // Watch value2
    watch(
      () => props.value2,
      (newVal, oldVal) => {
        currentValue2.value = newVal;
      },
      { immediate: true }
    );

    // Watch bool_values
    watch(
      () => props.bool_values,
      (newVal, oldVal) => {
        currentBoolValues.value = [...newVal];
      },
      { deep: true, immediate: true }
    );

    return {
      currentValue1,
      currentValue2,
      currentBoolValues,
      printActualInverterStatus
    };
  }
};
</script>

<style scoped>
.dots-container {
  display: flex;
  justify-content: center;
  gap: 50px; /* space between each dot+label */
  align-items: flex-start;
}

.dot-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center; /* center dot and label horizontally */
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  display: inline-block;
  background-color: red;
}

.dot.green {
  background-color: green;
}

.dot-label {
  margin-top: 6px;
  font-size: 12px;
  color: #fff;
}

.flex {
  position: relative; /* Ensure the container is positioned relative */
}

.cap-size {
  min-width: 90px;
  min-height: 40px;
  max-width: 120px;
  max-height: 48px;
}

.overflow-hidden {
  overflow: hidden;
  text-overflow: ellipsis; /* Show ellipsis for overflow text */
  white-space: nowrap; /* Prevent text from wrapping */
}
.header-section {
  display: flex;           /* arrange items horizontally */
  align-items: center;     /* vertically align items to the middle */
  gap: 12px;               /* spacing between header text and buttons */
  margin-bottom: 16px;     /* optional: add space between header and dots */
}

.header-text {
  font-size: 16px;
  color: white;
  font-weight: 600;
}

.btn-style {
  display: flex;
  flex-direction: column;
  justify-content: start;
  padding: 4px;
  color: white;
  background-color: #1e40af; /* equivalent to Tailwind bg-blue-800 */
  border-radius: 0.5rem;
  font-size: 0.75rem;
  text-align: left;
  overflow: hidden;
  min-width: 90px;
  min-height: 40px;
  max-width: 120px;
  max-height: 48px;
  white-space: nowrap;
  text-overflow: ellipsis;
}
</style>
