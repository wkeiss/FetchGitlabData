#[Getting started with the API — python-gitlab 2.4.0 documentation](https://python-gitlab.readthedocs.io/en/stable/api-usage.html#gitlab-gitlab-class)

import gitlab
import json
import os

private_token = os.environ['private_token']

gl = gitlab.Gitlab('https://gitlab.com', private_token)

'''
# Get a project by ID
project_id = 851
project = gl.projects.get(project_id)
[Projects — python-gitlab 2.4.0 documentation](https://python-gitlab.readthedocs.io/en/stable/gl_objects/projects.html)
'''
project_id = 16345223
project = gl.projects.get(project_id)

'''
‘By default GitLab does not return the complete list of items. 
Use the all parameter to get all the items when using listing methods
- [Getting started with the API — python-gitlab 2.4.0 documentation](https://python-gitlab.readthedocs.io/en/stable/api-usage.html#pagination)
'''
branches = project.branches.list(all = True) 
#print(len(branches)) (output:36 )


'''
[Issues — python-gitlab 2.4.0 documentation](https://python-gitlab.readthedocs.io/en/stable/gl_objects/issues.html#project-issues)
'''
issues = project.issues.list(all = True)

#print('The number of Tasks respository issues:', + len(issues)) #output: The number of Tasks respository issues: 144


#save the date to Dic

issue_data = {}
issue_note_data = {}
commit_data = {}
commit_comment_data ={}

issue_authors = {}

'''
data = {}
data['people'] = []
data['people'].append({
    'name': 'Scott',
    'website': 'stackabuse.com',
    'from': 'Nebraska'
})
[Reading and Writing JSON to a File in Python](https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/#:~:text=The%20easiest%20way%20to%20write,of%20data%20types%20supported%20here.)
'''
'''
# Get issue data
for issue in issues:
	issue_data[issue.iid] = {
	'issue_iid': issue.iid,
	'created_at': issue.created_at,
	'author': issue.author['name'],
	'title': issue.title,
	'description': issue.description
	}
'''

'''
#get issue note data
for issue in issues:
	issue_discussions = issue.discussions.list(all = True)
	issue_note_data[issue.iid] = []
	for issue_discussion in issue_discussions:
		for note in issue_discussion.attributes['notes']:
			issue_note_data[issue.iid].append(
				{'author': note['author']['name'],
				'body': note['body'],
				'created_at': note['created_at']

				})
			#print(issue_note_data)
'''

'''	
#Get commits data	
for branch in branches:
	#print(branch) 
	commits = project.commits.list(all = True, query_parameters={'ref_name': branch.name})
	commit_data[branch.name] = []
	for commit in commits:
		commit_data[branch.name].append(
			{'id': commit.attributes['id'],
			'message': commit.attributes['message'],
			'author': commit.attributes['author_name'],
			'created_at': commit.attributes['created_at']
			})
		#print(commit_data)
'''

'''
#Get commit comment data:
for branch in branches:
	commits = project.commits.list(all = True, query_parameters={'ref_name': branch.name})
	for commit in commits:
		commit_discussions = commit.discussions.list()
		for commit_discussion in commit_discussions:
			commit_comment_data[commit.attributes['id']] = []
			for comment in commit_discussion.attributes['notes']:
				commit_comment_data[commit.attributes['id']].append(
					{'body': comment['body'],
					'author': comment['author']['name'],
					'created_at':comment['created_at']
					})

			#print(commit_comment_data)
'''

'''
# create a new file and save data to it
def save_to_file(data, filename):
	with open(filename, 'a') as f:
		json.dump(data, f, indent=4, ensure_ascii=False)
	pass
'''

#save_to_file(issue_data, 'issue_data.txt')
#save_to_file(issue_note_data, 'issue_note_data.txt')
#save_to_file(commit_data, 'commit_data.txt')
#save_to_file(commit_comment_data, 'commit_comment_data.txt')


# load data from file
def load_data_from_file(filename):
	with open(filename, 'r') as f:
		return json.load(f)
	pass


# Get group members
# [Groups — python-gitlab 2.5.0 documentation](https://python-gitlab.readthedocs.io/en/stable/gl_objects/groups.html)
def get_group_member_name_list(group_id):
	group = gl.groups.get(group_id)
	members = group.members.list(all = True)
	members_name_list = []
	for member in members:
		members_name_list.append(member.attributes['name'])
		#print(members_name_list)
	return members_name_list

def get_top5(data):
	def by_value(item):
		return item[1]
	for k, v in sorted(data.items(), key=by_value, reverse=True)[:5]:
		print(k, '->', v)

'''
# Count the number of issues for each member(branch)
group_id = 6937760
members_name_list = get_group_member_name_list(group_id)
#print(members_name_list)
issue_data = load_data_from_file('issue_data.txt')
issues = {}
for member in members_name_list:
	issues[member]=[]
	for iid in issue_data:
		if issue_data[iid]['author'] == member:
			issues[member].append(iid)
			#print(issues)
count_issue_of_every_member = {}
for member in members_name_list:
	count_issue_of_every_member[member] = len(issues[member])
	#print(count_issue_of_every_member)

[How to Iterate Through a Dictionary in Python – Real Python](https://realpython.com/iterate-through-dictionary-python/#iterating-through-values)
>>> incomes = {'apple': 5600.00, 'orange': 3500.00, 'banana': 5000.00}
>>> def by_value(item):
...     return item[1]
...
>>> for k, v in sorted(incomes.items(), key=by_value):
...     print(k, '->', v)
...
('orange', '->', 3500.0)
('banana', '->', 5000.0)
('apple', '->', 5600.0)
& [Python: Get top n key's with Value as dictionary - Stack Overflow](https://stackoverflow.com/questions/38218501/python-get-top-n-keys-with-value-as-dictionary)

print('Top5 is:')
get_top5(count_issue_of_every_member)
'''

'''
# Count the number of issue notes for each member(branch)
group_id = 6937760
members_name_list = get_group_member_name_list(group_id)
#print(members_name_list)
issue_note_data = load_data_from_file('issue_note_data.txt')
count_issue_note_of_every_member = {}
for member in members_name_list:
	count_issue_note_of_every_member[member] = 0 # 让每一个学员的发布的issue note 的数量为0
	for iid in issue_note_data:
		for note in issue_note_data[iid]:
			if note['author'] == member:
				count_issue_note_of_every_member[member] += 1
				#print(count_issue_note_of_every_member)
print('Top5 ic:')
get_top5(count_issue_note_of_every_member)
'''

'''
# Count the number of commits per branch
commit_data = load_data_from_file('commit_data.txt')
count_commit_of_every_member = {}
for branch_name in commit_data:
	count_commit_of_every_member[branch_name] = len(commit_data[branch_name])
	#print(count_commit_of_every_member)
print('Top5 ci:')
get_top5(count_commit_of_every_member)
'''

# Count the number of commit comments for each member
group_id = 6937760
members_name_list = get_group_member_name_list(group_id)
#print(members_name_list)
commit_comment_data = load_data_from_file('commit_comment_data.txt')
count_commit_comment_of_every_member = {}
for member in members_name_list:
	count_commit_comment_of_every_member[member] = 0
	for id in commit_comment_data:
		for comment in commit_comment_data[id]:
			if comment['author'] == member:
				count_commit_comment_of_every_member[member] +=1
				print(count_commit_comment_of_every_member)
print('Top5 cc:')
get_top5(count_commit_comment_of_every_member)
