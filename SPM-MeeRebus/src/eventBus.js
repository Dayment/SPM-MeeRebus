import { reactive } from 'vue';

const eventBus = reactive({
  isLoggedIn: false,
  isHR: false,
  isDir: false,
  isManager: false
});
export default eventBus;

// Just testing something out here, feel free to ignore it