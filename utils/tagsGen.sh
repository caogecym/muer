# create .py list
find . -name '*.py' > cscope.files

# remove .py file of no use
vi cscope.files -s ~/cscope/delPtn.vim

# create the tags file
echo "generating tags file..."
ctags -L cscope.files

# clean workspace
rm cscope.files
