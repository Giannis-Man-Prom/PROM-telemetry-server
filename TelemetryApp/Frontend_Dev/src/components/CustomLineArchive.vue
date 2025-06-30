<!-- Παρόμοια διαδικασία με το CustomBarChart -->

<template>
  <div class="flex items-center justify-center min-h-[350px] rounded bg-gray-50 dark:bg-gray-800 ">
    <canvas ref="chartCanvas">
    </canvas>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, onBeforeUnmount, toRefs } from 'vue';
import Chart, { ChartConfiguration } from 'chart.js/auto';

export default defineComponent({
  name: "CustomLineArchive",
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
      type: String,
      required: true
    },
    items: {
      type: Number,
      required: true
    },
    title: {
      type: String,
      required: true
    },
    update_ms: {
      type: Number,
      default: 1000
    },
    max_dp: {
      type: Number,
      default: 100
    }
  },
  setup(props) {
    const chartCanvas = ref<HTMLCanvasElement | null>(null);
    let chartInstance: Chart | null = null;
    let timer: ReturnType<typeof setInterval> | null = null;
    const maxDataPoints = props.max_dp; // 10 minutes at 1-second intervals

    const updateChart = () => {
      const currentTime = new Date().toLocaleTimeString();
      const items = toRefs(props);

      if (chartInstance) {
        const labels = chartInstance.data.labels as string[];
        const data = chartInstance.data.datasets[0].data as number[];

        // Maintain a buffer of data points for the last 10 minutes
        if (labels.length >= maxDataPoints) {
          labels.shift();
          data.shift();
        }

        labels.push(currentTime);
        data.push(items.items.value); // Assuming items is an array and accessing the first item's value1

        chartInstance.update();
      }
    };

    onMounted(() => {
      const canvas = chartCanvas.value;
      if (!canvas) return;

      const ctx = canvas.getContext('2d');
      if (!ctx) return;

      localStorage.removeItem('lineChartLabels');
      localStorage.removeItem('lineChartData');

      const savedLabels = JSON.parse(localStorage.getItem('lineChartLabels') || '[]');
      const savedData = JSON.parse(localStorage.getItem('lineChartData') || '[]');

      const data = {
        labels: savedLabels,
        datasets: [
          {
            label: 'Max Cell Voltage',
            data: savedData,
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
              position: 'top',
            },
            title: {
              display: true,
              text: props.title
            }
          }
        },
      };

      chartInstance = new Chart(ctx, config);
      timer = setInterval(updateChart, props.update_ms); // Update every second
    });

    onBeforeUnmount(() => {
      if (timer) {
        clearInterval(timer);
      }
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
