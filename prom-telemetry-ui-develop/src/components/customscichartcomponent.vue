<template>
    <div class="sci-chart-container">
        <h1>SciChart - Vue Integration</h1>
        <div id="scichart-root" style="width: 800px; height: 500px; margin: auto;"></div>
    </div>
</template>

<script>
import { defineComponent } from "vue";
import { SciChartSurface } from "scichart"; // Import necessary SciChart modules

async function initSciChart() {
    // ... (Your existing initSciChart implementation)
}

export default defineComponent({
    async mounted() {
        const { sciChartSurface } = await initSciChart();
        console.log("SciChart surface created successfully!");
    },
    name: "customscichartcomponent",
});
</script>

<style scoped>
.sci-chart-container {
    text-align: center;
    padding: 20px;
}
</style>
