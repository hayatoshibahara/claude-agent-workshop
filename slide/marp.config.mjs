// marp の設定。npm run serve などで読む

// リンクを全部新しいタブで開く。Markdown のリンクと、スライドに直接書いた <a> の両方
const newTab = (md) => {
  const attrs = (tokens, idx, options, env, self) => {
    tokens[idx].attrSet('target', '_blank')
    tokens[idx].attrSet('rel', 'noopener')
    return self.renderToken(tokens, idx, options)
  }
  md.renderer.rules.link_open = attrs

  const addTarget = (html) => html.replace(/<a (?![^>]*\btarget=)/g, '<a target="_blank" rel="noopener" ')
  for (const rule of ['html_inline', 'html_block']) {
    const orig = md.renderer.rules[rule]
    md.renderer.rules[rule] = (tokens, idx, options, env, self) =>
      addTarget(orig(tokens, idx, options, env, self))
  }
}

export default {
  themeSet: 'theme',
  html: true,
  allowLocalFiles: true,
  engine: ({ marp }) => marp.use(newTab),
}
