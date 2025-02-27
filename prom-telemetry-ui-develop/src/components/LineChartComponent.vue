<script lang="ts">
import {defineComponent, ref} from 'vue'
import Chart from 'chart.js/auto'
import {ChartConfiguration} from "chart.js";

export default defineComponent({
  name: "LineChartComponent",
  props: {
    borderColor: {
      type: String,
      default: () => ('rgb(215,37,37)'),
    },
    backgroundColor: {
      type: String,
      default: () => ('rgba(255, 255, 255, 0.6)'),
    },
    labels: {
      type: [],
      required: true
    },
    chart_data: {
      type: [],
      required: true
    }
  },
  components: {

  },
  data() {
    return {
    };
  },
  mounted() {

    const chart = ref<Chart | null>(null);

    const data = {
      labels: this.labels,
      datasets: [
        {
          label: 'Dataset 1',
          data: this.chart_data,
          borderColor: this.borderColor,
          backgroundColor: this.backgroundColor,
        }
      ]
    };

    const config = {
      type: 'line',
      data: data,
      options: {
        responsive: true,
        plugins: {
          legend: {
            display: false,
            position: 'top',
          },
          title: {
            display: false,
            text: 'Chart.js Line Chart'
          }
        }
      },
    } as ChartConfiguration

    if (chart.value) {
      chart.value.destroy(); // Destroy the previous chart if it exists
    }

    chart.value = new Chart(this.$refs.chart.getContext('2d'), config) as never as any;

  },
  methods: {


  }
})
</script>


<template>

  <div class="flex items-center justify-center min-h-1/2 rounded bg-gray-50 dark:bg-gray-800 ">
    <!-- Put canvas tag here. -->
    <canvas ref="chart"></canvas>
  </div>
</template>