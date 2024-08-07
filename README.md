# Cascade

**Cascade** is a versatile platform for managing Incus instances through a user-friendly web interface. It supports the creation, management, modification, and deletion of application containers, system containers, and virtual machines (VMs) all from a single dashboard. Users can select and purchase plans to access specific features or instances, offering extensive capabilities similar to Pterodactyl but with broader functionality.

Cascade also features a configurable API that supports running multiple versions concurrently and a JWT cookie-based system for secure communication between the backend and the web UI.

## Features

- **Unified Dashboard**: Manage application containers, system containers, and VMs from a single, intuitive interface.
- **Configurable API**: Run and manage multiple API versions simultaneously with extensive configuration options.
- **Plan Management**: Purchase and manage plans for different features and instance access.
- **JWT Cookie-Based API**: Secure communication between the backend and web UI.
- **Flexible Database Options**: Supports any database compatible with SQLAlchemy.
- **Customizable Caching Storage**: Choose from memcached, Redis, SQLite3, or a custom system.

## Project Structure

The project is organized into several key components:

```
├── README.md
├── api
│   └── v0
│       ├── __init__.py
│       ├── views
│       │   └── index.py
│       └── views.py
├── blueprints.py
├── core
│   ├── authentication.py
│   ├── cache.py
│   ├── cache_storage
│   │   ├── __init__.py
│   │   └── connectors
│   │       ├── base.py
│   │       ├── memcached.py
│   │       ├── redis.py
│   │       ├── sqlite.py
│   │       └── system.py
│   ├── config.py
│   ├── cookies.py
│   ├── database
│   │   ├── DALs
│   │   │   ├── base.py
│   │   │   ├── config_dal.py
│   │   │   ├── instance
│   │   │   │   ├── chicken_dal.py
│   │   │   │   ├── instance_audit_dal.py
│   │   │   │   ├── instance_dal.py
│   │   │   │   ├── node_dal.py
│   │   │   │   └── subuser_dal.py
│   │   │   └── user
│   │   │       ├── email_oauth.py
│   │   │       ├── mfa_backup_codes_dal.py
│   │   │       ├── mfa_dal.py
│   │   │       ├── oauth_dal.py
│   │   │       ├── password_reset_dal.py
│   │   │       ├── user_audit_dal.py
│   │   │       └── user_dal.py
│   │   ├── __init__.py
│   │   └── models
│   │       ├── Config.py
│   │       ├── instance
│   │       │   ├── Chicken.py
│   │       │   ├── Instance.py
│   │       │   ├── InstanceAudit.py
│   │       │   ├── Node.py
│   │       │   └── Subuser.py
│   │       └── user
│   │           ├── EmailOauth.py
│   │           ├── Mfa.py
│   │           ├── MfaBackupCodes.py
│   │           ├── Oauth.py
│   │           ├── PasswordReset.py
│   │           ├── User.py
│   │           └── UserAudit.py
│   ├── decorators.py
│   ├── email.py
│   ├── env_manager.py
│   ├── hashing.py
│   ├── incus
│   │   ├── __init__.py
│   │   ├── models
│   │   │   ├── metadata.py
│   │   │   ├── responses.py
│   │   │   └── server.py
│   │   └── status_codes.py
│   ├── server_events.py
│   ├── sessions.py
│   ├── type_hints.py
│   └── utilities.py
├── example.env
├── requirements.txt
├── server.py
└── templates
```

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Daftscientist/Cascade.git
    cd Cascade
    ```

2. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Set up environment variables:**

    Copy `example.env` to `.env` and configure your environment settings:

    ```bash
    cp example.env .env
    ```

    Update `.env` with your specific configuration:

    ```ini
    APP_NAME = 'my_app'
    ACTIVE_VERSIONS = ['v0']
    APP_HOST = 'localhost'
    APP_PORT = '8000'
    RELOAD_MODE = True
    DEBUG_MODE = True
    DEV_MODE = True

    COOKIE_IDENTITY = 'your_cookie_identity'
    COOKIE_SECRET = 'your_cookie_secret'
    MAIN_DB_URL = 'sqlite:///main.db'
    # Can be any URL supported by SQLAlchemy, e.g., PostgreSQL, MySQL, SQLite

    DB_ENCRYPTION_KEY = 'your_db_encryption_key'

    CACHE_STORAGE_TYPE = 'sqlite'
    # Options: 'sqlite', 'redis', 'memcached', or 'system'
    REDIS_URL = 'redis://localhost:6379/0'
    CACHE_STORAGE_DB_PATH = '/path/to/cache.db'
    MEMCACHED_URL = 'localhost:11211'

    SESSION_TTL = 3600
    CACHE_EXPIRATION_INTERVAL = 3600
    ```

4. **Run the server:**

    ```bash
    python server.py
    ```

## Usage

1. **Access the Web UI:**

   Open your web browser and navigate to `http://localhost:8000` (or the port specified in your `.env` file).

2. **API Interaction:**

   Cascade supports multiple versions of the API running concurrently. Configure and manage these versions via the [API Documentation](api/v0/views/index.py). The platform uses a JWT cookie-based API for secure communication between the backend and web UI.

## Configuration

1. **Database Setup:**

   Cascade uses SQLAlchemy, which allows you to use any database supported by SQLAlchemy. Configure your database connection in the `.env` file using the `MAIN_DB_URL` setting.

2. **Caching Storage Setup:**

   The caching system supports several storage options: SQLite, Redis, Memcached, or a custom system. Specify your preferred caching storage in the `.env` file under `CACHE_STORAGE_TYPE`. Configure additional caching settings like `REDIS_URL`, `CACHE_STORAGE_DB_PATH`, or `MEMCACHED_URL` as needed.

## Contributing

Contributions are welcome! Please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on how to contribute to this project.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or support, please open an issue in the GitHub repository.