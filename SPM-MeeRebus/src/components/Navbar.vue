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
          <div class="collapse navbar-collapse" id="navbarNav">
              <ul class="navbar-nav" v-if="eventBus.isLoggedIn">
                  <li class="nav-item">
                      <a class="nav-link" href="/home">Own Schedule</a>
                  </li>
                  <li class="nav-item">
                      <a class="nav-link" href="/team">Team Schedule</a>
                  </li>
                  <li class="nav-item" v-if="showDepartmentNav">
                      <a class="nav-link" href="/dept">Department Schedule</a>
                  </li>
                  <li class="nav-item" v-if="showCompanyNav">
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
import eventBus from '../eventBus';
export default {
  name: 'NavbarComponent',
  data() {
    const isDir = localStorage.getItem('isDir') == 'true';
    const isHR = localStorage.getItem('isHR') == 'true';

      return {
          showDepartmentNav: eventBus.isDir || isDir,
          showCompanyNav: eventBus.isHR || isHR,
      };
  },
  mounted() {
      this.checkUserRole();
      console.log(this.showDepartmentNav)
      console.log("HR:", this.showCompanyNav)
  },
  beforeUpdate(){
    this.checkUserRole();
  },
  updated(){
    this.checkUserRole();
  },
  methods: {
      checkUserRole() {
          const isDir = localStorage.getItem('isDir') == 'true';
          const isHR = localStorage.getItem('isHR') == 'true';
          this.showDepartmentNav = eventBus.isDir || isDir;
          this.showCompanyNav = eventBus.isHR || isHR;
      }
  },
  setup() {
      return { eventBus };
  }
};
</script>