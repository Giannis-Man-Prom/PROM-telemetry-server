<!-- Εδώ έχουμε το VD View που δεν είναι developped και απλά δείχνει άκυρα δεδομένα -->
<template>
  <!--&lt;!&ndash;  Here we have the sidebar component that we need for navigation and features&ndash;&gt;-->
  <div class="p-6 mx-2 min-w-full">
    <div class="grid grid-cols-2 grid-rows-2 gap-x-8 gap-y-4 h-screen">

      <LineChartComponent :labels="['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange']" :chart_data="[12, 19, 3, 5, 2, 3]"/>
      <LineChartComponent :labels="['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange']" :chart_data="[12, 19, 3, 5, 2, 3]"/>
      <LineChartComponent :labels="['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange']" :chart_data="[12, 19, 3, 5, 2, 3]"/>
      <StatusListComponent/>

    </div>
  </div>

</template>

<script lang="ts">
import {defineComponent} from "vue"
import SideBar from "../components/SideBar.vue";
import LineChartComponent from "@/components/LineChartComponent.vue";
import StatusListComponent from "@/components/StatusListComponent.vue";


export default defineComponent({
  name: "Dashboard",
  components: {
    SideBar,
    LineChartComponent,
    StatusListComponent
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