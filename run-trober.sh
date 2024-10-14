PWD=`pwd`

if [ -z "$1" ]
then
    echo "Provide the file to inpsect and run!"
    exit
else
    pep8 $1 >/dev/null 2>&1
    if [ $? != 0 ]; then
        echo "PEP8 Fail :("
        pep8 $1
        exit
    else
        pylint $1 >/dev/null 2>&1
        if [ $? != 0 ]; then
            echo "PyLint3 Fail :("
            pylint $1
            exit
        else
            pyflakes3 $1 >/dev/null 2>&1
            if [ $? != 0 ]; then
                echo "PyFlakes3 Fail :("
                pyflakes3 $1
            else
                #echo "You win :D"
                # Run the following command...
                if [ -x "$PWD/$1" ]
                then
                    echo ./$1 $2 $3 $4 $5 $6
                else
                    echo "Make the inspected file be executable with:\n chmod +x "$1
                fi
            fi
        fi
    fi
fi
