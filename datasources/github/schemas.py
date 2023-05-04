
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

from pydantic import AnyUrl, BaseModel, Field


class Actor(BaseModel):
    id: int
    login: str
    display_login: Optional[str] = None
    gravatar_id: Optional[str]
    url: AnyUrl
    avatar_url: AnyUrl


class Repo(BaseModel):
    id: int
    name: str
    url: AnyUrl


class Org(BaseModel):
    id: int
    login: str
    display_login: Optional[str] = None
    gravatar_id: Optional[str]
    url: AnyUrl
    avatar_url: AnyUrl


class StateReason(Enum):
    completed = 'completed'
    reopened = 'reopened'
    not_planned = 'not_planned'
    NoneType_None = None


class UserItem(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    login: str = Field(..., examples=['octocat'])
    id: int = Field(..., examples=[1])
    node_id: str = Field(..., examples=['MDQ6VXNlcjE='])
    avatar_url: AnyUrl = Field(
        ..., examples=['https://github.com/images/error/octocat_happy.gif']
    )
    gravatar_id: Optional[str] = Field(
        ..., examples=['41d064eb2195891e12d0413f63227ea7']
    )
    url: AnyUrl = Field(..., examples=['https://api.github.com/users/octocat'])
    html_url: AnyUrl = Field(..., examples=['https://github.com/octocat'])
    followers_url: AnyUrl = Field(
        ..., examples=['https://api.github.com/users/octocat/followers']
    )
    following_url: str = Field(
        ..., examples=['https://api.github.com/users/octocat/following{/other_user}']
    )
    gists_url: str = Field(
        ..., examples=['https://api.github.com/users/octocat/gists{/gist_id}']
    )
    starred_url: str = Field(
        ..., examples=['https://api.github.com/users/octocat/starred{/owner}{/repo}']
    )
    subscriptions_url: AnyUrl = Field(
        ..., examples=['https://api.github.com/users/octocat/subscriptions']
    )
    organizations_url: AnyUrl = Field(
        ..., examples=['https://api.github.com/users/octocat/orgs']
    )
    repos_url: AnyUrl = Field(
        ..., examples=['https://api.github.com/users/octocat/repos']
    )
    events_url: str = Field(
        ..., examples=['https://api.github.com/users/octocat/events{/privacy}']
    )
    received_events_url: AnyUrl = Field(
        ..., examples=['https://api.github.com/users/octocat/received_events']
    )
    type: str = Field(..., examples=['User'])
    site_admin: bool
    starred_at: Optional[str] = Field(None, examples=['"2020-07-09T00:17:55Z"'])


class Label(BaseModel):
    id: Optional[int] = None
    node_id: Optional[str] = None
    url: Optional[AnyUrl] = None
    name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    default: Optional[bool] = None


class AssigneeItem(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    login: str = Field(..., examples=['octocat'])
    id: int = Field(..., examples=[1])
    node_id: str = Field(..., examples=['MDQ6VXNlcjE='])
    avatar_url: AnyUrl = Field(
        ..., examples=['https://github.com/images/error/octocat_happy.gif']
    )
    gravatar_id: Optional[str] = Field(
        ..., examples=['41d064eb2195891e12d0413f63227ea7']
    )
    url: AnyUrl = Field(..., examples=['https://api.github.com/users/octocat'])
    html_url: AnyUrl = Field(..., examples=['https://github.com/octocat'])
    followers_url: AnyUrl = Field(
        ..., examples=['https://api.github.com/users/octocat/followers']
    )
    following_url: str = Field(
        ..., examples=['https://api.github.com/users/octocat/following{/other_user}']
    )
    gists_url: str = Field(
        ..., examples=['https://api.github.com/users/octocat/gists{/gist_id}']
    )
    starred_url: str = Field(
        ..., examples=['https://api.github.com/users/octocat/starred{/owner}{/repo}']
    )
    subscriptions_url: AnyUrl = Field(
        ..., examples=['https://api.github.com/users/octocat/subscriptions']
    )
    organizations_url: AnyUrl = Field(
        ..., examples=['https://api.github.com/users/octocat/orgs']
    )
    repos_url: AnyUrl = Field(
        ..., examples=['https://api.github.com/users/octocat/repos']
    )
    events_url: str = Field(
        ..., examples=['https://api.github.com/users/octocat/events{/privacy}']
    )
    received_events_url: AnyUrl = Field(
        ..., examples=['https://api.github.com/users/octocat/received_events']
    )
    type: str = Field(..., examples=['User'])
    site_admin: bool
    starred_at: Optional[str] = Field(None, examples=['"2020-07-09T00:17:55Z"'])


class Assignee(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    login: str = Field(..., examples=['octocat'])
    id: int = Field(..., examples=[1])
    node_id: str = Field(..., examples=['MDQ6VXNlcjE='])
    avatar_url: AnyUrl = Field(
        ..., examples=['https://github.com/images/error/octocat_happy.gif']
    )
    gravatar_id: Optional[str] = Field(
        ..., examples=['41d064eb2195891e12d0413f63227ea7']
    )
    url: AnyUrl = Field(..., examples=['https://api.github.com/users/octocat'])
    html_url: AnyUrl = Field(..., examples=['https://github.com/octocat'])
    followers_url: AnyUrl = Field(
        ..., examples=['https://api.github.com/users/octocat/followers']
    )
    following_url: str = Field(
        ..., examples=['https://api.github.com/users/octocat/following{/other_user}']
    )
    gists_url: str = Field(
        ..., examples=['https://api.github.com/users/octocat/gists{/gist_id}']
    )
    starred_url: str = Field(
        ..., examples=['https://api.github.com/users/octocat/starred{/owner}{/repo}']
    )
    subscriptions_url: AnyUrl = Field(
        ..., examples=['https://api.github.com/users/octocat/subscriptions']
    )
    organizations_url: AnyUrl = Field(
        ..., examples=['https://api.github.com/users/octocat/orgs']
    )
    repos_url: AnyUrl = Field(
        ..., examples=['https://api.github.com/users/octocat/repos']
    )
    events_url: str = Field(
        ..., examples=['https://api.github.com/users/octocat/events{/privacy}']
    )
    received_events_url: AnyUrl = Field(
        ..., examples=['https://api.github.com/users/octocat/received_events']
    )
    type: str = Field(..., examples=['User'])
    site_admin: bool
    starred_at: Optional[str] = Field(None, examples=['"2020-07-09T00:17:55Z"'])


class State(Enum):
    open = 'open'
    closed = 'closed'


class CreatorItem(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    login: str = Field(..., examples=['octocat'])
    id: int = Field(..., examples=[1])
    node_id: str = Field(..., examples=['MDQ6VXNlcjE='])
    avatar_url: AnyUrl = Field(
        ..., examples=['https://github.com/images/error/octocat_happy.gif']
    )
    gravatar_id: Optional[str] = Field(
        ..., examples=['41d064eb2195891e12d0413f63227ea7']
    )
    url: AnyUrl = Field(..., examples=['https://api.github.com/users/octocat'])
    html_url: AnyUrl = Field(..., examples=['https://github.com/octocat'])
    followers_url: AnyUrl = Field(
        ..., examples=['https://api.github.com/users/octocat/followers']
    )
    following_url: str = Field(
        ..., examples=['https://api.github.com/users/octocat/following{/other_user}']
    )
    gists_url: str = Field(
        ..., examples=['https://api.github.com/users/octocat/gists{/gist_id}']
    )
    starred_url: str = Field(
        ..., examples=['https://api.github.com/users/octocat/starred{/owner}{/repo}']
    )
    subscriptions_url: AnyUrl = Field(
        ..., examples=['https://api.github.com/users/octocat/subscriptions']
    )
    organizations_url: AnyUrl = Field(
        ..., examples=['https://api.github.com/users/octocat/orgs']
    )
    repos_url: AnyUrl = Field(
        ..., examples=['https://api.github.com/users/octocat/repos']
    )
    events_url: str = Field(
        ..., examples=['https://api.github.com/users/octocat/events{/privacy}']
    )
    received_events_url: AnyUrl = Field(
        ..., examples=['https://api.github.com/users/octocat/received_events']
    )
    type: str = Field(..., examples=['User'])
    site_admin: bool
    starred_at: Optional[str] = Field(None, examples=['"2020-07-09T00:17:55Z"'])


class MilestoneItem(BaseModel):
    url: AnyUrl = Field(
        ..., examples=['https://api.github.com/repos/octocat/Hello-World/milestones/1']
    )
    html_url: AnyUrl = Field(
        ..., examples=['https://github.com/octocat/Hello-World/milestones/v1.0']
    )
    labels_url: AnyUrl = Field(
        ...,
        examples=[
            'https://api.github.com/repos/octocat/Hello-World/milestones/1/labels'
        ],
    )
    id: int = Field(..., examples=[1002604])
    node_id: str = Field(..., examples=['MDk6TWlsZXN0b25lMTAwMjYwNA=='])
    number: int = Field(..., description='The number of the milestone.', examples=[42])
    state: State = Field(
        ..., description='The state of the milestone.', examples=['open']
    )
    title: str = Field(
        ..., description='The title of the milestone.', examples=['v1.0']
    )
    description: Optional[str] = Field(
        ..., examples=['Tracking milestone for version 1.0']
    )
    creator: Optional[CreatorItem]
    open_issues: int = Field(..., examples=[4])
    closed_issues: int = Field(..., examples=[8])
    created_at: datetime = Field(..., examples=['2011-04-10T20:09:31Z'])
    updated_at: datetime = Field(..., examples=['2014-03-03T18:58:10Z'])
    closed_at: Optional[datetime] = Field(..., examples=['2013-02-12T13:22:01Z'])
    due_on: Optional[datetime] = Field(..., examples=['2012-10-09T23:39:01Z'])


class PullRequest(BaseModel):
    merged_at: Optional[datetime] = None
    diff_url: Optional[AnyUrl]
    html_url: Optional[AnyUrl]
    patch_url: Optional[AnyUrl]
    url: Optional[AnyUrl]


class ClosedByItem(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    login: str = Field(..., examples=['octocat'])
    id: int = Field(..., examples=[1])
    node_id: str = Field(..., examples=['MDQ6VXNlcjE='])
    avatar_url: AnyUrl = Field(
        ..., examples=['https://github.com/images/error/octocat_happy.gif']
    )
    gravatar_id: Optional[str] = Field(
        ..., examples=['41d064eb2195891e12d0413f63227ea7']
    )
    url: AnyUrl = Field(..., examples=['https://api.github.com/users/octocat'])
    html_url: AnyUrl = Field(..., examples=['https://github.com/octocat'])
    followers_url: AnyUrl = Field(
        ..., examples=['https://api.github.com/users/octocat/followers']
    )
    following_url: str = Field(
        ..., examples=['https://api.github.com/users/octocat/following{/other_user}']
    )
    gists_url: str = Field(
        ..., examples=['https://api.github.com/users/octocat/gists{/gist_id}']
    )
    starred_url: str = Field(
        ..., examples=['https://api.github.com/users/octocat/starred{/owner}{/repo}']
    )
    subscriptions_url: AnyUrl = Field(
        ..., examples=['https://api.github.com/users/octocat/subscriptions']
    )
    organizations_url: AnyUrl = Field(
        ..., examples=['https://api.github.com/users/octocat/orgs']
    )
    repos_url: AnyUrl = Field(
        ..., examples=['https://api.github.com/users/octocat/repos']
    )
    events_url: str = Field(
        ..., examples=['https://api.github.com/users/octocat/events{/privacy}']
    )
    received_events_url: AnyUrl = Field(
        ..., examples=['https://api.github.com/users/octocat/received_events']
    )
    type: str = Field(..., examples=['User'])
    site_admin: bool
    starred_at: Optional[str] = Field(None, examples=['"2020-07-09T00:17:55Z"'])


class LicenseItem(BaseModel):
    key: str = Field(..., examples=['mit'])
    name: str = Field(..., examples=['MIT License'])
    url: Optional[AnyUrl] = Field(..., examples=['https://api.github.com/licenses/mit'])
    spdx_id: Optional[str] = Field(..., examples=['MIT'])
    node_id: str = Field(..., examples=['MDc6TGljZW5zZW1pdA=='])
    html_url: Optional[AnyUrl] = None


class OrganizationItem(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    login: str = Field(..., examples=['octocat'])
    id: int = Field(..., examples=[1])
    node_id: str = Field(..., examples=['MDQ6VXNlcjE='])
    avatar_url: AnyUrl = Field(
        ..., examples=['https://github.com/images/error/octocat_happy.gif']
    )
    gravatar_id: Optional[str] = Field(
        ..., examples=['41d064eb2195891e12d0413f63227ea7']
    )
    url: AnyUrl = Field(..., examples=['https://api.github.com/users/octocat'])
    html_url: AnyUrl = Field(..., examples=['https://github.com/octocat'])
    followers_url: AnyUrl = Field(
        ..., examples=['https://api.github.com/users/octocat/followers']
    )
    following_url: str = Field(
        ..., examples=['https://api.github.com/users/octocat/following{/other_user}']
    )
    gists_url: str = Field(
        ..., examples=['https://api.github.com/users/octocat/gists{/gist_id}']
    )
    starred_url: str = Field(
        ..., examples=['https://api.github.com/users/octocat/starred{/owner}{/repo}']
    )
    subscriptions_url: AnyUrl = Field(
        ..., examples=['https://api.github.com/users/octocat/subscriptions']
    )
    organizations_url: AnyUrl = Field(
        ..., examples=['https://api.github.com/users/octocat/orgs']
    )
    repos_url: AnyUrl = Field(
        ..., examples=['https://api.github.com/users/octocat/repos']
    )
    events_url: str = Field(
        ..., examples=['https://api.github.com/users/octocat/events{/privacy}']
    )
    received_events_url: AnyUrl = Field(
        ..., examples=['https://api.github.com/users/octocat/received_events']
    )
    type: str = Field(..., examples=['User'])
    site_admin: bool
    starred_at: Optional[str] = Field(None, examples=['"2020-07-09T00:17:55Z"'])


class Permissions(BaseModel):
    admin: bool
    pull: bool
    triage: Optional[bool] = None
    push: bool
    maintain: Optional[bool] = None


class Owner(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    login: str = Field(..., examples=['octocat'])
    id: int = Field(..., examples=[1])
    node_id: str = Field(..., examples=['MDQ6VXNlcjE='])
    avatar_url: AnyUrl = Field(
        ..., examples=['https://github.com/images/error/octocat_happy.gif']
    )
    gravatar_id: Optional[str] = Field(
        ..., examples=['41d064eb2195891e12d0413f63227ea7']
    )
    url: AnyUrl = Field(..., examples=['https://api.github.com/users/octocat'])
    html_url: AnyUrl = Field(..., examples=['https://github.com/octocat'])
    followers_url: AnyUrl = Field(
        ..., examples=['https://api.github.com/users/octocat/followers']
    )
    following_url: str = Field(
        ..., examples=['https://api.github.com/users/octocat/following{/other_user}']
    )
    gists_url: str = Field(
        ..., examples=['https://api.github.com/users/octocat/gists{/gist_id}']
    )
    starred_url: str = Field(
        ..., examples=['https://api.github.com/users/octocat/starred{/owner}{/repo}']
    )
    subscriptions_url: AnyUrl = Field(
        ..., examples=['https://api.github.com/users/octocat/subscriptions']
    )
    organizations_url: AnyUrl = Field(
        ..., examples=['https://api.github.com/users/octocat/orgs']
    )
    repos_url: AnyUrl = Field(
        ..., examples=['https://api.github.com/users/octocat/repos']
    )
    events_url: str = Field(
        ..., examples=['https://api.github.com/users/octocat/events{/privacy}']
    )
    received_events_url: AnyUrl = Field(
        ..., examples=['https://api.github.com/users/octocat/received_events']
    )
    type: str = Field(..., examples=['User'])
    site_admin: bool
    starred_at: Optional[str] = Field(None, examples=['"2020-07-09T00:17:55Z"'])


class Owner1(BaseModel):
    login: Optional[str] = None
    id: Optional[int] = None
    node_id: Optional[str] = None
    avatar_url: Optional[str] = None
    gravatar_id: Optional[str] = None
    url: Optional[str] = None
    html_url: Optional[str] = None
    followers_url: Optional[str] = None
    following_url: Optional[str] = None
    gists_url: Optional[str] = None
    starred_url: Optional[str] = None
    subscriptions_url: Optional[str] = None
    organizations_url: Optional[str] = None
    repos_url: Optional[str] = None
    events_url: Optional[str] = None
    received_events_url: Optional[str] = None
    type: Optional[str] = None
    site_admin: Optional[bool] = None


class Permissions1(BaseModel):
    admin: Optional[bool] = None
    maintain: Optional[bool] = None
    push: Optional[bool] = None
    triage: Optional[bool] = None
    pull: Optional[bool] = None


class SquashMergeCommitTitle(Enum):
    PR_TITLE = 'PR_TITLE'
    COMMIT_OR_PR_TITLE = 'COMMIT_OR_PR_TITLE'


class SquashMergeCommitMessage(Enum):
    PR_BODY = 'PR_BODY'
    COMMIT_MESSAGES = 'COMMIT_MESSAGES'
    BLANK = 'BLANK'


class MergeCommitTitle(Enum):
    PR_TITLE = 'PR_TITLE'
    MERGE_MESSAGE = 'MERGE_MESSAGE'


class MergeCommitMessage(Enum):
    PR_BODY = 'PR_BODY'
    PR_TITLE = 'PR_TITLE'
    BLANK = 'BLANK'


class TemplateRepository(BaseModel):
    id: Optional[int] = None
    node_id: Optional[str] = None
    name: Optional[str] = None
    full_name: Optional[str] = None
    owner: Optional[Owner1] = None
    private: Optional[bool] = None
    html_url: Optional[str] = None
    description: Optional[str] = None
    fork: Optional[bool] = None
    url: Optional[str] = None
    archive_url: Optional[str] = None
    assignees_url: Optional[str] = None
    blobs_url: Optional[str] = None
    branches_url: Optional[str] = None
    collaborators_url: Optional[str] = None
    comments_url: Optional[str] = None
    commits_url: Optional[str] = None
    compare_url: Optional[str] = None
    contents_url: Optional[str] = None
    contributors_url: Optional[str] = None
    deployments_url: Optional[str] = None
    downloads_url: Optional[str] = None
    events_url: Optional[str] = None
    forks_url: Optional[str] = None
    git_commits_url: Optional[str] = None
    git_refs_url: Optional[str] = None
    git_tags_url: Optional[str] = None
    git_url: Optional[str] = None
    issue_comment_url: Optional[str] = None
    issue_events_url: Optional[str] = None
    issues_url: Optional[str] = None
    keys_url: Optional[str] = None
    labels_url: Optional[str] = None
    languages_url: Optional[str] = None
    merges_url: Optional[str] = None
    milestones_url: Optional[str] = None
    notifications_url: Optional[str] = None
    pulls_url: Optional[str] = None
    releases_url: Optional[str] = None
    ssh_url: Optional[str] = None
    stargazers_url: Optional[str] = None
    statuses_url: Optional[str] = None
    subscribers_url: Optional[str] = None
    subscription_url: Optional[str] = None
    tags_url: Optional[str] = None
    teams_url: Optional[str] = None
    trees_url: Optional[str] = None
    clone_url: Optional[str] = None
    mirror_url: Optional[str] = None
    hooks_url: Optional[str] = None
    svn_url: Optional[str] = None
    homepage: Optional[str] = None
    language: Optional[str] = None
    forks_count: Optional[int] = None
    stargazers_count: Optional[int] = None
    watchers_count: Optional[int] = None
    size: Optional[int] = None
    default_branch: Optional[str] = None
    open_issues_count: Optional[int] = None
    is_template: Optional[bool] = None
    topics: Optional[List[str]] = None
    has_issues: Optional[bool] = None
    has_projects: Optional[bool] = None
    has_wiki: Optional[bool] = None
    has_pages: Optional[bool] = None
    has_downloads: Optional[bool] = None
    archived: Optional[bool] = None
    disabled: Optional[bool] = None
    visibility: Optional[str] = None
    pushed_at: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    permissions: Optional[Permissions1] = None
    allow_rebase_merge: Optional[bool] = None
    temp_clone_token: Optional[str] = None
    allow_squash_merge: Optional[bool] = None
    allow_auto_merge: Optional[bool] = None
    delete_branch_on_merge: Optional[bool] = None
    allow_update_branch: Optional[bool] = None
    use_squash_pr_title_as_default: Optional[bool] = None
    squash_merge_commit_title: Optional[SquashMergeCommitTitle] = Field(
        None,
        description="The default value for a squash merge commit title:\n\n- `PR_TITLE` - default to the pull request's title.\n- `COMMIT_OR_PR_TITLE` - default to the commit's title (if only one commit) or the pull request's title (when more than one commit).",
    )
    squash_merge_commit_message: Optional[SquashMergeCommitMessage] = Field(
        None,
        description="The default value for a squash merge commit message:\n\n- `PR_BODY` - default to the pull request's body.\n- `COMMIT_MESSAGES` - default to the branch's commit messages.\n- `BLANK` - default to a blank commit message.",
    )
    merge_commit_title: Optional[MergeCommitTitle] = Field(
        None,
        description="The default value for a merge commit title.\n\n- `PR_TITLE` - default to the pull request's title.\n- `MERGE_MESSAGE` - default to the classic title for a merge message (e.g., Merge pull request #123 from branch-name).",
    )
    merge_commit_message: Optional[MergeCommitMessage] = Field(
        None,
        description="The default value for a merge commit message.\n\n- `PR_TITLE` - default to the pull request's title.\n- `PR_BODY` - default to the pull request's body.\n- `BLANK` - default to a blank commit message.",
    )
    allow_merge_commit: Optional[bool] = None
    subscribers_count: Optional[int] = None
    network_count: Optional[int] = None


class Repository(BaseModel):
    id: int = Field(
        ..., description='Unique identifier of the repository', examples=[42]
    )
    node_id: str = Field(..., examples=['MDEwOlJlcG9zaXRvcnkxMjk2MjY5'])
    name: str = Field(
        ..., description='The name of the repository.', examples=['Team Environment']
    )
    full_name: str = Field(..., examples=['octocat/Hello-World'])
    license: Optional[LicenseItem]
    organization: Optional[OrganizationItem] = None
    forks: int
    permissions: Optional[Permissions] = None
    owner: Owner = Field(..., description='A GitHub user.', title='Simple User')
    private: bool = Field(
        ..., description='Whether the repository is private or public.'
    )
    html_url: AnyUrl = Field(..., examples=['https://github.com/octocat/Hello-World'])
    description: Optional[str] = Field(..., examples=['This your first repo!'])
    fork: bool
    url: AnyUrl = Field(
        ..., examples=['https://api.github.com/repos/octocat/Hello-World']
    )
    archive_url: str = Field(
        ...,
        examples=[
            'http://api.github.com/repos/octocat/Hello-World/{archive_format}{/ref}'
        ],
    )
    assignees_url: str = Field(
        ...,
        examples=['http://api.github.com/repos/octocat/Hello-World/assignees{/user}'],
    )
    blobs_url: str = Field(
        ...,
        examples=['http://api.github.com/repos/octocat/Hello-World/git/blobs{/sha}'],
    )
    branches_url: str = Field(
        ...,
        examples=['http://api.github.com/repos/octocat/Hello-World/branches{/branch}'],
    )
    collaborators_url: str = Field(
        ...,
        examples=[
            'http://api.github.com/repos/octocat/Hello-World/collaborators{/collaborator}'
        ],
    )
    comments_url: str = Field(
        ...,
        examples=['http://api.github.com/repos/octocat/Hello-World/comments{/number}'],
    )
    commits_url: str = Field(
        ..., examples=['http://api.github.com/repos/octocat/Hello-World/commits{/sha}']
    )
    compare_url: str = Field(
        ...,
        examples=[
            'http://api.github.com/repos/octocat/Hello-World/compare/{base}...{head}'
        ],
    )
    contents_url: str = Field(
        ...,
        examples=['http://api.github.com/repos/octocat/Hello-World/contents/{+path}'],
    )
    contributors_url: AnyUrl = Field(
        ..., examples=['http://api.github.com/repos/octocat/Hello-World/contributors']
    )
    deployments_url: AnyUrl = Field(
        ..., examples=['http://api.github.com/repos/octocat/Hello-World/deployments']
    )
    downloads_url: AnyUrl = Field(
        ..., examples=['http://api.github.com/repos/octocat/Hello-World/downloads']
    )
    events_url: AnyUrl = Field(
        ..., examples=['http://api.github.com/repos/octocat/Hello-World/events']
    )
    forks_url: AnyUrl = Field(
        ..., examples=['http://api.github.com/repos/octocat/Hello-World/forks']
    )
    git_commits_url: str = Field(
        ...,
        examples=['http://api.github.com/repos/octocat/Hello-World/git/commits{/sha}'],
    )
    git_refs_url: str = Field(
        ..., examples=['http://api.github.com/repos/octocat/Hello-World/git/refs{/sha}']
    )
    git_tags_url: str = Field(
        ..., examples=['http://api.github.com/repos/octocat/Hello-World/git/tags{/sha}']
    )
    git_url: str = Field(..., examples=['git:github.com/octocat/Hello-World.git'])
    issue_comment_url: str = Field(
        ...,
        examples=[
            'http://api.github.com/repos/octocat/Hello-World/issues/comments{/number}'
        ],
    )
    issue_events_url: str = Field(
        ...,
        examples=[
            'http://api.github.com/repos/octocat/Hello-World/issues/events{/number}'
        ],
    )
    issues_url: str = Field(
        ...,
        examples=['http://api.github.com/repos/octocat/Hello-World/issues{/number}'],
    )
    keys_url: str = Field(
        ..., examples=['http://api.github.com/repos/octocat/Hello-World/keys{/key_id}']
    )
    labels_url: str = Field(
        ..., examples=['http://api.github.com/repos/octocat/Hello-World/labels{/name}']
    )
    languages_url: AnyUrl = Field(
        ..., examples=['http://api.github.com/repos/octocat/Hello-World/languages']
    )
    merges_url: AnyUrl = Field(
        ..., examples=['http://api.github.com/repos/octocat/Hello-World/merges']
    )
    milestones_url: str = Field(
        ...,
        examples=[
            'http://api.github.com/repos/octocat/Hello-World/milestones{/number}'
        ],
    )
    notifications_url: str = Field(
        ...,
        examples=[
            'http://api.github.com/repos/octocat/Hello-World/notifications{?since,all,participating}'
        ],
    )
    pulls_url: str = Field(
        ..., examples=['http://api.github.com/repos/octocat/Hello-World/pulls{/number}']
    )
    releases_url: str = Field(
        ..., examples=['http://api.github.com/repos/octocat/Hello-World/releases{/id}']
    )
    ssh_url: str = Field(..., examples=['git@github.com:octocat/Hello-World.git'])
    stargazers_url: AnyUrl = Field(
        ..., examples=['http://api.github.com/repos/octocat/Hello-World/stargazers']
    )
    statuses_url: str = Field(
        ..., examples=['http://api.github.com/repos/octocat/Hello-World/statuses/{sha}']
    )
    subscribers_url: AnyUrl = Field(
        ..., examples=['http://api.github.com/repos/octocat/Hello-World/subscribers']
    )
    subscription_url: AnyUrl = Field(
        ..., examples=['http://api.github.com/repos/octocat/Hello-World/subscription']
    )
    tags_url: AnyUrl = Field(
        ..., examples=['http://api.github.com/repos/octocat/Hello-World/tags']
    )
    teams_url: AnyUrl = Field(
        ..., examples=['http://api.github.com/repos/octocat/Hello-World/teams']
    )
    trees_url: str = Field(
        ...,
        examples=['http://api.github.com/repos/octocat/Hello-World/git/trees{/sha}'],
    )
    clone_url: str = Field(..., examples=['https://github.com/octocat/Hello-World.git'])
    mirror_url: Optional[AnyUrl] = Field(
        ..., examples=['git:git.example.com/octocat/Hello-World']
    )
    hooks_url: AnyUrl = Field(
        ..., examples=['http://api.github.com/repos/octocat/Hello-World/hooks']
    )
    svn_url: AnyUrl = Field(
        ..., examples=['https://svn.github.com/octocat/Hello-World']
    )
    homepage: Optional[AnyUrl] = Field(..., examples=['https://github.com'])
    language: Optional[str]
    forks_count: int = Field(..., examples=[9])
    stargazers_count: int = Field(..., examples=[80])
    watchers_count: int = Field(..., examples=[80])
    size: int = Field(
        ...,
        description='The size of the repository. Size is calculated hourly. When a repository is initially created, the size is 0.',
        examples=[108],
    )
    default_branch: str = Field(
        ..., description='The default branch of the repository.', examples=['master']
    )
    open_issues_count: int = Field(..., examples=[0])
    is_template: Optional[bool] = Field(
        False,
        description='Whether this repository acts as a template that can be used to generate new repositories.',
        examples=[True],
    )
    topics: Optional[List[str]] = None
    has_issues: bool = Field(
        ..., description='Whether issues are enabled.', examples=[True]
    )
    has_projects: bool = Field(
        ..., description='Whether projects are enabled.', examples=[True]
    )
    has_wiki: bool = Field(
        ..., description='Whether the wiki is enabled.', examples=[True]
    )
    has_pages: bool
    has_downloads: bool = Field(
        ..., description='Whether downloads are enabled.', examples=[True]
    )
    has_discussions: Optional[bool] = Field(
        False, description='Whether discussions are enabled.', examples=[True]
    )
    archived: bool = Field(..., description='Whether the repository is archived.')
    disabled: bool = Field(
        ..., description='Returns whether or not this repository disabled.'
    )
    visibility: Optional[str] = Field(
        'public', description='The repository visibility: public, private, or internal.'
    )
    pushed_at: Optional[datetime] = Field(..., examples=['2011-01-26T19:06:43Z'])
    created_at: Optional[datetime] = Field(..., examples=['2011-01-26T19:01:12Z'])
    updated_at: Optional[datetime] = Field(..., examples=['2011-01-26T19:14:43Z'])
    allow_rebase_merge: Optional[bool] = Field(
        True,
        description='Whether to allow rebase merges for pull requests.',
        examples=[True],
    )
    template_repository: Optional[TemplateRepository] = None
    temp_clone_token: Optional[str] = None
    allow_squash_merge: Optional[bool] = Field(
        True,
        description='Whether to allow squash merges for pull requests.',
        examples=[True],
    )
    allow_auto_merge: Optional[bool] = Field(
        False,
        description='Whether to allow Auto-merge to be used on pull requests.',
        examples=[False],
    )
    delete_branch_on_merge: Optional[bool] = Field(
        False,
        description='Whether to delete head branches when pull requests are merged',
        examples=[False],
    )
    allow_update_branch: Optional[bool] = Field(
        False,
        description='Whether or not a pull request head branch that is behind its base branch can always be updated even if it is not required to be up to date before merging.',
        examples=[False],
    )
    use_squash_pr_title_as_default: Optional[bool] = Field(
        False,
        description='Whether a squash merge commit can use the pull request title as default. **This property has been deprecated. Please use `squash_merge_commit_title` instead.',
    )
    squash_merge_commit_title: Optional[SquashMergeCommitTitle] = Field(
        None,
        description="The default value for a squash merge commit title:\n\n- `PR_TITLE` - default to the pull request's title.\n- `COMMIT_OR_PR_TITLE` - default to the commit's title (if only one commit) or the pull request's title (when more than one commit).",
    )
    squash_merge_commit_message: Optional[SquashMergeCommitMessage] = Field(
        None,
        description="The default value for a squash merge commit message:\n\n- `PR_BODY` - default to the pull request's body.\n- `COMMIT_MESSAGES` - default to the branch's commit messages.\n- `BLANK` - default to a blank commit message.",
    )
    merge_commit_title: Optional[MergeCommitTitle] = Field(
        None,
        description="The default value for a merge commit title.\n\n- `PR_TITLE` - default to the pull request's title.\n- `MERGE_MESSAGE` - default to the classic title for a merge message (e.g., Merge pull request #123 from branch-name).",
    )
    merge_commit_message: Optional[MergeCommitMessage] = Field(
        None,
        description="The default value for a merge commit message.\n\n- `PR_TITLE` - default to the pull request's title.\n- `PR_BODY` - default to the pull request's body.\n- `BLANK` - default to a blank commit message.",
    )
    allow_merge_commit: Optional[bool] = Field(
        True,
        description='Whether to allow merge commits for pull requests.',
        examples=[True],
    )
    allow_forking: Optional[bool] = Field(
        None, description='Whether to allow forking this repo'
    )
    web_commit_signoff_required: Optional[bool] = Field(
        False,
        description='Whether to require contributors to sign off on web-based commits',
    )
    subscribers_count: Optional[int] = None
    network_count: Optional[int] = None
    open_issues: int
    watchers: int
    master_branch: Optional[str] = None
    starred_at: Optional[str] = Field(None, examples=['"2020-07-09T00:17:42Z"'])
    anonymous_access_enabled: Optional[bool] = Field(
        None, description='Whether anonymous git access is enabled for this repository'
    )


class OwnerItem(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    login: str = Field(..., examples=['octocat'])
    id: int = Field(..., examples=[1])
    node_id: str = Field(..., examples=['MDQ6VXNlcjE='])
    avatar_url: AnyUrl = Field(
        ..., examples=['https://github.com/images/error/octocat_happy.gif']
    )
    gravatar_id: Optional[str] = Field(
        ..., examples=['41d064eb2195891e12d0413f63227ea7']
    )
    url: AnyUrl = Field(..., examples=['https://api.github.com/users/octocat'])
    html_url: AnyUrl = Field(..., examples=['https://github.com/octocat'])
    followers_url: AnyUrl = Field(
        ..., examples=['https://api.github.com/users/octocat/followers']
    )
    following_url: str = Field(
        ..., examples=['https://api.github.com/users/octocat/following{/other_user}']
    )
    gists_url: str = Field(
        ..., examples=['https://api.github.com/users/octocat/gists{/gist_id}']
    )
    starred_url: str = Field(
        ..., examples=['https://api.github.com/users/octocat/starred{/owner}{/repo}']
    )
    subscriptions_url: AnyUrl = Field(
        ..., examples=['https://api.github.com/users/octocat/subscriptions']
    )
    organizations_url: AnyUrl = Field(
        ..., examples=['https://api.github.com/users/octocat/orgs']
    )
    repos_url: AnyUrl = Field(
        ..., examples=['https://api.github.com/users/octocat/repos']
    )
    events_url: str = Field(
        ..., examples=['https://api.github.com/users/octocat/events{/privacy}']
    )
    received_events_url: AnyUrl = Field(
        ..., examples=['https://api.github.com/users/octocat/received_events']
    )
    type: str = Field(..., examples=['User'])
    site_admin: bool
    starred_at: Optional[str] = Field(None, examples=['"2020-07-09T00:17:55Z"'])


class Permissions2(BaseModel):
    issues: Optional[str] = None
    checks: Optional[str] = None
    metadata: Optional[str] = None
    contents: Optional[str] = None
    deployments: Optional[str] = None


class PerformedViaGithubAppItem(BaseModel):
    id: int = Field(
        ..., description='Unique identifier of the GitHub app', examples=[37]
    )
    slug: Optional[str] = Field(
        None, description='The slug name of the GitHub app', examples=['probot-owners']
    )
    node_id: str = Field(..., examples=['MDExOkludGVncmF0aW9uMQ=='])
    owner: Optional[OwnerItem]
    name: str = Field(
        ..., description='The name of the GitHub app', examples=['Probot Owners']
    )
    description: Optional[str] = Field(..., examples=['The description of the app.'])
    external_url: AnyUrl = Field(..., examples=['https://example.com'])
    html_url: AnyUrl = Field(..., examples=['https://github.com/apps/super-ci'])
    created_at: datetime = Field(..., examples=['2017-07-08T16:18:44-04:00'])
    updated_at: datetime = Field(..., examples=['2017-07-08T16:18:44-04:00'])
    permissions: Permissions2 = Field(
        ...,
        description='The set of permissions for the GitHub app',
        example={'issues': 'read', 'deployments': 'write'},
    )
    events: List[str] = Field(
        ...,
        description='The list of events for the GitHub app',
        examples=['label', 'deployment'],
    )
    installations_count: Optional[int] = Field(
        None,
        description='The number of installations associated with the GitHub app',
        examples=[5],
    )
    client_id: Optional[str] = Field(None, examples=['"Iv1.25b5d1e65ffc4022"'])
    client_secret: Optional[str] = Field(
        None, examples=['"1d4b2097ac622ba702d19de498f005747a8b21d3"']
    )
    webhook_secret: Optional[str] = Field(
        None, examples=['"6fba8f2fc8a7e8f2cca5577eddd82ca7586b3b6b"']
    )
    pem: Optional[str] = Field(
        None,
        examples=[
            '"-----BEGIN RSA PRIVATE KEY-----\\nMIIEogIBAAKCAQEArYxrNYD/iT5CZVpRJu4rBKmmze3PVmT/gCo2ATUvDvZTPTey\\nxcGJ3vvrJXazKk06pN05TN29o98jrYz4cengG3YGsXPNEpKsIrEl8NhbnxapEnM9\\nJCMRe0P5JcPsfZlX6hmiT7136GRWiGOUba2X9+HKh8QJVLG5rM007TBER9/z9mWm\\nrJuNh+m5l320oBQY/Qq3A7wzdEfZw8qm/mIN0FCeoXH1L6B8xXWaAYBwhTEh6SSn\\nZHlO1Xu1JWDmAvBCi0RO5aRSKM8q9QEkvvHP4yweAtK3N8+aAbZ7ovaDhyGz8r6r\\nzhU1b8Uo0Z2ysf503WqzQgIajr7Fry7/kUwpgQIDAQABAoIBADwJp80Ko1xHPZDy\\nfcCKBDfIuPvkmSW6KumbsLMaQv1aGdHDwwTGv3t0ixSay8CGlxMRtRDyZPib6SvQ\\n6OH/lpfpbMdW2ErkksgtoIKBVrDilfrcAvrNZu7NxRNbhCSvN8q0s4ICecjbbVQh\\nnueSdlA6vGXbW58BHMq68uRbHkP+k+mM9U0mDJ1HMch67wlg5GbayVRt63H7R2+r\\nVxcna7B80J/lCEjIYZznawgiTvp3MSanTglqAYi+m1EcSsP14bJIB9vgaxS79kTu\\noiSo93leJbBvuGo8QEiUqTwMw4tDksmkLsoqNKQ1q9P7LZ9DGcujtPy4EZsamSJT\\ny8OJt0ECgYEA2lxOxJsQk2kI325JgKFjo92mQeUObIvPfSNWUIZQDTjniOI6Gv63\\nGLWVFrZcvQBWjMEQraJA9xjPbblV8PtfO87MiJGLWCHFxmPz2dzoedN+2Coxom8m\\nV95CLz8QUShuao6u/RYcvUaZEoYs5bHcTmy5sBK80JyEmafJPtCQVxMCgYEAy3ar\\nZr3yv4xRPEPMat4rseswmuMooSaK3SKub19WFI5IAtB/e7qR1Rj9JhOGcZz+OQrl\\nT78O2OFYlgOIkJPvRMrPpK5V9lslc7tz1FSh3BZMRGq5jSyD7ETSOQ0c8T2O/s7v\\nbeEPbVbDe4mwvM24XByH0GnWveVxaDl51ABD65sCgYB3ZAspUkOA5egVCh8kNpnd\\nSd6SnuQBE3ySRlT2WEnCwP9Ph6oPgn+oAfiPX4xbRqkL8q/k0BdHQ4h+zNwhk7+h\\nWtPYRAP1Xxnc/F+jGjb+DVaIaKGU18MWPg7f+FI6nampl3Q0KvfxwX0GdNhtio8T\\nTj1E+SnFwh56SRQuxSh2gwKBgHKjlIO5NtNSflsUYFM+hyQiPiqnHzddfhSG+/3o\\nm5nNaSmczJesUYreH5San7/YEy2UxAugvP7aSY2MxB+iGsiJ9WD2kZzTUlDZJ7RV\\nUzWsoqBR+eZfVJ2FUWWvy8TpSG6trh4dFxImNtKejCR1TREpSiTV3Zb1dmahK9GV\\nrK9NAoGAbBxRLoC01xfxCTgt5BDiBcFVh4fp5yYKwavJPLzHSpuDOrrI9jDn1oKN\\nonq5sDU1i391zfQvdrbX4Ova48BN+B7p63FocP/MK5tyyBoT8zQEk2+vWDOw7H/Z\\nu5dTCPxTIsoIwUw1I+7yIxqJzLPFgR2gVBwY1ra/8iAqCj+zeBw=\\n-----END RSA PRIVATE KEY-----\\n"'
        ],
    )


class AuthorAssociation(Enum):
    COLLABORATOR = 'COLLABORATOR'
    CONTRIBUTOR = 'CONTRIBUTOR'
    FIRST_TIMER = 'FIRST_TIMER'
    FIRST_TIME_CONTRIBUTOR = 'FIRST_TIME_CONTRIBUTOR'
    MANNEQUIN = 'MANNEQUIN'
    MEMBER = 'MEMBER'
    NONE = 'NONE'
    OWNER = 'OWNER'


class Reactions(BaseModel):
    url: AnyUrl
    total_count: int
    field_1: int = Field(..., alias='+1')
    field_1_1: int = Field(..., alias='-1')
    laugh: int
    confused: int
    heart: int
    hooray: int
    eyes: int
    rocket: int


class Issue(BaseModel):
    id: int
    node_id: str
    url: AnyUrl = Field(
        ...,
        description='URL for the issue',
        examples=['https://api.github.com/repositories/42/issues/1'],
    )
    repository_url: AnyUrl
    labels_url: str
    comments_url: AnyUrl
    events_url: AnyUrl
    html_url: AnyUrl
    number: int = Field(
        ...,
        description='Number uniquely identifying the issue within its repository',
        examples=[42],
    )
    state: str = Field(
        ...,
        description="State of the issue; either 'open' or 'closed'",
        examples=['open'],
    )
    state_reason: Optional[StateReason] = Field(
        None, description='The reason for the current state', examples=['not_planned']
    )
    title: str = Field(
        ...,
        description='Title of the issue',
        examples=['Widget creation fails in Safari on OS X 10.8'],
    )
    body: Optional[str] = Field(
        None,
        description='Contents of the issue',
        examples=[
            'It looks like the new widget form is broken on Safari. When I try and create the widget, Safari crashes. This is reproducible on 10.8, but not 10.9. Maybe a browser bug?'
        ],
    )
    user: Optional[UserItem]
    labels: List[Union[str, Label]] = Field(
        ...,
        description='Labels to associate with this issue; pass one or more label names to replace the set of labels on this issue; send an empty array to clear all labels from the issue; note that the labels are silently dropped for users without push access to the repository',
        examples=['bug', 'registration'],
    )
    assignee: Optional[AssigneeItem]
    assignees: Optional[List[Assignee]] = None
    milestone: Optional[MilestoneItem]
    locked: bool
    active_lock_reason: Optional[str] = None
    comments: int
    pull_request: Optional[PullRequest] = None
    closed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    draft: Optional[bool] = None
    closed_by: Optional[ClosedByItem] = None
    body_html: Optional[str] = None
    body_text: Optional[str] = None
    timeline_url: Optional[AnyUrl] = None
    repository: Optional[Repository] = Field(
        None, description='A repository on GitHub.', title='Repository'
    )
    performed_via_github_app: Optional[PerformedViaGithubAppItem] = None
    author_association: AuthorAssociation = Field(
        ...,
        description='How the author is associated with the repository.',
        examples=['OWNER'],
        title='author_association',
    )
    reactions: Optional[Reactions] = Field(None, title='Reaction Rollup')


class PerformedViaGithubAppItem1(BaseModel):
    id: int = Field(
        ..., description='Unique identifier of the GitHub app', examples=[37]
    )
    slug: Optional[str] = Field(
        None, description='The slug name of the GitHub app', examples=['probot-owners']
    )
    node_id: str = Field(..., examples=['MDExOkludGVncmF0aW9uMQ=='])
    owner: Optional[OwnerItem]
    name: str = Field(
        ..., description='The name of the GitHub app', examples=['Probot Owners']
    )
    description: Optional[str] = Field(..., examples=['The description of the app.'])
    external_url: AnyUrl = Field(..., examples=['https://example.com'])
    html_url: AnyUrl = Field(..., examples=['https://github.com/apps/super-ci'])
    created_at: datetime = Field(..., examples=['2017-07-08T16:18:44-04:00'])
    updated_at: datetime = Field(..., examples=['2017-07-08T16:18:44-04:00'])
    permissions: Permissions2 = Field(
        ...,
        description='The set of permissions for the GitHub app',
        example={'issues': 'read', 'deployments': 'write'},
    )
    events: List[str] = Field(
        ...,
        description='The list of events for the GitHub app',
        examples=['label', 'deployment'],
    )
    installations_count: Optional[int] = Field(
        None,
        description='The number of installations associated with the GitHub app',
        examples=[5],
    )
    client_id: Optional[str] = Field(None, examples=['"Iv1.25b5d1e65ffc4022"'])
    client_secret: Optional[str] = Field(
        None, examples=['"1d4b2097ac622ba702d19de498f005747a8b21d3"']
    )
    webhook_secret: Optional[str] = Field(
        None, examples=['"6fba8f2fc8a7e8f2cca5577eddd82ca7586b3b6b"']
    )
    pem: Optional[str] = Field(
        None,
        examples=[
            '"-----BEGIN RSA PRIVATE KEY-----\\nMIIEogIBAAKCAQEArYxrNYD/iT5CZVpRJu4rBKmmze3PVmT/gCo2ATUvDvZTPTey\\nxcGJ3vvrJXazKk06pN05TN29o98jrYz4cengG3YGsXPNEpKsIrEl8NhbnxapEnM9\\nJCMRe0P5JcPsfZlX6hmiT7136GRWiGOUba2X9+HKh8QJVLG5rM007TBER9/z9mWm\\nrJuNh+m5l320oBQY/Qq3A7wzdEfZw8qm/mIN0FCeoXH1L6B8xXWaAYBwhTEh6SSn\\nZHlO1Xu1JWDmAvBCi0RO5aRSKM8q9QEkvvHP4yweAtK3N8+aAbZ7ovaDhyGz8r6r\\nzhU1b8Uo0Z2ysf503WqzQgIajr7Fry7/kUwpgQIDAQABAoIBADwJp80Ko1xHPZDy\\nfcCKBDfIuPvkmSW6KumbsLMaQv1aGdHDwwTGv3t0ixSay8CGlxMRtRDyZPib6SvQ\\n6OH/lpfpbMdW2ErkksgtoIKBVrDilfrcAvrNZu7NxRNbhCSvN8q0s4ICecjbbVQh\\nnueSdlA6vGXbW58BHMq68uRbHkP+k+mM9U0mDJ1HMch67wlg5GbayVRt63H7R2+r\\nVxcna7B80J/lCEjIYZznawgiTvp3MSanTglqAYi+m1EcSsP14bJIB9vgaxS79kTu\\noiSo93leJbBvuGo8QEiUqTwMw4tDksmkLsoqNKQ1q9P7LZ9DGcujtPy4EZsamSJT\\ny8OJt0ECgYEA2lxOxJsQk2kI325JgKFjo92mQeUObIvPfSNWUIZQDTjniOI6Gv63\\nGLWVFrZcvQBWjMEQraJA9xjPbblV8PtfO87MiJGLWCHFxmPz2dzoedN+2Coxom8m\\nV95CLz8QUShuao6u/RYcvUaZEoYs5bHcTmy5sBK80JyEmafJPtCQVxMCgYEAy3ar\\nZr3yv4xRPEPMat4rseswmuMooSaK3SKub19WFI5IAtB/e7qR1Rj9JhOGcZz+OQrl\\nT78O2OFYlgOIkJPvRMrPpK5V9lslc7tz1FSh3BZMRGq5jSyD7ETSOQ0c8T2O/s7v\\nbeEPbVbDe4mwvM24XByH0GnWveVxaDl51ABD65sCgYB3ZAspUkOA5egVCh8kNpnd\\nSd6SnuQBE3ySRlT2WEnCwP9Ph6oPgn+oAfiPX4xbRqkL8q/k0BdHQ4h+zNwhk7+h\\nWtPYRAP1Xxnc/F+jGjb+DVaIaKGU18MWPg7f+FI6nampl3Q0KvfxwX0GdNhtio8T\\nTj1E+SnFwh56SRQuxSh2gwKBgHKjlIO5NtNSflsUYFM+hyQiPiqnHzddfhSG+/3o\\nm5nNaSmczJesUYreH5San7/YEy2UxAugvP7aSY2MxB+iGsiJ9WD2kZzTUlDZJ7RV\\nUzWsoqBR+eZfVJ2FUWWvy8TpSG6trh4dFxImNtKejCR1TREpSiTV3Zb1dmahK9GV\\nrK9NAoGAbBxRLoC01xfxCTgt5BDiBcFVh4fp5yYKwavJPLzHSpuDOrrI9jDn1oKN\\nonq5sDU1i391zfQvdrbX4Ova48BN+B7p63FocP/MK5tyyBoT8zQEk2+vWDOw7H/Z\\nu5dTCPxTIsoIwUw1I+7yIxqJzLPFgR2gVBwY1ra/8iAqCj+zeBw=\\n-----END RSA PRIVATE KEY-----\\n"'
        ],
    )


class Comment(BaseModel):
    id: int = Field(
        ..., description='Unique identifier of the issue comment', examples=[42]
    )
    node_id: str
    url: AnyUrl = Field(
        ...,
        description='URL for the issue comment',
        examples=['https://api.github.com/repositories/42/issues/comments/1'],
    )
    body: Optional[str] = Field(
        None,
        description='Contents of the issue comment',
        examples=['What version of Safari were you using when you observed this bug?'],
    )
    body_text: Optional[str] = None
    body_html: Optional[str] = None
    html_url: AnyUrl
    user: Optional[UserItem]
    created_at: datetime = Field(..., examples=['2011-04-14T16:00:49Z'])
    updated_at: datetime = Field(..., examples=['2011-04-14T16:00:49Z'])
    issue_url: AnyUrl
    author_association: AuthorAssociation = Field(
        ...,
        description='How the author is associated with the repository.',
        examples=['OWNER'],
        title='author_association',
    )
    performed_via_github_app: Optional[PerformedViaGithubAppItem1] = None
    reactions: Optional[Reactions] = Field(None, title='Reaction Rollup')


class Page(BaseModel):
    page_name: Optional[str] = None
    title: Optional[str] = None
    summary: Optional[str] = None
    action: Optional[str] = None
    sha: Optional[str] = None
    html_url: Optional[str] = None


class Payload(BaseModel):
    action: Optional[str] = None
    issue: Optional[Issue] = Field(
        None,
        description='Issues are a great way to keep track of tasks, enhancements, and bugs for your projects.',
        title='Issue',
    )
    comment: Optional[Comment] = Field(
        None,
        description='Comments provide a way for people to collaborate on an issue.',
        title='Issue Comment',
    )
    pages: Optional[List[Page]] = None


class ModelItem(BaseModel):
    id: str
    type: Optional[str]
    actor: Actor = Field(..., description='Actor', title='Actor')
    repo: Repo
    org: Optional[Org] = Field(None, description='Actor', title='Actor')
    payload: Payload
    public: bool
    created_at: Optional[datetime]


class Model(BaseModel):
    __root__: List[ModelItem]
