# -*- coding: utf-8 -*-
"""生成静态网站（美化版 URL）
输出结构：
  /index.html          ->  /
  /courses/1/index.html  ->  /courses/1/
  /courses/2/index.html  ->  /courses/2/
  ...
  /code/course1.txt   (代码文件，仅开发使用)
"""
import os
import io

OUT = os.path.dirname(os.path.abspath(__file__))


def read_tpl(path):
    with io.open(os.path.join(OUT, path), 'r', encoding='utf-8') as f:
        return f.read()


def build_index(cards):
    tpl = read_tpl('tpl_index.html')
    return tpl.replace('__COURSE_CARDS__', cards)


def build_course(c):
    tpl = read_tpl('tpl_course.html')
    # tags
    tags_html = ''
    for t in c['tags']:
        tags_html += '<span class="chip chip-dark">'+t+'</span>'

    # knowledge panels
    k_html = ''
    for (t, b) in c['knowledge']:
        k_html += '    <details class="k-panel">\n'
        k_html += '      <summary>'+t+'<span class="caret">▶</span></summary>\n'
        k_html += '      <div class="k-body">'+b+'</div>\n'
        k_html += '    </details>\n'

    # quiz
    q_html = ''
    for qi, (q, choices, correct, explain) in enumerate(c['quiz']):
        letters = ['A', 'B', 'C', 'D', 'E', 'F']
        rows = ''
        for ci, ct in enumerate(choices):
            rows += '      <div class="q-choice"><span class="q-letter">'+letters[ci]+'</span><span class="q-text">'+ct+'</span></div>\n'
        q_html += '      <div class="quiz-block border border-gray-200 rounded-2xl p-6 bg-gray-50" data-correct="'+str(correct)+'">\n'
        q_html += '        <div class="font-semibold text-gray-900 text-base leading-7 mb-4">'+str(qi+1)+'. '+q+'</div>\n'
        q_html += '        <div class="space-y-2">\n'+rows+'        </div>\n'
        q_html += '        <div class="mt-5 flex items-center gap-3 flex-wrap">\n'
        q_html += '          <button class="q-submit btn-base bg-brand-500 hover:bg-brand-600 text-white px-5 py-2.5 rounded-xl font-semibold text-sm inline-flex items-center gap-2 opacity-50 cursor-not-allowed" disabled>提交答案</button>\n'
        q_html += '          <span class="q-status-text text-xs text-gray-400">请先选择一个选项</span>\n'
        q_html += '        </div>\n'
        q_html += '        <div class="q-explain mt-5 rounded-xl bg-brand-50 border border-brand-100 p-5 text-sm text-gray-700 leading-7" style="display:none"><div class="font-semibold text-brand-600 mb-2 text-base">💡 解析</div>'+explain+'</div>\n'
        q_html += '      </div>\n'

    # summary
    sb = ''
    for s in c['summary']:
        sb += '        <li class="flex items-start gap-3 text-sm text-gray-700 leading-7"><span class="flex-shrink-0 w-6 h-6 rounded-full bg-purple-500 text-white text-xs font-bold flex items-center justify-center mt-0.5">✓</span><span>'+s+'</span></li>\n'

    # level class
    if c['level'] == 'beginner':
        level_class_inline = 'text-green-700 bg-green-50'
        level_class_banner = 'text-white bg-green-400/30'
    elif c['level'] == 'intermediate':
        level_class_inline = 'text-brand-700 bg-brand-50'
        level_class_banner = 'text-white bg-yellow-400/30'
    else:
        level_class_inline = 'text-purple-700 bg-purple-50'
        level_class_banner = 'text-white bg-purple-400/30'

    # nav links — 使用根相对路径
    if c['idx'] > 1:
        prev_link = '<a href="/courses/'+str(c['idx']-1)+'/" class="btn bg-gray-100 hover:bg-gray-200 text-gray-700 px-5 py-2.5 rounded-lg font-semibold text-sm">← 上一课</a>'
    else:
        prev_link = ''
    if c['idx'] < 10:
        next_link = '<a href="/courses/'+str(c['idx']+1)+'/" class="btn bg-brand-500 hover:bg-brand-600 text-white px-5 py-2.5 rounded-lg font-semibold text-sm">下一课 →</a>'
    else:
        next_link = ''

    out = tpl
    out = out.replace('__TITLE__', c['title'])
    out = out.replace('__IDX__', str(c['idx']))
    out = out.replace('__LEVEL_TEXT__', c['level_text'])
    out = out.replace('__LEVEL_CLASS_INLINE__', level_class_inline)
    out = out.replace('__LEVEL_CLASS_BANNER__', level_class_banner)
    out = out.replace('__HOURS__', c['hours'])
    out = out.replace('__RATING__', c['rating'])
    out = out.replace('__SUBTITLE__', c['subtitle'])
    out = out.replace('__GOALS__', c['goals'])
    out = out.replace('__AUDIENCE__', c['audience'])
    out = out.replace('__PREREQ__', c['prereq'])
    out = out.replace('__TAGS_HTML__', tags_html)
    out = out.replace('__KNOWLEDGE_HTML__', k_html)
    out = out.replace('__QUIZ_HTML__', q_html)
    out = out.replace('__SUMMARY_BULLETS__', sb)
    out = out.replace('__CODE_TEXT__', c['code'])
    out = out.replace('__PREV_LINK__', prev_link)
    out = out.replace('__NEXT_LINK__', next_link)
    return out


def write_file(full_path, content):
    """写入文件（自动创建父目录）"""
    parent = os.path.dirname(full_path)
    if parent and not os.path.isdir(parent):
        os.makedirs(parent, exist_ok=True)
    with io.open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    rel = os.path.relpath(full_path, OUT)
    print('generated:', rel)


def write_redirect(full_path, target_url):
    """创建一个自动跳转到新 URL 的页面（兼容旧链接）"""
    html = '<!DOCTYPE html>\n'
    html += '<html lang="zh-CN"><head><meta charset="UTF-8" />\n'
    html += '<meta http-equiv="refresh" content="0; url='+target_url+'" />\n'
    html += '<title>跳转中...</title>\n'
    html += '<style>body{display:flex;align-items:center;justify-content:center;height:100vh;margin:0;font-family:sans-serif;background:#f5f7fb;color:#165DFF;}</style>\n'
    html += '</head><body><p>正在跳转到 <a href="'+target_url+'">'+target_url+'</a>...</p></body></html>'
    write_file(full_path, html)


if __name__ == '__main__':
    from courses_data import COURSES

    # 首页卡片（使用美化后的链接 /courses/N/）
    cards = ''
    for c in COURSES:
        if c['level'] == 'beginner':
            lvl_cls = 'text-green-700 bg-green-50'
        elif c['level'] == 'intermediate':
            lvl_cls = 'text-brand-700 bg-brand-50'
        else:
            lvl_cls = 'text-purple-700 bg-purple-50'
        tag_html = ''
        for t in c['tags']:
            tag_html += '<span class="text-[11px] bg-gray-50 text-gray-600 border border-gray-200 px-2 py-0.5 rounded">'+t+'</span>'
        cards += '<a href="/courses/'+str(c['idx'])+'/" class="group block bg-white rounded-2xl p-6 shadow-sm border border-gray-100 hover-lift">'
        cards += '<div class="flex items-start justify-between gap-3">'
        cards += '<div class="flex items-center gap-3">'
        cards += '<div class="w-12 h-12 rounded-xl bg-brand-50 text-brand-500 flex items-center justify-center font-extrabold text-xl">'+str(c['idx'])+'</div>'
        cards += '<div><div class="text-xs text-gray-400">课程 '+str(c['idx'])+' / 10</div>'
        cards += '<h3 class="font-bold text-gray-900 mt-0.5 group-hover:text-brand-500 transition">'+c['title']+'</h3></div></div>'
        cards += '<span class="'+lvl_cls+' text-xs font-semibold px-2.5 py-1 rounded-full whitespace-nowrap">'+c['level_text']+'</span>'
        cards += '</div>'
        cards += '<p class="text-sm text-gray-500 mt-4 leading-7">'+c['subtitle']+'</p>'
        cards += '<div class="flex flex-wrap gap-1.5 mt-4">'+tag_html+'</div>'
        cards += '<div class="flex items-center justify-between text-xs text-gray-400 mt-5 pt-4 border-t border-gray-100">'
        cards += '<span>⏱ '+c['hours']+' · ★ '+c['rating']+'</span>'
        cards += '<span class="text-brand-500 font-semibold group-hover:translate-x-1 transition-transform inline-flex items-center gap-1">开始学习 →</span>'
        cards += '</div></a>\n'

    # 首页
    write_file(os.path.join(OUT, 'index.html'), build_index(cards))

    # 课程页：/courses/N/index.html
    for c in COURSES:
        d = os.path.join(OUT, 'courses', str(c['idx']))
        os.makedirs(d, exist_ok=True)
        write_file(os.path.join(d, 'index.html'), build_course(c))

    # 兼容旧链接：courseN.html → /courses/N/
    for c in COURSES:
        write_redirect(
            os.path.join(OUT, 'course'+str(c['idx'])+'.html'),
            '/courses/'+str(c['idx'])+'/'
        )

    # 额外：在 /courses/ 下添加一个聚合页，点击跳回首页
    agg = '<!DOCTYPE html>\n'
    agg += '<html lang="zh-CN"><head><meta charset="UTF-8" />\n'
    agg += '<meta http-equiv="refresh" content="0; url=/" />\n'
    agg += '<title>课程目录</title></head>'
    agg += '<body><p>正在跳转到 <a href="/">首页</a>...</p></body></html>'
    write_file(os.path.join(OUT, 'courses', 'index.html'), agg)

    print('\nDONE — 所有页面已生成')
    print('  首页:          /')
    print('  课程页:        /courses/1/ ~ /courses/10/')
    print('  (旧链接 courseN.html 自动跳转)')
