<template>
  <div class="flex items-center justify-center min-h-1/2 rounded bg-gray-50 dark:bg-gray-800">
  <Scatter :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import { Scatter } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  PointElement,
  LinearScale
} from 'chart.js'
import { watch, ref } from 'vue'

ChartJS.register(Title, Tooltip, Legend, PointElement, LinearScale)

const props = defineProps({
  point: {
    type: Object,
    required: true
  }
})

const chartData = ref({
  datasets: [{
    label: 'Single Point',
    data: [],
    backgroundColor: 'rgba(75, 192, 192, 1)',
    pointRadius: 6
  }]
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
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

watch(() => props.point, (newPoint) => {
  chartData.value.datasets[0].data = [newPoint]
}, { immediate: true })
</script>
