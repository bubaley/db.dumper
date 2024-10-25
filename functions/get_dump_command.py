from managers.config_manager import Config


def get_dump_command(config: Config, file_path: str):
    db = config.database
    # if db.type == 'mysql':
    #     cmd = f'mysqldump -h {db.host} -P {db.port} -u {db.user} -p {db.password} {db.name}'
    if db.type == 'postgres':
        cmd = f'pg_dump "postgresql://{db.user}:{db.password}@{db.host}:{db.port}/{db.name}"'
    else:
        raise ValueError(f'Unsupported database type: {db.type}')
    if db.docker_container:
        cmd = f'docker exec {db.docker_container} {cmd}'
    cmd = f'{cmd} > {file_path}'
    return cmd
