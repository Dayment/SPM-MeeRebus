<!-- <template>
    <div class="login-container">
        <h2>Login</h2>
        <form @submit.prevent="handleLogin">
            <div class="form-group">
            <label for="empId">Username:</label>
            <input type="text" id="empId" v-model="empId" required>
            </div>
            <button type="submit" class="login-btn">Login</button>
        </form>
    </div>
</template> -->

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
                this.$router.push('/home');
            } else {
                this.errorMessage = 'Invalid Employee ID. Please try again.';
            }
        },
        async checkValidID() {
            try {
                const response = await axios.get(`http://127.0.0.1:5000/employee/${this.empId}`);
                console.log(response.data);
                return response.data;
            } catch (error) {
                console.error(error);
                return false; 
            }
        }
    }
}
</script>

<style scoped>
/* Add any custom styles here */
</style>