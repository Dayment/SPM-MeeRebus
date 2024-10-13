import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import path from 'path';

export default defineConfig({
    plugins: [vue()],
    resolve: {
        alias: {
        '@': path.resolve(__dirname, 'src'),
        },
    },
    server: {
        port: 5174, // Change this to your desired port
        open: true, // Automatically open the app in the browser
    },
});