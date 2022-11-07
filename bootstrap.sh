echo "Starting local nginx service..."
brew services start nginx
echo "Begin to start CoderMind."
uwsgi --ini codermind_uwsi.ini


echo "Starting stop nginx..."
brew services stop nginx
echo "Server exit success."
