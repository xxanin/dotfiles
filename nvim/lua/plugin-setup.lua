local gh = function(x) return 'https://github.com/' .. x end

vim.pack.add({
   gh('vague2k/vague.nvim'),
  -- gh('zenbones-theme/zenbones.nvim'),
  gh('stevearc/oil.nvim'),
  gh('tpope/vim-fugitive'),
  gh('nvim-lua/plenary.nvim'),
  { src = gh('nvim-telescope/telescope.nvim'), version = vim.version.range('0.1') },
})

vim.pack.add({
  gh('Exafunction/windsurf.vim'),
  gh('chomosuke/typst-preview.nvim'),
  gh('evanleck/vim-svelte'),
  gh('DingDean/wgsl.vim')
}, { load = function() end })

require('vague').setup({
  transparent = true,
  italic = false,
})
vim.cmd('colorscheme vague')

-- vim.g.zenbones_compat = 1
-- vim.cmd('colorscheme zenbones')
-- vim.api.nvim_set_hl(0, 'Normal', { bg = 'NONE' })
-- vim.api.nvim_set_hl(0, 'NormalNC', { bg = 'NONE' })
-- vim.api.nvim_set_hl(0, 'NormalFloat', { bg = 'NONE' })
-- vim.api.nvim_set_hl(0, 'FloatBorder', { bg = 'NONE' })
-- vim.api.nvim_set_hl(0, 'SignColumn', { bg = 'NONE' })
-- vim.api.nvim_set_hl(0, 'EndOfBuffer', { bg = 'NONE' })

require('oil').setup({
  keymaps = {
    ['gx'] = 'actions.open_cmdline',
    ['go'] = 'actions.open_external',
  },
  skip_confirm_for_simple_edits = true,
  columns = {
    'permissions',
    'size',
    'mtime',
  },
})
vim.keymap.set('n', '-', function() require('oil').open() end)

vim.keymap.set('n', '<leader>gd', ':Gvdiffsplit!<CR>')
vim.keymap.set('n', '<leader>dh', ':diffget //2<CR>')
vim.keymap.set('n', '<leader>dl', ':diffget //3<CR>')
vim.keymap.set('n', '<leader>gl', ':Gclog<CR>')
vim.keymap.set('n', '<leader>gb', ':G blame<CR>')
vim.keymap.set('n', '<leader>gf', ':G fetch<CR>')
vim.keymap.set('n', '<leader>gc', ':G checkout ')
vim.keymap.set('n', '<leader>gs', ':G switch ')
vim.keymap.set('n', '<leader>gp', ':G push<CR>')
vim.keymap.set('n', '<leader>gP', ':G pull<CR>')

local function telescope(builtin)
  return function()
    if not _G._telescope_loaded then
      local actions = require('telescope.actions')
      local actions_layout = require('telescope.actions.layout')
      require('telescope').setup({
        defaults = {
          mappings = {
            n = {
              ['d'] = actions.delete_buffer,
              ['<A-p>'] = actions_layout.toggle_preview,
            },
            i = {
              ['<A-p>'] = actions_layout.toggle_preview,
            },
          },
        },
        pickers = {
          find_files = { previewer = false, theme = 'ivy' },
          buffers = { previewer = false, sort_mru = true, sort_lastused = true, initial_mode = 'normal', theme = 'ivy' },
          live_grep = { previewer = false, theme = 'ivy' },
          help_tags = { theme = 'ivy' },
        },
      })
      _G._telescope_loaded = true
    end
    require('telescope.builtin')[builtin]()
  end
end

vim.keymap.set('n', ';f', telescope('find_files'))
vim.keymap.set('n', ';r', telescope('live_grep'))
vim.keymap.set('n', ';t', telescope('help_tags'))
vim.keymap.set('n', '\\\\', telescope('buffers'))
vim.keymap.set('n', ';;', telescope('resume'))

vim.api.nvim_create_autocmd('FileType', {
  pattern = { 'javascript', 'typescript', 'javascriptreact', 'typescriptreact', 'html', 'css', 'scss' },
  once = true,
  callback = function()
    vim.cmd.packadd('windsurf.vim')
    vim.g.codeium_disable_bindings = 1
    vim.g.codeium_filetypes = { TelescopePrompt = false }
    vim.keymap.set('i', '<A-y>', function() return vim.fn['codeium#Accept']() end, { expr = true, silent = true })
    vim.keymap.set('i', '<A-t>', function() return vim.fn['codeium#AcceptNextWord']() end, { expr = true, silent = true })
    vim.keymap.set('i', '<A-.>', function() return vim.fn['codeium#CycleCompletions'](1) end,
      { expr = true, silent = true })
    vim.keymap.set('i', '<A-/>', function() return vim.fn['codeium#CycleCompletions'](-1) end,
      { expr = true, silent = true })
  end,
})

vim.api.nvim_create_autocmd('FileType', {
  pattern = 'typst',
  once = true,
  callback = function()
    vim.cmd.packadd('typst-preview.nvim')
    require('typst-preview').setup({})
  end,
})

vim.api.nvim_create_autocmd('FileType', {
  pattern = 'svelte',
  once = true,
  callback = function()
    vim.cmd.packadd('vim-svelte')
  end,
})

vim.api.nvim_create_autocmd('FileType', {
  pattern = 'wgsl',
  once = true,
  callback = function()
    vim.cmd.packadd('wgsl.vim')
  end,
})

vim.cmd.packadd('nvim.undotree')
