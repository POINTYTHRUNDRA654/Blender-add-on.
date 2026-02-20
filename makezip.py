import zipfile, pathlib
root = pathlib.Path('.').resolve()
zip_path = root.parent / 'Blender-add-on-v2.1.2.zip'
with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
    for path in root.rglob('*'):
        if path.is_file():
            rel = path.relative_to(root)
            if rel.parts[0] in ('.git', 'tools', '.venv'):
                continue
            zf.write(path, rel)
print('Created', zip_path)
