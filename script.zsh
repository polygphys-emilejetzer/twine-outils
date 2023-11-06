git add setup.cfg
git commit -m "Mise à jour mineure"
git tag $1
git push --tags
python -m build
twine upload dist/*
