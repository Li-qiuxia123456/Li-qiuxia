// 代码执行器：运行用户代码、捕获输出、渲染表格
(function(global) {
  function htmlEscape(str) {
    if (str === null || str === undefined) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function renderDataFrame(data) {
    if (!data || !data.rows || !data.columns) return '';
    let html = '<div class="df-wrapper"><div class="df-title">' + htmlEscape(data.name || 'DataFrame') +
               '  <span class="df-shape">(' + data.shape[0] + ' rows × ' + data.shape[1] + ' cols)</span></div>';
    html += '<div class="df-scroll"><table class="df-table"><thead><tr><th class="df-index-head"></th>';
    data.columns.forEach(function(c) {
      html += '<th>' + htmlEscape(c) + '</th>';
    });
    html += '</tr></thead><tbody>';
    const maxRows = Math.min(data.rows.length, 100);
    for (let i = 0; i < maxRows; i++) {
      html += '<tr><td class="df-index">' + htmlEscape((data.index[i] !== undefined ? data.index[i] : i)) + '</td>';
      data.rows[i].forEach(function(v) {
        html += '<td>' + htmlEscape(v) + '</td>';
      });
      html += '</tr>';
    }
    html += '</tbody></table></div></div>';
    if (data.rows.length > maxRows) {
      html += '<div class="df-truncated">... 仅显示前 ' + maxRows + ' 行（共 ' + data.rows.length + ' 行）</div>';
    }
    return html;
  }

  function parseOutput(text, tableRegistry) {
    if (!text) return '';
    const pattern = /=====HTML_TABLE_(\d+)=====/g;
    let html = '';
    let lastIndex = 0;
    let match;
    while ((match = pattern.exec(text)) !== null) {
      const before = text.substring(lastIndex, match.index);
      if (before.trim()) {
        html += '<pre class="text-output">' + htmlEscape(before) + '</pre>';
      }
      const idx = parseInt(match[1], 10);
      if (tableRegistry && tableRegistry[idx]) {
        html += renderDataFrame(tableRegistry[idx]);
      }
      lastIndex = match.index + match[0].length;
    }
    const tail = text.substring(lastIndex);
    if (tail.trim()) {
      html += '<pre class="text-output">' + htmlEscape(tail) + '</pre>';
    }
    return html;
  }

  const Runner = {
    isReady: function() {
      return !!global.pyodide;
    },
    run: function(code, csvText, outputElement, statusElement) {
      const self = this;
      if (outputElement) outputElement.innerHTML = '<div class="output-running">正在执行...</div>';
      if (statusElement) statusElement.textContent = '运行中...';

      return global.loadPyodideRuntime().then(function() {
        return global.pyodide.runPythonAsync('_html_table_registry.clear()').then(function() {
          // 准备 CSV 变量
          if (csvText) {
            global.pyodide.globals.set('__csv_text__', csvText);
            return global.pyodide.runPythonAsync(
              '__df__ = pd.read_csv(io.StringIO(__csv_text__))\n' +
              'df = __df__\n' +
              'print("数据集已加载，变量名：df，形状：", df.shape)\n'
            );
          }
        }).then(function() {
          // 运行用户代码，捕获 stdout
          global.pyodide.setStdout({ batched: function(s) { /* handled below */ } });
          return global.pyodide.runPythonAsync(
            'import sys\n' +
            'from io import StringIO\n' +
            '_buf = StringIO()\n' +
            '_old_out = sys.stdout\n' +
            'sys.stdout = _buf\n' +
            '_ok = True\n' +
            'try:\n' +
            '    exec("""' + code.replace(/"""/g, '\\"\\"\\"') + '""")\n' +
            'except Exception as _e:\n' +
            '    import traceback\n' +
            '    traceback.print_exc()\n' +
            '    _ok = False\n' +
            'sys.stdout = _old_out\n' +
            '_captured = _buf.getvalue()\n' +
            '_captured\n'
          ).then(function(captured) {
            let okFlag = global.pyodide.globals.get('_ok');
            const ok = okFlag === true || (okFlag && okFlag.valueOf && okFlag.valueOf() === true);
            const tables = global.pyodide.globals.get('_html_table_registry').toJs();
            const tableArr = tables.map(function(t) {
              return {
                name: String(t.get('name') || ''),
                columns: Array.from(t.get('columns') || []),
                rows: Array.from(t.get('rows') || []).map(function(r) { return Array.from(r); }),
                index: Array.from(t.get('index') || []),
                shape: Array.from(t.get('shape') || [0, 0])
              };
            });

            let resultHtml = '';
            if (!ok) resultHtml = '<div class="output-error">⚠ 执行出错</div>';
            const parsed = parseOutput(captured || '', tableArr);
            resultHtml += parsed || '<pre class="text-output muted">(无输出)</pre>';
            if (outputElement) outputElement.innerHTML = resultHtml;
            if (statusElement) statusElement.textContent = ok ? '执行完成' : '执行出错';
            return { ok: ok, html: resultHtml };
          });
        });
      }).catch(function(err) {
        const msg = '<div class="output-error">执行失败: ' + htmlEscape(err.message || String(err)) + '</div>';
        if (outputElement) outputElement.innerHTML = msg;
        if (statusElement) statusElement.textContent = '执行失败';
        return { ok: false, html: msg };
      });
    }
  };

  global.PandasCampRunner = Runner;
})(window);
