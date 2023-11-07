git add setup.cfg

message="Màj mineure $1"
while getopts ":m:a" o
do
    case "${o}" in
        m)
            message=$OPTARG
        ;;
        a)
            git add -A
        ;;
    esac
done

git commit -m $message
git tag $1 -m $message
git push --tags
python -m build
twine upload dist/*
