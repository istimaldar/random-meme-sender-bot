from dynaconf import Dynaconf, Validator

settings = Dynaconf(
    environments=False,
    envvar_prefix="RNDMESND",
    settings_files=["settings.toml", ".secrets.toml"],
    merge_enabled=True,
    validators=[
        Validator("bot.token", must_exist=True, is_type_of=str),
        Validator("messages.start", must_exist=True, is_type_of=str),
        Validator("messages.help", must_exist=True, is_type_of=str),
        Validator("messages.privacy", must_exist=True, is_type_of=str),
        Validator("messages.add_meme", must_exist=True, is_type_of=str),
        Validator("messages.upload.no_caption", must_exist=True, is_type_of=str),
        Validator("messages.upload.no_image", must_exist=True, is_type_of=str),
        Validator("messages.upload.invalid_caption", must_exist=True, is_type_of=str),
        Validator("messages.upload.duplicated_caption", must_exist=True, is_type_of=str),
        Validator("messages.list.image_select", must_exist=True, is_type_of=str),
        Validator("messages.select.invalid_format", must_exist=True, is_type_of=str),
        Validator("messages.select.not_found", must_exist=True, is_type_of=str),
        Validator("messages.select.canceled", must_exist=True, is_type_of=str),
        Validator("messages.select.deleted", must_exist=True, is_type_of=str),
        Validator("messages.buttons.caption", must_exist=True, is_type_of=str),
        Validator("messages.buttons.delete", must_exist=True, is_type_of=str),
        Validator("messages.buttons.cancel", must_exist=True, is_type_of=str)
    ]
)
