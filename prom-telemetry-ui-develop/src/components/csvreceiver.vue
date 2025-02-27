<template>
  <div class="p-0 mx-0 ml-40 mt-20 min-w-full overflow-y-auto">
    <form @submit.prevent="handleFileUpload">
      <input type="file" @change="handleFileChange" />
      <button type="submit">Upload File</button>
    </form>
    <div v-if="response">
      <h3>Upload Response:</h3>
      <pre>{{ JSON.stringify(response, null, 2) }}</pre>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const file = ref(null);
const response = ref(null);

const handleFileChange = (e) => {
  file.value = e.target.files[0];
};

const handleFileUpload = async () => {
  if (!file.value) {
    alert('Please select a file first!');
    return;
  }

  const formData = new FormData();
  formData.append('file', file.value);

  try {
    const res = await fetch('http://localhost:8000/api/v1/data_analysis/file_upload', {
      method: 'POST',
      body: formData,
    });

    if (!res.ok) {
      throw new Error('File upload failed');
    }

    const data = await res.json();
    response.value = data;
  } catch (error) {
    console.error('Error:', error);
  }
};
</script>

<style scoped>
/* Add your styles here */
</style>
