(function(global) {
  function htmlEscape(str) {
    if (str === null || str === undefined) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');
  }

  function parseOutput(text) {
    if (!text) return '';
    return '<pre class="text-output">' + htmlEscape(text) + '</pre>';
  }

  const Runner = {
    run: function(code, csvText, outputElement, statusElement) {
      const self = this;
      if (outputElement) outputElement.innerHTML = '<div class="output-running">正在执行代码... (Pyodide 首次加载可能需要 10-20 秒)</div>';
      if (statusElement) statusElement.textContent = '执行中...';

      return global.loadPyodideRuntime().then(function() {
        return new Promise(function(resolve, reject) {
          try {
            // 将 CSV 数据导入 pyodide
            if (csvText) {
              global.pyodide.globals.set('__csv_data__', csvText);
            }

            // 完整的执行脚本：加载数据 → 执行用户代码 → 捕获结果
            const fullScript = `
import sys, io, traceback
import pandas as pd

_buf = io.StringIO()
_old_out = sys.stdout
sys.stdout = _buf

results = []

def show(df, name=None):
    try:
        if isinstance(df, pd.DataFrame):
            cols = list(df.columns.astype(str))
            rows = [list(r) for r in df.values.tolist()]
            idx = list(df.index.astype(str)) if hasattr(df.index, 'astype') else [str(x) for x in df.index]
            shape = list(df.shape)
            results.append({'type': 'df', 'name': name or 'DataFrame', 'columns': cols, 'rows': rows, 'index': idx, 'shape': shape})
        elif isinstance(df, pd.Series):
            cols = [str(df.name) if df.name is not None else 'value']
            rows = [[v] for v in df.values.tolist()]
            idx = [str(x) for x in df.index]
            shape = [df.shape[0], 1]
            results.append({'type': 'df', 'name': name or 'Series', 'columns': cols, 'rows': rows, 'index': idx, 'shape': shape})
        else:
            print(df)
    except Exception as e:
        print('显示错误:', e)

try:
    __csv_data__
except NameError:
    __csv_data__ = ''

df = pd.read_csv(io.StringIO(__csv_data__)) if __csv_data__ else None

try:
    exec(''' + JSON.stringify(code) + ''', globals())
except Exception as _e:
    traceback.print_exc()
    results.append({'type': 'error'})

sys.stdout = _old_out
_output = _buf.getvalue()
{'output': _output, 'tables': results}
`;

            global.pyodide.runPythonAsync(fullScript).then(function(pyResult) {
              const output = pyResult.get ? pyResult.toJs() : pyResult;
              let html = '';
              if (output.output) html += parseOutput(output.output);

              if (output.tables) {
                const tables = output.tables.toJs ? output.tables.toJs() : output.tables;
                for (const t of tables) {
                  const obj = t.toJs ? t.toJs() : t;
                  if (obj.type === 'df') {
                    html += renderDataFrame(obj);
                  }
                }
              }

              if (!html) {
                html = '<pre class="text-output muted">(无输出)</pre>';
              }

              if (outputElement) outputElement.innerHTML = html;
              if (statusElement) statusElement.textContent = '执行完成 ✓';
              resolve({ ok: true, html: html });
            }).catch(function(err) {
              const msg = '<div class="output-error">⚠ Python 执行错误:</div><pre class="text-output">' + htmlEscape(err.message || String(err)) + '</pre>';
              if (outputElement) outputElement.innerHTML = msg;
              if (statusElement) statusElement.textContent = '执行失败';
              resolve({ ok: false, html: msg });
            });
          } catch (err) {
            const msg = '<div class="output-error">⚠ 执行初始化错误:</div><pre class="text-output">' + htmlEscape(err.message || String(err)) + '</pre>';
            if (outputElement) outputElement.innerHTML = msg;
            if (statusElement) statusElement.textContent = '执行失败';
            resolve({ ok: false, html: msg });
          }
        });
      }).catch(function(err) {
        const msg = '<div class="output-error">⚠ Pyodide 加载失败:</div><pre class="text-output">' + htmlEscape(err.message || String(err)) + '</pre>';
        if (outputElement) outputElement.innerHTML = msg;
        if (statusElement) statusElement.textContent = '加载失败';
        return { ok: false, html: msg };
      });
    }
  };

  function renderDataFrame(data) {
    let html = '<div class="df-wrapper"><div class="df-title">' + htmlEscape(data.name || 'DataFrame') +
               '  <span class="df-shape">(' + data.shape[0] + ' 行 × ' + data.shape[1] + ' 列)</span></div>';
    html += '<div class="df-scroll"><table class="df-table"><thead><tr><th class="df-index-head"></th>';
    data.columns.forEach(function(c) { html += '<th>' + htmlEscape(c) + '</th>'; });
    html += '</tr></thead><tbody>';
    const maxRows = Math.min(data.rows.length, 200);
    for (let i = 0; i < maxRows; i++) {
      html += '<tr><td class="df-index">' + htmlEscape((data.index[i] !== undefined ? data.index[i] : i)) + '</td>';
      data.rows[i].forEach(function(v) {
        let cell = v;
        if (typeof cell === 'number') cell = Math.round(cell * 1000) / 1000;
        html += '<td>' + htmlEscape(cell) + '</td>';
      });
      html += '</tr>';
    }
    html += '</tbody></table></div>';
    if (data.rows.length > maxRows) {
      html += '<div class="df-truncated">... 仅显示前 ' + maxRows + ' 行（共 ' + data.rows.length + ' 行）</div>';
    }
    html += '</div>';
    return html;
  }

  global.PandasCampRunner = Runner;
})(window);
