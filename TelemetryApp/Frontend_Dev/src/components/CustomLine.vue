<!-- Παρόμοια διαδικασία με το CustomBarChart -->

<template>
  <div class="flex w-full h-[500px] min-h-[350px] rounded bg-gray-50 dark:bg-gray-800 p-4 gap-4 overflow-x-auto">
    <!-- Chart Container -->
    <div :style="chartStyle" class="h-full min-w-0 relative">
      <canvas ref="chartCanvas" class="absolute inset-0 w-full h-full"></canvas>
    </div>

    <!-- Raw Values Box -->
    <div :style="boxStyle" class="overflow-y-auto bg-white dark:bg-gray-700 p-4 rounded shadow">
      <h3 class="font-bold mb-2 text-black dark:text-white">Raw Values</h3>
      <ul>
        <li
          v-for="(label, i) in datasetLabels"
          :key="i"
          class="mb-3 text-gray-800 dark:text-gray-300"
        >
          <strong
            class="block truncate max-w-[8rem] text-sm"
            :title="label"
          >
            {{ label }}:
          </strong>
          <span class="ml-1">
            {{ !isNaN(Number(items[i])) ? Number(items[i]).toFixed(precision) : '-' }}
          </span>
        </li>
      </ul>
    </div>
  </div>
</template>



<script lang="ts">
import { defineComponent, ref, onMounted, onBeforeUnmount, computed } from 'vue';
import Chart, { ChartConfiguration } from 'chart.js/auto';

export default defineComponent({
  name: "CustomLine",
  props: {
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
      default: 50
    },
    borderColor: {
    type: Array as () => string[],
      default: () => [
        'rgb(215,37,37)',
        'rgb(37, 99, 235)',
        'rgb(16, 185, 129)',
        'rgb(234, 179, 8)'
      ]
    },
    ystart: {
      type: Number,
      default: undefined
    },
    precision: {
      type: Number,
      default: 5
    },
    chartPercent: {
      type: Number,
      default: 70, // default to 80% chart, 20% box
      validator: (value: number) => value > 0 && value < 100
    }
  },
  setup(props) {
    const chartCanvas = ref<HTMLCanvasElement | null>(null);
    let chartInstance: Chart | null = null;
    let timer: ReturnType<typeof setInterval> | null = null;
    const maxDataPoints = props.max_dp; // 10 minutes at 1-second intervals

    const chartStyle = computed(() => ({
      flexGrow: 0,
      flexShrink: 0,
      flexBasis: `${props.chartPercent}%`
    }));

    const boxStyle = computed(() => ({
      flexGrow: 0,
      flexShrink: 1,
      flexBasis: `${100 - props.chartPercent}%`,
      minWidth: '50px' // Optional for safety on small values
    }));

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

      const data = {
        labels: [],
        datasets: props.datasetLabels.map((label, index) => ({
          label: label,
          data: [],
          borderColor: props.borderColor[index],
          backgroundColor: 'transparent',
        }))
      };

      const config: ChartConfiguration = {
        type: 'line',
        data: data,
        options: {
          animation: false,
          scales: {
            y: {
              stacked: false,
              ...(props.ystart !== undefined ? { min: props.ystart } : {})
            }
          },
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: true,
              position: 'top',
              labels: {
                boxWidth: 12,
                padding: 10,
                color: 'white'
              }
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
      chartStyle,
      boxStyle
    };
  }
});
</script>
