# Backend for WFH Management System

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

### Set-up project in files

Clone this repository or download the files to local directory. Use the command line to navigate to (`~/SPM-MeeRebus/SPM-MeeRebus`)

### Provide Environment Variables

We will use the environment variables to connect to our backend server to use its APIs and data processing. We need to provide it the following information. Edit the backend server URL in `.env.example` using any text editor.

1. Replace `""` fields with the respective information (backend server URL)
2. Rename `.env.example` to `.env`

**Note: `.env` is automatically ignored by git`**

### Install Dependencies

```
pip install --upgrade pip
pip install -r requirements.txt
```

## Development Mode

Run app in development mode

```shell
python api.py
```

## Testing

Navigate to root folder of `backend`

```shell
cd /path/to/SPM-MeeRebus/backend
python run_all_tests.py
```

This command runs all of our unit, functional and integration tests.

Navigate to root folder of selenium-tests

```
cd /path/to/SPM-MeeRebus/backend
pytest test_SCRUM-x.py # replace x with the SCRUM number 
```

The tests scripts inside selenium-tests are E2E tests that simulate a real user flow.
