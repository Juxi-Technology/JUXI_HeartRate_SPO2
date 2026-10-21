/* 精简 Markdown 渲染器：只覆盖本仓库文档用到的语法，无外部依赖 */
(function (global) {
  'use strict';

  function escapeHtml(s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function slugify(text) {
    return text
      .toLowerCase()
      .replace(/`([^`]*)`/g, '$1')
      .replace(/\[([^\]]*)\]\([^)]*\)/g, '$1')
      .replace(/[*_~]/g, '')
      .replace(/[^\p{L}\p{N}\s_-]/gu, '')
      .trim()
      .replace(/\s+/g, '-');
  }

  var PH = '\u0000';

  function inline(text) {
    var s = escapeHtml(text);
    var codes = [];
    s = s.replace(/`([^`]+)`/g, function (m, c) {
      codes.push(c);
      return PH + (codes.length - 1) + PH;
    });
    s = s.replace(/!\[([^\]]*)\]\(([^)\s]+)\)/g, function (m, alt, src) {
      return '<img src="' + src + '" alt="' + alt + '" loading="lazy">';
    });
    s = s.replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, function (m, label, href) {
      return '<a href="' + href + '">' + label + '</a>';
    });
    s = s.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    s = s.replace(/(^|[^*])\*([^*\n]+)\*/g, '$1<em>$2</em>');
    s = s.replace(new RegExp(PH + '(\\d+)' + PH, 'g'), function (m, i) {
      return '<code>' + codes[+i] + '</code>';
    });
    return s;
  }

  function isTableSep(line) {
    // 至少一列；`---` 本身是分隔线，所以要求这一行带竖线
    return line.indexOf('|') >= 0 &&
      /^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?\s*$/.test(line);
  }

  function splitRow(line) {
    var s = line.trim();
    if (s.charAt(0) === '|') s = s.slice(1);
    if (s.charAt(s.length - 1) === '|') s = s.slice(0, -1);
    var cells = [];
    var cur = '';
    var inCode = false;
    for (var i = 0; i < s.length; i++) {
      var ch = s.charAt(i);
      if (ch === '`') inCode = !inCode;
      if (ch === '|' && !inCode) {
        cells.push(cur);
        cur = '';
      } else {
        cur += ch;
      }
    }
    cells.push(cur);
    return cells.map(function (c) { return c.trim(); });
  }

  function isBlockStart(line) {
    return (
      /^\s*```/.test(line) ||
      /^\s{0,3}#{1,6}\s+/.test(line) ||
      /^\s{0,3}([-*_])\s*(\1\s*){2,}$/.test(line) ||
      /^\s*>/.test(line) ||
      /^\s*([-*+]|\d+\.)\s+/.test(line)
    );
  }

  function renderList(lines, start) {
    var items = [];
    var i = start;
    var last = null;
    while (i < lines.length) {
      var line = lines[i];
      var m = line.match(/^(\s*)([-*+]|\d+\.)\s+(.*)$/);
      if (m) {
        var indent = m[1].replace(/\t/g, '    ').length;
        items.push({
          indent: indent,
          ordered: /^\d/.test(m[2]),
          num: parseInt(m[2], 10) || 1,
          text: [m[3]]
        });
        last = items[items.length - 1];
        i++;
      } else if (line.trim() && /^\s+\S/.test(line) && last) {
        last.text.push(line.trim());
        i++;
      } else {
        break;
      }
    }

    var root = { indent: -1, children: [] };
    var stack = [root];
    for (var k = 0; k < items.length; k++) {
      var it = items[k];
      while (stack.length > 1 && it.indent <= stack[stack.length - 1].indent) stack.pop();
      var node = { indent: it.indent, ordered: it.ordered, num: it.num, text: it.text, children: [] };
      stack[stack.length - 1].children.push(node);
      stack.push(node);
    }

    function build(node) {
      if (!node.children.length) return '';
      var ordered = node.children[0].ordered;
      var tag = ordered ? 'ol' : 'ul';
      var attr = ordered && node.children[0].num !== 1 ? ' start="' + node.children[0].num + '"' : '';
      return '<' + tag + attr + '>' + node.children.map(function (ch) {
        return '<li>' + inline(ch.text.join(' ')) + build(ch) + '</li>';
      }).join('') + '</' + tag + '>';
    }
    return [build(root), i];
  }

  function renderBlocks(lines) {
    var out = [];
    var i = 0;
    while (i < lines.length) {
      var line = lines[i];

      if (!line.trim()) { i++; continue; }

      var fence = line.match(/^\s*```+\s*([\w+-]*)\s*$/);
      if (fence) {
        var lang = fence[1];
        var buf = [];
        i++;
        while (i < lines.length && !/^\s*```+\s*$/.test(lines[i])) buf.push(lines[i++]);
        i++;
        out.push('<pre><code' + (lang ? ' class="language-' + lang + '"' : '') + '>' +
          escapeHtml(buf.join('\n')) + '</code></pre>');
        continue;
      }

      var h = line.match(/^\s{0,3}(#{1,6})\s+(.*?)\s*#*\s*$/);
      if (h) {
        var level = h[1].length;
        out.push('<h' + level + ' id="' + escapeHtml(slugify(h[2])) + '">' + inline(h[2]) + '</h' + level + '>');
        i++;
        continue;
      }

      if (/^\s{0,3}([-*_])\s*(\1\s*){2,}$/.test(line)) {
        out.push('<hr>');
        i++;
        continue;
      }

      if (line.indexOf('|') >= 0 && i + 1 < lines.length && isTableSep(lines[i + 1])) {
        var head = splitRow(line);
        var aligns = splitRow(lines[i + 1]).map(function (c) {
          var l = c.charAt(0) === ':';
          var r = c.charAt(c.length - 1) === ':';
          return l && r ? 'center' : r ? 'right' : l ? 'left' : '';
        });
        i += 2;
        var rows = [];
        while (i < lines.length && lines[i].trim() && lines[i].indexOf('|') >= 0) {
          rows.push(splitRow(lines[i++]));
        }
        function cell(tag, text, idx) {
          var al = aligns[idx] ? ' style="text-align:' + aligns[idx] + '"' : '';
          return '<' + tag + al + '>' + inline(text || '') + '</' + tag + '>';
        }
        var html = '<div class="table-wrap"><table><thead><tr>' +
          head.map(function (c, idx) { return cell('th', c, idx); }).join('') +
          '</tr></thead><tbody>' +
          rows.map(function (r) {
            var tds = '';
            for (var c = 0; c < head.length; c++) tds += cell('td', r[c], c);
            return '<tr>' + tds + '</tr>';
          }).join('') +
          '</tbody></table></div>';
        out.push(html);
        continue;
      }

      if (/^\s*>/.test(line)) {
        var quote = [];
        while (i < lines.length && /^\s*>/.test(lines[i])) {
          quote.push(lines[i++].replace(/^\s*>\s?/, ''));
        }
        out.push('<blockquote>' + renderBlocks(quote) + '</blockquote>');
        continue;
      }

      if (/^\s*([-*+]|\d+\.)\s+/.test(line)) {
        var res = renderList(lines, i);
        out.push(res[0]);
        i = res[1];
        continue;
      }

      var para = [];
      while (i < lines.length && lines[i].trim() && !isBlockStart(lines[i]) &&
             !(lines[i].indexOf('|') >= 0 && i + 1 < lines.length && isTableSep(lines[i + 1]))) {
        para.push(lines[i++]);
      }
      out.push('<p>' + inline(para.join(' ')) + '</p>');
    }
    return out.join('\n');
  }

  global.renderMarkdown = function (src) {
    return renderBlocks(src.replace(/\r\n?/g, '\n').split('\n'));
  };
})(window);
