<template>
<!--  <div class="flex items-center justify-center rounded bg-gray-50 dark:bg-gray-800">-->
<!--    <div class="grid grid-cols-4 gap-8">-->
<!--      <div v-for="(variable, index) in variables" :key="index" class="relative">-->
<!--        <div :class="{ 'bg-green-500': variable, 'bg-red-500': !variable }" class="w-32 h-24 flex items-center justify-center rounded-lg border-2 border-gray-400 dark:border-gray-600">-->
<!--          <div class="absolute top-0 left-0 w-full h-full flex items-center justify-center">-->
<!--            {{ variableNames[index] }}-->
<!--          </div>-->
<!--        </div>-->
<!--      </div>-->
<!--    </div>-->
<!--  </div>-->
  <div class="flex items-center justify-center rounded bg-gray-50 dark:bg-gray-800">
    <div class="grid grid-cols-4 gap-8">

      {{text}}

    </div>
  </div>


</template>

<script>
export default {
  props: {
    text: {
      type: String,
      default: () => ('den exw text'),
    }
  },
  data() {
    return {
      variables: [
        true,  // BSPD_OK
        false, // ASB_OK
        true,  // IMD_OK
        false, // AMS_OK
        true,  // BOTS_SD
        false, // COCKPIT_SD
        true,  // INERTIA_SD
        false, // SD_CLOSED
        true,  // L_SD_CLOSED
        false, // R_SD_CLOSED
        true,  // AIR_M_STATE
        false  // AIR_P_STATE
      ],
      variableNames: [
        'BSPD_OK', 'ASB_OK', 'IMD_OK', 'AMS_OK', 'BOTS_SD', 'COCKPIT_SD',
        'INERTIA_SD', 'SD_CLOSED', 'L_SD_CLOSED', 'R_SD_CLOSED', 'AIR_M_STATE', 'AIR_P_STATE'
      ]
    };
  }
}
</script>

