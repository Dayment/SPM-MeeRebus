<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">WFH Management System</a>
        <button
          class="navbar-toggler"
          type="button"
          data-toggle="collapse"
          data-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse " id="navbarNav">
          <ul class="navbar-nav">
            <li class="nav-item">
              <a class="nav-link" href="/home">Own Schedule</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/team">Team Schedule</a>
            </li>
            <li class="nav-item" v-if="isHR">
              <a class="nav-link" href="/company">Company Schedule</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/apply">Apply For Arrangement</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </template>
  
  <script>
export default {
  name: 'NavbarComponent',
  data() {
    return {
      isHR: false,
    };
  },
  mounted() {
    this.checkEmployeeRole();
  },
  methods: {
    async checkEmployeeRole() {
      try {
        const employeeData = JSON.parse(localStorage.getItem('employeeData'));
        if (employeeData && employeeData.dept === 'HR') {
          this.isHR = true;
        }
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>