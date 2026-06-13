# -*- coding: utf-8 -*-
import os, io

OUT = os.path.dirname(os.path.abspath(__file__))

def read_tpl(path):
    with io.open(os.path.join(OUT, path), 'r', encoding='utf-8') as f:
        return f.read()

def build_index(cards):
    tpl = read_tpl('tpl_index.html')
    return tpl.replace('__COURSE_CARDS__', cards)

def build_course(c):
    tpl = read_tpl('tpl_course.html')
    # tags —— 更新为新的 chip 样式
    tags_html = ''
    for t in c['tags']:
        tags_html += '<span class="chip chip-dark">'+t+'</span>'

    # knowledge —— 新样式 k-panel
    k_html = ''
    for (t, b) in c['knowledge']:
        k_html += '    <details class="k-panel">\n'
        k_html += '      <summary>'+t+'<span class="caret">▶</span></summary>\n'
        k_html += '      <div class="k-body">'+b+'</div>\n'
        k_html += '    </details>\n'
    # quiz —— 新模板使用 .q-choice / .q-submit / .q-explain
    q_html = ''
    for qi, (q, choices, correct, explain) in enumerate(c['quiz']):
        letters = ['A','B','C','D','E','F']
        rows = ''
        for ci, ct in enumerate(choices):
            rows += '      <div class="q-choice"><span class="q-letter">'+letters[ci]+'</span><span class="q-text">'+ct+'</span></div>\n'
        q_html += '      <div class="quiz-block border border-gray-200 rounded-2xl p-6 bg-gray-50" data-correct="'+str(correct)+'">\n'
        q_html += '        <div class="font-semibold text-gray-900 text-base leading-7 mb-4">'+str(qi+1)+'. '+q+'</div>\n'
        q_html += '        <div class="space-y-2">\n' + rows + '        </div>\n'
        q_html += '        <div class="mt-5 flex items-center gap-3 flex-wrap">\n'
        q_html += '          <button class="q-submit btn-base bg-brand-500 hover:bg-brand-600 text-white px-5 py-2.5 rounded-xl font-semibold text-sm inline-flex items-center gap-2 opacity-50 cursor-not-allowed" disabled>提交答案</button>\n'
        q_html += '          <span class="q-status-text text-xs text-gray-400">请先选择一个选项</span>\n'
        q_html += '        </div>\n'
        q_html += '        <div class="q-explain mt-5 rounded-xl bg-brand-50 border border-brand-100 p-5 text-sm text-gray-700 leading-7" style="display:none"><div class="font-semibold text-brand-600 mb-2 text-base">💡 解析</div>'+explain+'</div>\n'
        q_html += '      </div>\n'
    # summary bullets —— 更精美的列表样式
    sb = ''
    for s in c['summary']:
        sb += '        <li class="flex items-start gap-3 text-sm text-gray-700 leading-7"><span class="flex-shrink-0 w-6 h-6 rounded-full bg-purple-500 text-white text-xs font-bold flex items-center justify-center mt-0.5">✓</span><span>'+s+'</span></li>\n'
    # level class (card)
    if c['level'] == 'beginner':
        level_class_inline = 'text-green-700 bg-green-50'
        level_class_banner = 'text-white bg-green-400/30'
    elif c['level'] == 'intermediate':
        level_class_inline = 'text-brand-700 bg-brand-50'
        level_class_banner = 'text-white bg-yellow-400/30'
    else:
        level_class_inline = 'text-purple-700 bg-purple-50'
        level_class_banner = 'text-white bg-purple-400/30'
    # nav links
    if c['idx'] > 1:
        prev_link = '<a href="course'+str(c['idx']-1)+'.html" class="btn bg-gray-100 hover:bg-gray-200 text-gray-700 px-5 py-2.5 rounded-lg font-semibold text-sm">← 上一课</a>'
    else:
        prev_link = ''
    if c['idx'] < 10:
        next_link = '<a href="course'+str(c['idx']+1)+'.html" class="btn bg-brand-500 hover:bg-brand-600 text-white px-5 py-2.5 rounded-lg font-semibold text-sm">下一课 →</a>'
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

def write_file(name, content):
    with io.open(os.path.join(OUT, name), 'w', encoding='utf-8') as f:
        f.write(content)
    print('generated:', name)

if __name__ == '__main__':
    # import course data
    from courses_data import COURSES
    # index cards
    cards = ''
    for c in COURSES:
        if c['level'] == 'beginner':
            lvl_cls = 'text-green-700 bg-green-50'
        elif c['level'] == 'intermediate':
            lvl_cls = 'text-brand-700 bg-brand-50'
        else:
            lvl_cls = 'text-purple-700 bg-purple-50'
        tags_html = ''
        for t in c['tags']:
            tags_html += '<span class="text-[11px] bg-gray-50 text-gray-600 border border-gray-200 px-2 py-0.5 rounded">'+t+'</span>'
        cards += '<a href="course'+str(c['idx'])+'.html" class="group block bg-white rounded-2xl p-6 shadow-sm border border-gray-100 hover-lift"><div class="flex items-start justify-between gap-3"><div class="flex items-center gap-3"><div class="w-12 h-12 rounded-xl bg-brand-50 text-brand-500 flex items-center justify-center font-extrabold text-xl">'+str(c['idx'])+'</div><div><div class="text-xs text-gray-400">课程 '+str(c['idx'])+' / 10</div><h3 class="font-bold text-gray-900 mt-0.5 group-hover:text-brand-500 transition">'+c['title']+'</h3></div></div><span class="'+lvl_cls+' text-xs font-semibold px-2.5 py-1 rounded-full whitespace-nowrap">'+c['level_text']+'</span></div><p class="text-sm text-gray-500 mt-4 leading-7">'+c['subtitle']+'</p><div class="flex flex-wrap gap-1.5 mt-4">'+tags_html+'</div><div class="flex items-center justify-between text-xs text-gray-400 mt-5 pt-4 border-t border-gray-100"><span>⏱ '+c['hours']+' · ★ '+c['rating']+'</span><span class="text-brand-500 font-semibold group-hover:translate-x-1 transition-transform inline-flex items-center gap-1">开始学习 →</span></div></a>\n'
    write_file('index.html', build_index(cards))
    for c in COURSES:
        write_file('course'+str(c['idx'])+'.html', build_course(c))
    print('DONE')
