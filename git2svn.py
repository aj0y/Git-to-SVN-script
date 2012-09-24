import os

# read in the commit diffs

# Eg.
# git diff --name-status 2abc775f c1f0530a
# M       common.php
# M       file.class.php
# M       fileSuccess.php
# D	  deletedFile.php


# run git log
# find all commits since last commit

prev_commit_file = open('last_commit.git', "r")
prev_commit = prev_commit_file.readline()
prev_commit_file.close()

git_repo = 'git-repo'
svn_repo = 'svn-repo'

os.chdir( '../'+git_repo)

# prev_commit = 'a3edbde4'
child = os.popen( "git log --pretty=format:'%h' " + prev_commit + "..")
output = child.read()
child.close()

# split output into lines
commits = output.split('\n')
latest_commit = commits[0]
# write commit to file

child = os.popen("git diff --name-status " + prev_commit + " " + latest_commit)
commitdiff = child.read()
child.close()

# get the files modified
print commitdiff
os.chdir( '../'+svn_repo)

filediff = commitdiff.split('\n')

filenames = ''

for line in filediff:
	line = line.strip()
	if line == '':
		continue

	print line
	mode, filename = line.split('\t',1)
	mode = mode.strip()
	filename = filename.strip()

	if filename == '':
		continue

	if mode == 'M' or mode == 'A':
		# file modified
		# need to be copied
		if not os.path.exists('../git-repo/' + filename):
			print 'File Not Found : ', filename
			continue

		print 'cp ../git-repo/'+filename, filename
		os.system( 'cp ../git-repo/'+filename + ' ' + filename )

	if mode == 'A':
		# new file
		# need to be copied
		print 'cp ../git-repo/'+filename, filename
		os.system( 'cp ../git-repo/'+filename + ' ' + filename )
		print 'svn add ', filename
		os.system( 'svn add ' + filename)

	if mode == 'D':
		# file deleted
		print 'svn rm', filename
		os.system( 'svn rm ' + filename)

	filenames += ' ' + filename

os.system('svn status')

print 'Latest Commit : ' + latest_commit

# save latest commit to file
last_commit_file = open('last_commit.git', "w")
last_commit_file.writelines( latest_commit)
last_commit_file.close()

print 'done\n'
print 'svn commit' , filenames, '-m ""'

