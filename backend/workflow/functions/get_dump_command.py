from config.models import Config, DatabaseConnection


def get_dump_command(config: Config, file_path: str):
    db = config.database_connection
    if db.type == DatabaseConnection.Type.POSTGRES:
        cmd = f'pg_dump "postgresql://{db.user}:{db.password}@{db.host}:{db.port}/{db.db}"'
    elif db.type == DatabaseConnection.Type.DOCKER_POSTGRES:
        cmd = f'docker exec {db.host} pg_dump -c -U {db.user} -d {db.db}'
    else:
        raise ValueError(f'Unsupported database type: {db.type}')
    cmd = f'{cmd} > {file_path}'
    return cmd
