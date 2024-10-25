# DB Dump Service

This service automates database dumps by connecting to a specified database over SSH and uploading the backup files to S3-compatible storage. Scheduled tasks can be configured for regular backups.

## Configuration

Configuration is handled through a YAML file structured as shown below.

### SSH Configuration

Define SSH connections for remote database access.

```yaml
ssh:
  - name: example_ssh_name
    host: 127.0.0.1
    port: 22
    username: root
    password: root
```

### S3 Configuration

Define S3-compatible storage settings where dumps will be stored.

```yaml
s3:
  - name: example_s3_name
    url: https://s3.example.com
    bucket: bucket
    region: ru-1
    access_key: cb46446
    secret_key: 00b5c7a0b9a26cec8b92d5897275ef7d
    root: dumps
```

### Backup Job Configuration

Set up each backup job specifying the target database, SSH and S3 configurations, and schedule details.

```yaml
configs:
  - settings:
      name: app
      ssh_name: example_ssh_name
      s3_name: example_s3_name
      schedule:
        active: true
        minute: 0
        hour: 0
        day_of_week: '*'
        day_of_month: '*'
        month_of_year: '*'
    database:
      type: postgres
      host: localhost
      port: 5432
      name: postgres
      user: postgres
      password: postgres
      docker_container: container-db-1
```

- **`settings`**: Configure the backup settings.
  - **`name`**: Identifier for the job.
  - **`ssh_name`**: Reference to the SSH configuration.
  - **`s3_name`**: Reference to the S3 configuration.
  - **`schedule`**: Cron-like schedule for the backup job.
- **`database`**: Define database connection details.
  - **`type`**: Database type (e.g., `postgres`).
  - **`docker_container`**: Specify if the database is in a Docker container (optional).

## Running the Service

1. Install dependencies.
2. Add your configuration to the service config file.
3. Start the service to automate backups based on the schedule defined in `configs`.

## License

This project is licensed under the MIT License.