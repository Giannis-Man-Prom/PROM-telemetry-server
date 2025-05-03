<template>
    <div class="flex items-center justify-center min-h-1/2 rounded bg-gray-50 dark:bg-gray-800">
      <canvas ref="chartCanvas"></canvas>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, onMounted, onBeforeUnmount, watch } from 'vue';
  import Chart, { ChartConfiguration } from 'chart.js/auto';
  import { linechartItems } from "../types/live_telemetry.ts";
  
  export default defineComponent({
    name: "CustomLineComponent",
    props: {
      borderColor: {
        type: String,
        default: 'rgb(215,37,37)',
      },
      backgroundColor: {
        type: String,
        default: 'rgba(255, 255, 255, 0.6)',
      },
      labels: {
        type: Array as () => string[],
        required: true
      },
      items: {
        type: Object as () => linechartItems,
        required: true
      },
      title: {
        type: String,
        required: true
      }
    },
    setup(props) {
      const chartCanvas = ref<HTMLCanvasElement | null>(null);
      let chartInstance: Chart | null = null;
      const maxDataPoints = 60 * 10; // 10 minutes at 1-second intervals
  
      onMounted(() => {
        const canvas = chartCanvas.value;
        if (!canvas) return;
  
        const ctx = canvas.getContext('2d');
        if (!ctx) return;
  
        const data = {
          labels: [],
          datasets: [
            {
              label: props.title,
              data: [],
              borderColor: props.borderColor,
              backgroundColor: props.backgroundColor,
            }
          ],
        };
  
        const config: ChartConfiguration = {
          type: 'line',
          data: data,
          options: {
            animation: false,
            scales: {
              y: {
                stacked: true
              }
            },
            responsive: true,
            plugins: {
              legend: {
                display: false,
              },
              title: {
                display: true,
                text: props.title
              }
            }
          },
        };
  
        chartInstance = new Chart(ctx, config);
      });
  
      watch(
        () => props.items,
        (newVal: linechartItems) => {
          if (!chartInstance || !newVal || newVal.value.length === 0) return;
  
          const currentTime = new Date().toLocaleTimeString();
          const labels = chartInstance.data.labels as string[];
          const data = chartInstance.data.datasets[0].data as number[];
  
          if (labels.length >= maxDataPoints) {
            labels.shift();
            data.shift();
          }
  
          labels.push(currentTime);
          data.push(newVal.value[0]); // Adjust according to the structure of `linechartItems`
  
          chartInstance.update();
        },
        { deep: true } // if `items` is an array of objects or reactive deeply
      );
  
      onBeforeUnmount(() => {
        if (chartInstance) {
          chartInstance.destroy();
          chartInstance = null;
        }
      });
  
      return {
        chartCanvas,
      };
    }
  });
  </script>
  