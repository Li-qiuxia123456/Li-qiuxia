// Pyodide 全局初始化器
(function(global) {
  let loadPromise = null;

  global.loadPyodideRuntime = function() {
    if (loadPromise) return loadPromise;

    loadPromise = new Promise(function(resolve, reject) {
      // 确保 loadPyodide 脚本已加载
      function waitForLoadPyodide(resolveLoader) {
        if (typeof global.loadPyodide === 'function') {
          resolveLoader();
        } else {
          setTimeout(function() { waitForLoadPyodide(resolveLoader); }, 100);
        }
      }

      waitForLoadPyodide(function() {
        global.loadPyodide({
          indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.26.2/full/'
        }).then(function(pyodide) {
          global.pyodide = pyodide;
          return pyodide.loadPackage(['pandas', 'numpy', 'scikit-learn']);
        }).then(function() {
          // 注入公共工具：CSV → DataFrame 函数
          const initCode = [
            'import pandas as pd',
            'import numpy as np',
            'import io',
            'from io import StringIO',
            '',
            '_html_table_registry = []',
            '',
            'def show(df, name=None):',
            '    """在前端以 HTML 表格形式显示 DataFrame/Series。"""',
            '    import json',
            '    if isinstance(df, pd.DataFrame):',
            '        data = {',
            '            "columns": list(df.columns.astype(str)),',
            '            "rows": [list(row) for row in df.values.tolist()],',
            '            "index": list(df.index.astype(str)) if hasattr(df.index, "astype") else [str(x) for x in df.index],',
            '            "name": name or "DataFrame",',
            '            "shape": list(df.shape),',
            '        }',
            '    elif isinstance(df, pd.Series):',
            '        data = {',
            '            "columns": [str(df.name) if df.name is not None else "value"],',
            '            "rows": [[v] for v in df.values.tolist()],',
            '            "index": [str(x) for x in df.index],',
            '            "name": name or "Series",',
            '            "shape": [df.shape[0], 1],',
            '        }',
            '    else:',
            '        print(str(df))',
            '        return',
            '    _html_table_registry.append(data)',
            '    print("=====HTML_TABLE_" + str(len(_html_table_registry) - 1) + "=====")',
            '',
            'def load_csv(csv_text):',
            '    """把页面传入的 CSV 字符串解析为 DataFrame。"""',
            '    return pd.read_csv(StringIO(csv_text))',
            ''
          ].join('\n');
          return global.pyodide.runPythonAsync(initCode);
        }).then(function() {
          resolve(global.pyodide);
        }).catch(function(err) {
          reject(err);
        });
      });
    });

    return loadPromise;
  };
})(window);
