<template>
    <div class="container d-flex justify-content-center align-items-center" style="height: 100vh;">
        <div class="col-md-4">
            <h2 class="text-center">Please key in your Employee ID to log in</h2>
            <!-- submit.prevent just makes sure they can't login without inputting anything. Won't show alert like invalid ID though, bootstrap built in popup exists -->
            <form @submit.prevent="handleLogin">
                <div class="form-group">
                    <label for="empId">Employee ID:</label>
                    <input type="number" id="empId" v-model="empId" class="form-control" required>
                </div>
                <button type="submit" class="btn btn-primary btn-block">Login</button>
            </form>
            <!-- Error alert using Bootstrap if invalid employee ID submitted -->
            <div v-if="errorMessage" class="alert alert-danger mt-3" role="alert">
                {{ errorMessage }}
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'LoginView',
    data() {
        return {
            empId: '',
            errorMessage: ''
        }
    },
    methods: {
        async handleLogin() {
            this.errorMessage = ''; 
            const isValid = await this.checkValidID();

            if (isValid) {
                console.log('Logged in with Employee ID:', this.empId);
                localStorage.setItem('employeeId', this.empId);
                // await this.getArrangementData(); 
                this.$router.push('/home');
            } else {
                this.errorMessage = 'Invalid Employee ID or not authorized to log in from this location. Please try again.';
            }
        },
        async checkValidID() {
            try {
                const response = await axios.get(`http://127.0.0.1:5000/employee/${this.empId}`);
                localStorage.setItem('employeeData', JSON.stringify(response.data));
                console.log(response.data);
                
                if (response.data.dept == "HR" || response.data.position == "MD" || response.data.position == "Director") {
                    // Only if HR, get all the arrangement data
                    await this.getArrangementData();
                }
                
                return true; // Return true if the request was successful
            } catch (error) {
                console.error(error);
                // Check if the error response contains a specific message
                if (error.response && error.response.data && error.response.data.error) {
                    this.errorMessage = error.response.data.error;
                } else {
                    this.errorMessage = 'An unexpected error occurred. Please try again later.';
                }
                return false; 
            }
        },
        async getArrangementData() {
            try {
                const response = await axios.get('http://127.0.0.1:5000/arrangement');
                localStorage.setItem('arrangement', JSON.stringify(response.data));
                console.log(response.data);  
            } catch (error) {
                console.log(error);
            }
        }
    }
}
</script>

<style scoped>
/* Add any custom styles here */
</style>