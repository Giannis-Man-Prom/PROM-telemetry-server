<template>
    <div class="flex items-center justify-center min-h-screen bg-gray-50 dark:bg-gray-800">
        <div class="w-full h-full flex flex-col items-center justify-center text-center"> <!-- Center the whole content (title, bar, value) -->
        <!-- Title above the bar -->
        <div class="title text-lg font-semibold mb-2">
          {{ title }}
        </div>
        
        <!-- The bar wrapper -->
        <div class="bar-wrapper">
          <!-- Main bar (background bar) -->
          <div class="bar-main"></div>
  
          <div
            class="bar-left"
            :style="{
              width: `${barWidthLeft}%`,  /* Use the absolute value for width */
              right: `50%`,  /* Position it at the center */
            }"
          ></div>
          
          <!-- Right inner bar for positive values -->
          <div
            class="bar-right"
            :style="{
              width: `${barWidthRight}%`,
              left: `50%`  /* Position it at the center */
            }"
          ></div>
        </div>
      
        <!-- Value indication below the bar -->
        <div class="value-indicator mt-2 text-sm text-gray-600 dark:text-gray-300">
          Value: {{ value }}
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { defineComponent, ref, watch } from 'vue';
  
  export default defineComponent({
    name: 'HorizontalBar',
    props: {
      value: {
        type: Number,
        required: true,
      },
      title: {
        type: String,
        default: 'Horizontal Bar',
      },
      range: {
        type: Number,
        default: 100
      }
    },
    setup(props) {
      const barWidthLeft = ref(0);  // Store width for the left bar (negative values)
      const barWidthRight = ref(0); // Store width for the right bar (positive values)
    
      // Watch the 'value' prop and update the bar widths based on the value
      watch(
        () => props.value,
        (newValue) => {
          // Clamp the value between -100 and 100
          if (newValue != undefined) {
            const clampedValue = Math.min(Math.max(newValue/2, -props.range), props.range);
    
            // Based on the sign of the clamped value, update the bar widths
            if (clampedValue < 0) {
              barWidthLeft.value = Math.abs(clampedValue);  // Left bar for negative values
              barWidthRight.value = 0;  // Reset right bar for negative values
              console.log("Left bar width (negative):", barWidthLeft.value);
            } else {
              barWidthLeft.value = 0;  // Reset left bar for positive values
              barWidthRight.value = clampedValue;  // Right bar for positive values
            }
          }
        },
        { immediate: true }
      );
    
      return { barWidthLeft, barWidthRight, title: props.title };
    },
  });
  </script>
  
  <style scoped>
  .bar-wrapper {
    width: 80%; /* Set the bar width to 80% of its container */
    height: 20px; /* Set a fixed height for the bar */
    background-color: #e0e0e0;
    border-radius: 10px;
    overflow: hidden;
    position: relative;
    margin: 0 auto; /* Center the bar wrapper horizontally */
  }
  
  .bar-left, .bar-right {
    height: 100%;
    position: absolute;
    top: 0;
    transition: width 0.3s ease-in-out; /* Smooth transition */
    border-radius: 10px; /* Round the edges of the bars */
  }
  
  .bar-left {
    background-color: #f44336; /* Red for negative values */
    right: 50%; /* Position the left bar at the center and grow left */
  }
  
  .bar-right {
    background-color: #4caf50; /* Green for positive values */
    left: 50%; /* Position the right bar at the center and grow right */
  }
  
  .bar-main {
    background-color: #e0e0e0; /* Background color for the main bar */
    height: 100%;
    position: absolute;
    left: 0;
    right: 0;
    top: 0;
  }
  
  .title {
    font-size: 1.25rem; /* Larger font size for the title */
    font-weight: bold;
    color: #333;
  }
  
  .value-indicator {
    font-size: 0.875rem; /* Smaller font size for the value indication */
    color: #666;
  }
  
  .flex {
    display: flex;
  }
  
  .items-center {
    align-items: center;
  }
  
  .justify-center {
    justify-content: center;
  }
  
  .min-h-screen {
    min-height: 100%; /* Full height of the viewport */
  }
  
  .bg-gray-50 {
    background-color: #fafafa;
  }
  
  .dark\:bg-gray-800 {
    background-color: #1f2937; /* Dark mode background */
  }
  </style>
  