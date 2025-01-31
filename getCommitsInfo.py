import sys
import csv
from pydriller import Repository
from pydriller.metrics.process.code_churn import CodeChurn
from pydriller.metrics.process.commits_count import CommitsCount
from pydriller.metrics.process.hunks_count import HunksCount

columns = ['Old File Path', 'New File Path', 'Commit SHA', 'Parent Commit SHA', 'Commit Message', 'Diff Myers', 'Diff Histogram', 'Matches']

rows = []
count=0
last_n=500

commits = []
for x in Repository(sys.argv[1],only_no_merge=True,skip_whitespaces=True,order='reverse').traverse_commits():
  if (x.in_main_branch==True):
    count=count+1
    commits.append(x)
    if count == last_n:
      break

count=0
commits2 = []
for x in Repository(sys.argv[1],only_no_merge=True,skip_whitespaces=True,histogram_diff=True,order='reverse').traverse_commits():
  if (x.in_main_branch==True):
    count=count+1
    commits2.append(x)
    if count == last_n:
      break

in_order = []
for value in range(len(commits)):
  in_order.append(commits.pop())

commits=in_order

in_order = []
for value in range(len(commits2)):
  in_order.append(commits2.pop())

commits2=in_order

i=-1
for it in range(len(commits)):
  commit = commits[it]
  commit2 = commits2[it]
  i+=1
  print('[{}/{}] Mining commit {}.{}'.format(i+1,len(commits),sys.argv[1],commit.hash))
  for it2 in range(len(commit.modified_files)):
    m = commit.modified_files[it2]
    diff_m = m.diff

    m2 = commit2.modified_files[it2]
    diff_h = m2.diff
    # for m in commit2.modified_files:

    if diff_h == diff_m:
        rows.append([m.old_path, m.new_path, commit.hash, commit.parents[0], commit.msg, diff_m, diff_h, 'True'])
    else:
        rows.append([m.old_path, m.new_path, commit.hash, commit.parents[0], commit.msg, diff_m, diff_h, 'False'])

    # rows.append([m.old_path, m.new_path, commit.hash, commit.parents[0], commit.msg, diff_m, diff_h])
        
#   if (i>=1):   
#     rows.append([m.old_path, m.new_path, commit.hash, commit.parents[0], commit.msg, diff_m, diff_h])
#   elif (i==0):
#     rows.append([m.old_path, m.new_path, commit.hash, commit.parents[0], commit.msg, '', ''])
       
with open(sys.argv[1]+'_results/commits_info.csv', 'a') as csvFile:
  writer = csv.writer(csvFile)
  writer.writerow(columns)
  writer.writerows(rows)