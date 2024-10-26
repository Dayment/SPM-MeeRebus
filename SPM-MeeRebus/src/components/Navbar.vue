<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid ">
          <a class="navbar-brand" href="/home">WFH Management System</a>
          <button
              class="navbar-toggler"
              type="button"
              data-bs-toggle="collapse"
              data-bs-target="#navbarNav"
              aria-controls="navbarNav"
              aria-expanded="false"
              aria-label="Toggle navigation"
          >
              <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarNav">
              <ul class="navbar-nav" v-if="eventBus.isLoggedIn">
                <li class="nav-item dropdown">
                  <button class="btn dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
                    Schedule
                  </button>
                  <ul class="dropdown-menu">
                    <li><a class="dropdown-item" href="/home">Own Schedule</a></li>
                    <li><a class="dropdown-item" href="/team">Team Schedule</a></li>
                  </ul>
                </li>
                  <!-- <li class="nav-item">
                      <a class="nav-link" href="/home">Own Schedule</a>
                  </li>
                  <li class="nav-item">
                      <a class="nav-link" href="/team">Team Schedule</a>
                  </li> --> 

                  <li class="nav-item dropdown" v-if="showTeamDropdown">
                    <button class="btn dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
                      Applications
                    </button>
                    <ul class="dropdown-menu">
                      <li><a class="dropdown-item" href="/history">Application History</a></li>
                      <li><a class="dropdown-item" href="/managerapproval">WFH Approval</a></li>
                    </ul>
                  </li>
                  <li class="nav-item" v-else>
                    <a class="nav-link" href="/history">Application History</a>
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
                  <li class="nav-item" v-if="showEvents">
                      <a class="nav-link" href="/events">Apply For Events</a>
                  </li>
              </ul>
              <div class="logout-container" v-if="eventBus.isLoggedIn">
                <a href="/" @click="logout()" class="logout-link">
                  <i class="bi bi-box-arrow-right"></i> Logout
                </a>
              </div>

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
    const isManager = localStorage.getItem('isManager') == 'true';

      return {
          showDepartmentNav: eventBus.isDir || isDir,
          showCompanyNav: eventBus.isHR || isHR,
          showEvents: eventBus.isHR || isHR,
          showTeamDropdown: eventBus.isManager || isManager
      };
  },
  mounted() {
      this.checkUserRole();
      console.log(this.showDepartmentNav)
      console.log("HR:", this.showCompanyNav)
      console.log("Man:", this.showTeamDropdown)
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
          const isManager = localStorage.getItem('isManager') == 'true';
          
          this.showDepartmentNav = eventBus.isDir || isDir;
          this.showCompanyNav = eventBus.isHR || isHR;
          this.showEvents = eventBus.isHR || isHR;
          this.showTeamDropdown = eventBus.isManager || isManager;
        

      },
      logout(){
        // Clears EVERYTHING from localstorage
        localStorage.clear()
      }
  },
  setup() {
      return { eventBus };
  }
};
</script>

<style scoped>
.navbar {
  font-size: 0.9rem;
}
.logout-container {
  margin-left: auto;
}
</style>