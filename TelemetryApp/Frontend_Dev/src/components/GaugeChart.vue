<template>
    <div class="flex items-start justify-center min-h-[350px] rounded bg-gray-50 dark:bg-gray-800 ">
        <apexchart 
            type="radialBar" 
            :options="chartOptions" 
            :series="series" 
            width="125%" 
            height="100%"
        />
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, watch, onMounted, onBeforeUnmount } from 'vue';
  import VueApexCharts from "vue3-apexcharts";
  
  export default defineComponent({
    name: "CustomGauge",
    props: {
        items: {
            type: Number,
            required: true
        },
        title: {
            type: String,
            required: true
        },
        min: {
            type: Number,
            default: 0,
        },
        max: {
            type: Number,
            default: 100,
        },
        precision: {
            type: Number,
            default: 5,
        }
    },
    components: {
      apexchart: VueApexCharts,
    },
    setup(props) {
        const series = ref<number[]>([0]);
        const actualValue = ref<number>(0);  // new ref to store raw value
        const chartOptions = ref({
        chart: {
            type: 'radialBar',
            dropShadow: {
            enabled: true,
            top: 5,
            left: 0,
            blur: 5,
            opacity: 0.1,
            color: '#white',
            },
        },
        plotOptions: {
            radialBar: {
            startAngle: -135,
            endAngle: 135,
            hollow: {
                size: '60%',
                background: 'transparent',
            },
            track: {
                background: '#e0e0e0',
                strokeWidth: '100%',
            },
            dataLabels: {
                name: {
                show: true,
                offsetY: -20,
                fontSize: '18px',
                fontWeight: '600',
                color: 'red',
                },
                value: {
                show: true,
                fontSize: '28px',
                fontWeight: '700',
                color: 'white',
                offsetY: 10,
                formatter: function () {
                    return actualValue.value.toFixed(props.precision);
                }
                }
            },
            // Make the bar ends rounded
            stroke: {
                lineCap: 'round',
            },
            },
        },
        colors: ['#4caf50'], // 🟢 green
        labels: [props.title],
        // Responsive adjustments
        responsive: [{
            breakpoint: 480,
            options: {
            chart: {
                width: 280
            },
            legend: {
                position: 'bottom'
            }
            }
        }],
        });

        watch(() => props.items, (newItems: number) => {
            if (typeof newItems === 'number') {
            actualValue.value = newItems;  // store raw value
            const normalized = ((newItems - props.min) / (props.max - props.min)) * 100;
            series.value = [Math.max(0, Math.min(100, normalized))];  // clamp only for chart fill
            }
        }, { immediate: true });
  
      return {
        series,
        chartOptions
      };
    }
  });
  </script>
  