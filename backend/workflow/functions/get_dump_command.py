from config.models import Config


def get_dump_command(config: Config, file_path: str):
    db = config.database_connection
    if db.type == 'postgres':
        cmd = f'pg_dump "postgresql://{db.user}:{db.password}@{db.host}:{db.port}/{db.db}"'
    else:
        raise ValueError(f'Unsupported database type: {db.type}')
    # if db.docker_container:
    #     cmd = f'docker exec {db.docker_container} {cmd}'
    cmd = f'{cmd} > {file_path}'
    return cmd
