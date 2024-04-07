def generate_sp(content: str, template_path: str, sp_nm: str, sp_nm_rmk: str, created_time) -> str:
    sp_body_text = content

    with open(template_path, 'r') as file:
        template = file.read()

    return template.format(sp_nm=sp_nm, sp_nm_rmk=sp_nm_rmk, created_time=created_time, sp_body_text=sp_body_text)
