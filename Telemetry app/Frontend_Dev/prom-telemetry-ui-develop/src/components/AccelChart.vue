<template>
    <div class="flex items-start justify-center min-h-1/2 rounded bg-gray-50 dark:bg-gray-800">
      <div>
        <h3>Current Acceleration</h3>
        <canvas ref="scatterChart" width="400" height="400"></canvas>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, watch, onMounted } from 'vue';
  import { Chart } from 'chart.js';
  
  export default defineComponent({
    name: 'CurrentAccelerationScatterPlot',
    props: {
      min: {
        type: Number,
        default: -10,
      },
      max: {
        type: Number,
        default: 10,
      },
      xAcceleration: {
        type: Number,
        required: true,
      },
      yAcceleration: {
        type: Number,
        required: true,
      },
    },
    setup(props) {
      const scatterChart = ref(null);
      const chartData = ref<{ x: number; y: number }[]>([
        { x: props.xAcceleration, y: props.yAcceleration },
      ]);
  
      let chartInstance: any = null;
  
      const chartOptions = {
        responsive: true,
        scales: {
          x: {
            type: 'linear',
            position: 'bottom',
            title: {
              display: true,
              text: 'X Acceleration (m/s²)',
            },
            min: props.min,
            max: props.max,
          },
          y: {
            type: 'linear',
            title: {
              display: true,
              text: 'Y Acceleration (m/s²)',
            },
            min: props.min,
            max: props.max,
          },
        },
      };
  
      const updateChartData = () => {
        // Update the single data point with the new acceleration values
        chartData.value[0] = { x: props.xAcceleration, y: props.yAcceleration };
  
        // Update the chart with the new data
        chartInstance.data.datasets[0].data = chartData.value;
        chartInstance.update();
      };
  
      onMounted(() => {
        const ctx = scatterChart.value.getContext('2d');
        chartInstance = new Chart(ctx, {
          type: 'scatter',
          data: {
            datasets: [
              {
                label: 'Current Acceleration',
                data: chartData.value,
                backgroundColor: 'rgba(0, 123, 255, 0.5)',
                borderColor: 'rgba(0, 123, 255, 1)',
                borderWidth: 1,
                pointRadius: 5,
              },
            ],
          }
        });
      });
  
      // Watch for updates to xAcceleration and yAcceleration and update the chart data
      watch(
        () => [props.xAcceleration, props.yAcceleration],
        () => {
          updateChartData();
        },
        { immediate: true }
      );
  
      return {
        scatterChart,
      };
    },
  });
  </script>
  
  <style scoped>
  canvas {
    border: 1px solid #ccc;
    background-color: #f9f9f9;
  }
  </style>
  