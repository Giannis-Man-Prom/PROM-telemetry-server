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
        min: {
            type: Number,
            default: 0,
        },
        max: {
            type: Number,
            default: 100,
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
        },
        plotOptions: {
            radialBar: {
            startAngle: -120,
            endAngle: 120,
            hollow: {
                size: '65%',
            },
            track: {
                background: '#f0f0f0',
                strokeWidth: '100%',
                margin: 10,
            },
            dataLabels: {
                name: {
                offsetY: -10,
                fontSize: '16px',
                color: '#f00',
                },
                value: {
                    fontSize: '22px',
                    offsetY: 10,
                    color: '#fff',
                    formatter: function () {
                        return `${actualValue.value}`;
                    }
                }
            }
            }
        },
        labels: [props.title],
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
  