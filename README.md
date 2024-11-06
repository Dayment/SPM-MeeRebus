
# WFH Management System SPM

## 🚀 Quick Start

This project aims for staff of All-In-One to seamlessly manage their work from home applications. This project is targetted for the first release, which consists of the following core features:

- HR and Senior Management should be allowed to view overall and team schedule
- Managers and Directors should be allowed to see their own team's schedule, approve and reject arrangements
- Staff should be able to view their team schedule, own schedule, apply for arrangement and withdraw an approved arrangement

Find the project live at:

- [Web application](https://spm-mee-rebus.vercel.app/)
- [Backend server](https://earnest-grace-production-04af.up.railway.app/home)

### Frontend

- [Vue.js](https://vuejs.org/) – Progressive JavaScript framework for building user interfaces
- [Vite](https://vitejs.dev/) – Lightning-fast build tool and development server
- [Bootstrap](https://getbootstrap.com/) – Popular CSS framework for responsive, mobile-first web development.

### Backend

- [Flask](https://flask.palletsprojects.com/) – Lightweight WSGI web application framework.
- [Supabase](https://supabase.com/) - The open source Firebase alternative for
  PostgreSQL

### Dev Tools

- [ESLint](https://eslint.org/) - Linting utility for TypeScript and TSX
- [Prettier](https://prettier.io/) - Code formatter
- [Selenium](https://www.selenium.dev/) – End-to-end testing framework for browser automation.
- [Vercel](https://vercel.com/) – Deployment platform for modern frontend applications.
- [Docker](https://www.docker.com/) - Containerized development environment

### Development

- [Vercel](https://vercel.com/) - Hosting and deployment
- [Supabase](https://supabase.com/) - Database and authentication

## 📚 Documentation

For more details on our project architecture, refer to our [C4 diagram](https://drive.google.com/file/d/1vJXdjTIHsBkzjJ09ZdxLewhopmxx2CXq/view?usp=drive_link)

We've created detailed setup guides for our Frontend and Backend componenents.

- [Frontend README](https://github.com/Dayment/SPM-MeeRebus/blob/main/SPM-MeeRebus/README.md)
- [Backend README](https://github.com/Dayment/SPM-MeeRebus/blob/main/backend/README.md)

Continuos Integration is enabled for this repository through Github Actions, with each PR automatically triggering the CI/CD pipeline. Promotion to production server for the latest deployment is handled manually.

The CI pipeline scripts can be found in .github/workflows

- [PR template](https://github.com/Dayment/SPM-MeeRebus/blob/main/.github/PULL_REQUEST_TEMPLATE.md)
