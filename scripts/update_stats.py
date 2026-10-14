"""Refreshes the GitHub Stats lines in dark_mode.svg / light_mode.svg."""
import os, re, requests

USER = os.environ["GH_USER"]
HEAD = {"Authorization": f"Bearer {os.environ['GH_TOKEN']}", "Accept": "application/vnd.github+json"}

def get(url, **kw):
    r = requests.get(url, headers=HEAD, **kw); r.raise_for_status(); return r

user = get(f"https://api.github.com/users/{USER}").json()
repos, page, stars = [], 1, 0
while True:
    batch = get(f"https://api.github.com/users/{USER}/repos", params={"per_page": 100, "page": page, "type": "owner"}).json()
    if not batch: break
    repos += batch; page += 1
stars = sum(r["stargazers_count"] for r in repos)
commits = get("https://api.github.com/search/commits", params={"q": f"author:{USER}", "per_page": 1}).json().get("total_count", 0)

values = {"repo_data": user["public_repos"], "star_data": stars,
          "follower_data": user["followers"], "commit_data": commits}

for f in ("dark_mode.svg", "light_mode.svg"):
    s = open(f).read()
    for k, v in values.items():
        s = re.sub(rf'(<tspan id="{k}"[^>]*>)[^<]*(</tspan>)', rf'\g<1>{v:,}\g<2>', s)
    open(f, "w").write(s)
print("updated", values)
