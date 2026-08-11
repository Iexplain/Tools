# -*- coding: utf-8 -*-
"""构建 LeetTrack 题库数据：Hot 100 + Top Interview 150 合并去重
数据源：
- lc_com_all.json  国际站全量（slug + difficulty）
- lc_cn_all.json   中国站全量（中文标题）
- hot100_raw.json  Hot 100 题单（含中文分类）
- t150_readme.md   Top Interview 150 题单（含难度/分类/标签）
输出：questions.json
"""
import json, re, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ---------- 1. 国际站：slug + 难度 ----------
com = json.load(open('lc_com_all.json', encoding='utf-8'))
com_map = {}
for p in com['stat_status_pairs']:
    st = p['stat']
    fid = str(st['frontend_question_id'])
    lvl = p['difficulty']['level']
    com_map[fid] = {'slug': st['question__title_slug'], 'diff': ['Easy', 'Medium', 'Hard'][lvl - 1]}

# ---------- 2. 中国站：中文标题 ----------
cn = json.load(open('lc_cn_all.json', encoding='utf-8'))
cn_map = {}
for p in cn['stat_status_pairs']:
    st = p['stat']
    cn_map[str(st['frontend_question_id'])] = st['question__title']

# ---------- 3. Hot 100 ----------
hot = json.load(open('hot100_raw.json', encoding='utf-8'))
final = {}          # fid -> item
hot_order = []
for q in hot:
    fid = str(q['id'])
    info = com_map.get(fid, {})
    item = {
        'id': q['id'],
        'title': q['title'],
        'slug': info.get('slug', q['slug']),
        'difficulty': info.get('diff', 'Easy'),
        'group': q['group'],
        'lists': ['hot100'],
    }
    final[fid] = item
    hot_order.append(fid)

# ---------- 4. Top Interview 150 ----------
md = open('t150_readme.md', encoding='utf-8').read()
GROUP_CN = {
    'Array/String': '数组/字符串', 'Two Pointers': '双指针', 'Sliding Window': '滑动窗口',
    'Matrix': '矩阵', 'Hashmap': '哈希表', 'Intervals': '区间', 'Stack': '栈',
    'Linked List': '链表', 'Binary Tree General': '二叉树', 'Binary Tree BFS': '二叉树',
    'Graph General': '图', 'Graph BFS': '图', 'Trie': '前缀树', 'Backtracking': '回溯',
    'Divide and Conquer': '分治', "Kadane's Algorithm": '动态规划', 'Binary Search': '二分查找',
    'Heap': '堆', 'Bit Manipulation': '位运算', 'Math': '数学',
    '1D DP': '动态规划', 'Multidimensional DP': '动态规划',
}
lines = md.split('\n')
in_section, cur_group = False, ''
t150_order = []
for ln in lines:
    if ln.startswith('### '):
        in_section = (ln.strip() == '### Top Interview 150')
        continue
    if not in_section:
        continue
    m = re.match(r'^#### Top Interview 150 (.+)$', ln)
    if m:
        cur_group = GROUP_CN.get(m.group(1).strip(), m.group(1).strip())
        continue
    m2 = re.match(r'^\| (\d+) \|([^|]+)\| \[', ln)
    if m2:
        fid = str(int(m2.group(1)))
        title_en = m2.group(2).strip()
        info = com_map.get(fid, {})
        cn_title = cn_map.get(fid, '')
        if fid in final:
            it = final[fid]
            if 'top150' not in it['lists']:
                it['lists'].append('top150')
            # 合并标签：hot100 group 优先；top150 分类不同时也加
            if it['group'] != cur_group:
                it['group'] = it['group']  # 保持 hot100 的 group
        else:
            final[fid] = {
                'id': int(fid),
                'title': cn_title or title_en,
                'slug': info.get('slug', ''),
                'difficulty': info.get('diff', 'Medium'),
                'group': cur_group,
                'lists': ['top150'],
            }
        t150_order.append(fid)

# ---------- 5. 输出 ----------
ordered = [final[f] for f in hot_order] + [final[f] for f in t150_order if f not in hot_order]
# 排序：按 id 升序
ordered.sort(key=lambda x: x['id'])

with open('questions.json', 'w', encoding='utf-8') as f:
    json.dump(ordered, f, ensure_ascii=False, separators=(',', ':'))

print('total:', len(ordered))
print('hot100:', len([x for x in ordered if 'hot100' in x['lists']]))
print('top150:', len([x for x in ordered if 'top150' in x['lists']]))
print('both:', len([x for x in ordered if len(x['lists']) == 2]))
print('sample:', json.dumps(ordered[0], ensure_ascii=False))
print('sample2:', json.dumps(ordered[-1], ensure_ascii=False))
# 抽查 Top 150 独有题
t_only = [x for x in ordered if x['lists'] == ['top150']]
print('top150-only count:', len(t_only))
for x in t_only[:5]:
    print(' ', x['id'], x['title'], x['difficulty'], x['group'], x['slug'])
