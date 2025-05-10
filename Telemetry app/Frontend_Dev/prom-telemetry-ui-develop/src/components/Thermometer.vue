<template>
  <div class="flex items-center justify-center min-h-1/2 rounded bg-gray-50 dark:bg-gray-800">
    <div class="thermometer-container min-h-[200px]"> <!-- Set a minimum height for the container -->
      <!-- Label at the top -->
      <div class="thermometer-top-label">{{ title }}</div>

      <!-- Thermometer Component -->
      <div class="thermometer">
        <!-- Set the height of the inner thermometer based on the temperature percentage -->
        <div class="thermometer-inner" :style="{ height: `${temperature}%` }"></div>
      </div>

      <!-- Temperature Label at the bottom -->
      <div class="thermometer-label">{{ temperature }}°C</div>
    </div>
  </div>
</template>


<script lang="ts">
import { defineComponent, ref, watch } from 'vue';

export default defineComponent({
  name: 'LiveThermometer',
  props: {
    temperature: {
      type: Number,
      required: true,
      validator(value: number) {
        return value >= 0 && value <= 100;
      }
    },
    title: {
      type: String,
      required: true
    }
  },
  setup(props) {
    const temperature = ref(props.temperature);

    // Watch for temperature prop changes
    watch(() => props.temperature, (newTemperature) => {
      temperature.value = newTemperature;
    });

    return {
      temperature
    };
  }
});
</script>

<style scoped>
/* Thermometer Container */
.thermometer-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start; /* Keeps items at the top of the container */
  font-family: 'Arial', sans-serif;
  margin-top: 20px;
  height: 100%;  /* Makes the container flexible */
  padding: 10px;
}

/* Label at the top */
.thermometer-top-label {
  font-weight: bold;
  font-size: 18px;  /* Adjust font size */
  color: #333;
  margin-bottom: 10px;  /* Spacing between the top label and thermometer */
  text-align: center;
  text-transform: uppercase;
}

/* Thermometer Shape */
.thermometer {
  width: 60px;
  height: 100%;  /* Take up full height of the parent container */
  background: linear-gradient(to bottom, #ccc, #bbb);
  border-radius: 30px;
  border: 8px solid #333;
  position: relative;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  overflow: hidden; /* Ensures the inner thermometer doesn't overflow */
}

/* Thermometer Inner (Temperature Indicator) */
.thermometer-inner {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  background: linear-gradient(to top, #ff4500, #ff6347);
  border-radius: 20px;
  transition: height 0.4s ease-out;
  max-height: 100%; /* Prevents it from growing beyond the container */
}

/* Label Text (Temperature in °C) */
.thermometer-label {
  font-weight: bold;
  font-size: 16px;
  color: #333;
  margin-top: 10px;
  text-align: center;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}
</style>
