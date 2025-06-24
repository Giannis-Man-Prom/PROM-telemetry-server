<script setup>
import { ref, watch, defineProps } from 'vue';
import { Scatter } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  PointElement,
  LinearScale
} from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, PointElement, LinearScale);

// Define props
const props = defineProps({
  point: {
    type: Object,
    required: true
  },
  title: {
    type: String,
    required: true
  }
});

// Chart data & options
const chartData = ref({
  datasets: [{
    label: props.title,
    data: [],
    backgroundColor: 'rgba(75, 192, 192, 1)',
    pointRadius: 6
  }]
});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: true,
  aspectRatio: 1,
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
};

// Watch the point prop
watch(() => props.point, (newPoint) => {
  if (newPoint && typeof newPoint.x === 'number' && typeof newPoint.y === 'number') {
    chartData.value = {
      datasets: [{
        label: props.title,
        data: [{ x: newPoint.x, y: newPoint.y }],
        backgroundColor: 'rgba(75, 192, 192, 1)',
        pointRadius: 6
      }]
    };
  }
}, { immediate: true });
</script>

<template>
  <div class="flex items-start justify-center min-h-[350px] rounded bg-gray-50 dark:bg-gray-800 p-4 space-x-6 h-[500px]"> <!-- set fixed height -->
    
    <!-- Scatter Chart Container -->
    <div class="flex-1 h-full">
      <div class="h-[80%]"> <!-- use % height relative to parent -->
        <Scatter :data="chartData" :options="chartOptions" />
      </div>
    </div>

    <!-- Buttons for showing X and Y -->
    <div class="flex flex-col space-y-4">
      <button class="bg-blue-500 text-white px-4 py-2 rounded">
        X Value: {{ props.point.x }}
      </button>
      <button class="bg-green-500 text-white px-4 py-2 rounded">
        Y Value: {{ props.point.y }}
      </button>
    </div>

  </div>
</template>
