# RemoteVim
config your remote session
```json
{
  "username": "chris",
  "hostname": "localhost",
  "port": "22",
  "current_path": "/"
}
```

show current_path and vim remote file.
```bash
cvim ls
python remote_vim.py --file filename
```

```
cd RemoteVim/
chmod u+x *
vim ~/.bashrc
export PATH="path_to_RemoteVim/bin:$PATH"
source ~/.bashrc
```
