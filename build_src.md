# pypi.org

* Удалить старые сборки
* Собрать
* Залить

```
rm -rf dist/ build/
python setup.py sdist bdist_wheel
twine upload --repository pypi dist/*
```