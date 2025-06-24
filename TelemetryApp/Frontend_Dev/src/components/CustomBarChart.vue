<!-- Εδώ φτιάχνουμε, όπως λέει και ο τίτλος ένα barchart -->
<template>
  <div class="flex items-center justify-center min-h-[350px] rounded bg-gray-50 dark:bg-gray-800">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<!-- Εδώ πάλι θα κάνουμε definecomponent -->
<script lang="ts">
import { defineComponent, ref, onMounted, onBeforeUnmount, toRefs } from 'vue';
import Chart, { ChartConfiguration } from 'chart.js/auto';

export default defineComponent({
  name: "CustomBarChart",
  //Εδώ είναι οι τιμές που θα χρειαστούμε
  props: {
    borderColor: {
      type: String,
      default: 'rgb(215,37,37)',
    },
    backgroundColor: {
      type: String,
      default: 'rgba(255, 255, 255, 0.6)',
    },
    title: {
      type: String,
      required: true
    },
    value: {
      type: Number,
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
    const chartCanvas = ref<HTMLCanvasElement | null>(null); //το Canvas είναι έτοιμο element που χρησιμοποιείται
    let chartInstance: Chart | null = null;
    let timer: ReturnType<typeof setInterval> | null = null;
    const maxDataPoints = props.max_dp;

    const updateChart = () => {

      //Αρχικά παίρνουμε την τωρινή στιγμή και ενημερωνόμαστε με την νέα τιμή του max_cell_voltage
      const currentTime = new Date().toLocaleTimeString(); //const εδώ σημαίνει ότι μπορούμε να αλλάξουμε τις τιμές μέσα αλλά όχι που δείχνει η μεταβλητη, πχ με ανάθεση ξανά
      const newValue = toRefs(props);

      if (newValue.value !== null && newValue.value !== undefined && chartInstance) {
        const labels = chartInstance.data.labels as string[];
        const data = chartInstance.data.datasets[0].data as number[];

        // Φροντίζουμε ο buffer να αφορά 2 λεπτά, όταν αυξηθεί παραπάνω κάνει shift και πετάει τις παλιές τιμές
        if (labels.length >= maxDataPoints) {
          labels.shift();
          data.shift();
        }

        //Εδώ προσθέτουμε τις καινούριες
        labels.push(currentTime);
        data.push(newValue.value.value);

        //Εδώ είναι για να αποθηκεύονται οι τιμές των chart όταν αλλάζουμε view
        // Save the current chart data to localStorage
        // localStorage.setItem('chartLabels', JSON.stringify(labels));
        // localStorage.setItem('chartData', JSON.stringify(data));

        // Dynamically adjust x-axis minimum and maximum values to center the chart
        // const startIndex = Math.max(0, labels.length - maxDataPoints);
        // const endIndex = labels.length - 1;
        // const visibleDataPoints = Math.min(maxDataPoints, labels.length);
        // const middleIndex = Math.floor(visibleDataPoints / 2);
        // const centerIndex = startIndex + middleIndex;
        // const centerLabel = labels[centerIndex];
        // const startLabel = labels[Math.max(0, centerIndex - middleIndex)];
        // const endLabel = labels[Math.min(labels.length - 1, centerIndex + middleIndex)];

        // chartInstance.options.scales!.x!.min = startLabel;
        // chartInstance.options.scales!.x!.max = endLabel;

        chartInstance.update('none');
      }
    };

    onMounted(() => {
      const canvas = chartCanvas.value;
      if (!canvas) return;

      const ctx = canvas.getContext('2d');
      if (!ctx) return;

      // Load the saved chart data from localStorage από πάνω
      const savedLabels = JSON.parse(localStorage.getItem('chartLabels') || '[]');
      const savedData = JSON.parse(localStorage.getItem('chartData') || '[]');

      //Κάνουμε configure τα δεδομένα του chart
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

      //Εδώ ορίζουμε πως θα μοιάζει το chart
      const config: ChartConfiguration = {
        type: 'bar',
        data: data,
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: false,
            }
          },
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
      timer = setInterval(updateChart, props.update_ms);
    });

    //Όταν φεύγουμε από την σελίδα το κλείνουμε για να αποφύγουμε memory leaks
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
      chartCanvas
    };
  }
});
</script>
