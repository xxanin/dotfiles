vim.keymap.set('n', '<leader>ff', vim.lsp.buf.format)
vim.keymap.set('n', '<leader>qd', function()
  vim.diagnostic.setqflist({ open = true })
end)

vim.lsp.config('rust_analyzer', {
  settings = {
    ['rust-analyzer'] = {
      check = {
        command = 'clippy',
      }
    }
  }
})
vim.lsp.config('sourcekit', {
  filetypes = { "swift" },
})

local prettier = { formatCommand = "prettierd --stdin-filepath ${INPUT}", formatStdin = true }
local black    = { formatCommand = "black -q -", formatStdin = true }

vim.lsp.config('efm', {
  init_options = { documentFormatting = true },
  filetypes = { "typescript", "typescriptreact", "javascript", "javascriptreact", "svelte", "json", "yaml", "markdown", "html", "css", "python" },
  settings = {
    rootMarkers = {
      ".git/",
      "package.json",
      ".prettierrc",
    },
    languages = {
      typescript = { prettier },
      typescriptreact = { prettier },
      javascript = { prettier },
      javascriptreact = { prettier },
      svelte = { prettier },
      json = { prettier },
      yaml = { prettier },
      markdown = { prettier },
      html = { prettier },
      css = { prettier },
      python = { black }
    },
  },
})

local disable_formatting_clients = {
  ts_ls = true,
  vtsls = true,
  html = true,
  cssls = true,
  eslint = true,
  oxlint = true
}

vim.lsp.enable({ "ts_ls", "eslint", "oxlint", "efm", "html", "cssls", "tailwindcss", "clangd", "rust_analyzer", "gopls",
  "pyright",
  "lua_ls", "tinymist", "svelte", "sourcekit" })

vim.api.nvim_create_autocmd("LspAttach", {
  callback = function(ev)
    local client = vim.lsp.get_client_by_id(ev.data.client_id)

    if disable_formatting_clients[client.name] then
      client.server_capabilities.documentFormattingProvider = false
    end

    if client.server_capabilities.semanticTokensProvider then
      client.server_capabilities.semanticTokensProvider = nil
    end
  end,
})
