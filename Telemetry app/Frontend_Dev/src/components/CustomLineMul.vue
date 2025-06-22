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
  name: "CustomLineMul",
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
      type: Array as () => number[],
      required: true
    },
    datasetLabels: {
      type: Array as () => string[],
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

      if (chartInstance) {
        const labels = chartInstance.data.labels as string[];
        if (labels.length >= maxDataPoints) labels.shift();
        labels.push(currentTime);

        chartInstance.data.datasets.forEach((dataset, i) => {
          const data = dataset.data as number[];
          if (data.length >= maxDataPoints) data.shift();
          data.push(props.items[i]); // Push corresponding value
        });

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
        datasets: props.datasetLabels.map((label, index) => ({
          label: label,
          data: savedData[index] || [],
          borderColor: props.borderColor,
          backgroundColor: props.backgroundColor,
        }))
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
