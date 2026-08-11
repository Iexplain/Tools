# -*- coding: utf-8 -*-
"""用 leetcode.cn GraphQL 补齐 Top 150 独有题的中文标题（translatedTitle）"""
import json, os, time, urllib.request

os.chdir(os.path.dirname(os.path.abspath(__file__)))

qs = json.load(open('questions.json', encoding='utf-8'))

def _has_cn(s):
    return any('\u4e00' <= c <= '\u9fff' for c in s)

missing = [x for x in qs if x['lists'] == ['top150'] and not _has_cn(x['title'])]
print('missing cn title:', len(missing))

def fetch(slug):
    body = json.dumps({
        "operationName": "getQuestionDetail",
        "variables": {"titleSlug": slug},
        "query": "query getQuestionDetail($titleSlug: String!) { question(titleSlug: $titleSlug) { translatedTitle titleSlug } }"
    }).encode()
    req = urllib.request.Request("https://leetcode.cn/graphql", data=body, headers={
        "Content-Type": "application/json",
        "Origin": "https://leetcode.cn",
        "Referer": "https://leetcode.cn/problems/" + slug + "/",
        "User-Agent": "Mozilla/5.0",
    })
    with urllib.request.urlopen(req, timeout=15) as r:
        d = json.loads(r.read().decode())
    return d['data']['question']['translatedTitle']

ok = fail = 0
for i, x in enumerate(missing):
    try:
        t = fetch(x['slug'])
        if t:
            x['title'] = t
            ok += 1
        else:
            fail += 1
    except Exception as e:
        fail += 1
        print('FAIL', x['id'], x['slug'], e)
    time.sleep(0.25)

with open('questions.json', 'w', encoding='utf-8') as f:
    json.dump(qs, f, ensure_ascii=False, separators=(',', ':'))

print('ok:', ok, 'fail:', fail)
print('remaining non-cn:', len([x for x in qs if not _has_cn(x['title'])]))
