from pydantic import BaseModel


class ConfigSettingsSchedule(BaseModel):
    active: bool = False
    minute: str | int = 0
    hour: str | int = 0
    day_of_week: str | int = '*'
    day_of_month: str | int = '*'
    month_of_year: str | int = '*'

    def get_crontab_config(self):
        return {
            'minute': self.minute,
            'hour': self.hour,
            'day_of_week': self.day_of_week,
            'day_of_month': self.day_of_month,
            'month_of_year': self.month_of_year,
        }


class ConfigSettings(BaseModel):
    name: str
    max_versions: int = 5
    s3_name: str = None
    ssh_name: str = None
    schedule: ConfigSettingsSchedule | None = None
