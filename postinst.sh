if [ -f /usr/share/videb/videb.py ];
    then rm -f /usr/bin/videb
fi

ln -s /usr/share/videb/videb.py /usr/bin/videb
