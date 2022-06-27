git add setup.cfg
git commit -m "Mise à jour mineure"
git push
python -m build
twine upload dist/*
