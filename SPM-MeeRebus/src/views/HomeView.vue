<script setup>
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios'; 
import Calendar from '@/components/Calendar.vue';
import TheWelcome from '../components/TheWelcome.vue';

const router = useRouter(); 


</script>

<template>
  <div>
    <Calendar />
  </div>
</template>