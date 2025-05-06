<template>
    <div class="thermometer-container">
      <div class="thermometer">
        <div class="thermometer-inner" :style="{ height: `${temperature}%` }"></div>
      </div>
      <div class="thermometer-label">{{ temperature }}°C</div>
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
    justify-content: center;
    font-family: 'Arial', sans-serif;
    margin-top: 20px;
  }
  
  /* Thermometer Shape */
  .thermometer {
    width: 60px;
    height: 300px;
    background: linear-gradient(to bottom, #ccc, #bbb);
    border-radius: 30px;
    border: 8px solid #333;
    position: relative;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
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
  