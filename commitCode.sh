#require message string to git to exist
if [ "$#" -ne 1 ]; then
    echo "build.sh requires one command line argument"
    exit 1
fi

#require messsage string to be longer than 10 chars
if [ ${#1} -lt 10 ]; then
    echo "build.sh requires a message greater than 10 chars"
    exit 2
fi

#commit with message from command line
git add .
git commit -m "$1"
