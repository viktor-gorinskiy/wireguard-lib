# Build docs
* Перейти в корень проекта
`sphinx-apidoc -o docs wireguard/wireguard.py`
* Перейти в docs
```
make clean html
make html
```