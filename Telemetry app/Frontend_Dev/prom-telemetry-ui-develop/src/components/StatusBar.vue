<template>
  <header>
    <nav class="ml-35 bg-white border-gray-200 px-4 lg:px-6 py-5 dark:bg-gray-800 w-full fixed top-0 left-0 z-50">
      <div class="flex justify-between items-center mx-auto max-w-screen-xl">
        <div class="hidden lg:flex lg:items-center">
          <button
              class="still block py-2 pr-4 pl-3 text-white rounded bg-primary-700 lg:bg-transparent lg:text-primary-700 lg:p-0 dark:text-white hover:bg-primary-600 lg:hover:bg-transparent lg:hover:text-primary-600 dark:hover:text-gray-300"
              :class="{ 'bg-green-500': logging }"
              @click="toggleLogging"
          >
            {{ logging ? 'Logging Active' : 'Start Logging' }}
          </button>
          <ul class="flex flex-col mt-4 font-medium lg:flex-row lg:space-x-8 lg:mt-0">
            <li v-for="(item, index) in items" :key="index" class="inline-block">
              <div v-if="item.label">
                <a
                    href="#"
                    class="items-left ml-20 block py-2 pr-4 pl-3 text-white rounded bg-primary-700 lg:bg-transparent lg:text-primary-700 lg:p-0 dark:text-white text-left w-full"
                    aria-current="page"
                >
                  {{ item.label[0] }}<span v-if="item.value">: {{ item.value[0] }}</span>
                </a>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </header>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { post_start_logging } from '../services/live_telemetry.services.js';
import { sidebarItems } from '../types/live_telemetry.ts';

export default defineComponent({
  name: 'StatusBar',
  data() {
    return {
      logging: false, // Track logging state
    };
  },
  props: {
    items: Array as () => sidebarItems[],
  },
  methods: {
    toggleLogging() {
      this.logging = !this.logging;

      post_start_logging().then((res) => {
        console.log(res);
      });

    },
  },
});
</script>

<style scoped>
/* Add your scoped styles here */
</style>
