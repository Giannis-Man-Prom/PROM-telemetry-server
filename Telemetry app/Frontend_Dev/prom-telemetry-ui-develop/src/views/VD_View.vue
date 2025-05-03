<!-- Εδώ έχουμε το VD View που δεν είναι developped και απλά δείχνει άκυρα δεδομένα -->
<template>
  <!--&lt;!&ndash;  Here we have the sidebar component that we need for navigation and features&ndash;&gt;-->
  <div class="p-6 mx-2 min-w-full">
    <div class="grid grid-cols-2 grid-rows-2 gap-x-8 gap-y-4 h-screen">
      <CustomBarChart :labels="[]" dataKey="max_cell_voltage" borderColor="green" backgroundColor="rgba(0,255,0,0.3)"/>

    </div>
  </div>

</template>

<script lang="ts">
import {defineComponent} from "vue"
import CustomBarChart from "../components/CustomBarChart.vue"
import SideBar from "../components/SideBar.vue";


export default defineComponent({
  name: "VD_View",
  components: {
    CustomBarChart,
    SideBar
  },
  data() {
    return {

    };
  },
  mounted() {

  },
  methods: {

  }
})
</script>