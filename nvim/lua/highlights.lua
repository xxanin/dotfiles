vim.opt.winborder = 'rounded'
vim.opt.pumborder = 'rounded'

vim.g.markdown_fenced_languages = { 'html', 'python', 'lua', 'vim', 'typescript', 'javascript', 'typescriptreact', 'sh',
  'bash', 'c', 'cpp', 'rust' }

vim.filetype.add({
  extension = {
    metal = "cpp",
  },
})

vim.api.nvim_create_autocmd({ "BufRead", "BufNewFile" }, {
  pattern = "*.metal",
  callback = function()
    vim.bo.filetype = "metal"
    vim.bo.syntax = "cpp"
  end,
})
