<script>
import { defineComponent, ref, watch } from 'vue';
import Scatter from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  PointElement,
  LinearScale
} from 'chart.js';

// Register chart.js components
ChartJS.register(Title, Tooltip, Legend, PointElement, LinearScale);

export default defineComponent({
  name: 'SPScatterChart',
  props: {
    point: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      chartData: ref({
        datasets: [{
          label: 'Single Point',
          data: [],
          backgroundColor: 'rgba(75, 192, 192, 1)',
          pointRadius: 6
        }]
      }),
      chartOptions: {
        responsive: true,
        maintainAspectRatio: true,
        scales: {
          x: {
            type: 'linear',
            position: 'bottom',
            min: -10,
            max: 10
          },
          y: {
            min: -10,
            max: 10
          }
        }
      }
    };
  },
  watch: {
    point(newPoint) {
      // Update the point directly in the data array
      this.chartData.datasets[0].data = [{ x: newPoint.x, y: newPoint.y }];
    }
  },
  created() {
    // For immediate update of the chart
    this.chartData.datasets[0].data = [{ x: this.point.x, y: this.point.y }];
  }
});
</script>


<template>
  <div class="flex items-center justify-center min-h-1/2 rounded bg-gray-50 dark:bg-gray-800">
    <Scatter :data="chartData" :options="chartOptions" />
  </div>
</template>