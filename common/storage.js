(function(global) {
  const PREFIX = 'pandas_camp_';

  function key(k) { return PREFIX + k; }

  const Storage = {
    // 获取某项目用户代码
    getCode: function(projectId) {
      try {
        return localStorage.getItem(key('code_' + projectId)) || null;
      } catch (e) { return null; }
    },
    // 保存用户代码
    saveCode: function(projectId, code) {
      try {
        localStorage.setItem(key('code_' + projectId), code);
        return true;
      } catch (e) { return false; }
    },
    // 清除用户代码
    clearCode: function(projectId) {
      try { localStorage.removeItem(key('code_' + projectId)); } catch (e) {}
    },

    // 标记项目完成
    markComplete: function(projectId) {
      try {
        const list = this.getCompletedList();
        if (list.indexOf(projectId) === -1) {
          list.push(projectId);
          localStorage.setItem(key('completed'), JSON.stringify(list));
        }
        return true;
      } catch (e) { return false; }
    },
    // 获取已完成项目列表
    getCompletedList: function() {
      try {
        const raw = localStorage.getItem(key('completed'));
        return raw ? JSON.parse(raw) : [];
      } catch (e) { return []; }
    },
    // 判断项目是否完成
    isCompleted: function(projectId) {
      return this.getCompletedList().indexOf(projectId) !== -1;
    },
    // 获取进度统计
    getProgress: function() {
      return this.getCompletedList().length;
    },
    // 清除所有进度
    clearAll: function() {
      try {
        const keys = Object.keys(localStorage).filter(function(k) {
          return k.indexOf(PREFIX) === 0;
        });
        keys.forEach(function(k) { localStorage.removeItem(k); });
      } catch (e) {}
    }
  };

  global.PandasCampStorage = Storage;
})(window);
