# aliases
alias vim='nvim'
alias ls='gls --color=always -ph --group-directories-first'
alias ll='ls -l'
alias la='ls -la'
alias qview='/Applications/qView.app/Contents/MacOS/qView'
alias clean-ds="fd '.DS_Store' ~ --type f --hidden --no-ignore -X rm"
alias ytv='yt-dlp -f "bv*[ext=mp4][vcodec^=avc1]+ba[ext=m4a]/b[ext=mp4][vcodec^=avc1]/best" -o "$HOME/videos/tmp/%(title)s.%(ext)s"'
alias yta='yt-dlp -f "bestaudio" --extract-audio --audio-format mp3 --audio-quality 0 --add-metadata --parse-metadata "artist:%(uploader)s" -o "$HOME/music/xanin/tmp/%(title)s.%(ext)s"'
alias fs='fastfetch --logo mac2_small --structure "title:os:host:kernel:uptime:packages:shell:wm:terminal:cpu:memory"'
alias cmus='LC_ALL=C.UTF-8 cmus'
alias python3='python3.14'
alias python='python3.14'

alias yad='yarn app:dev'
alias ydd='yarn dashboard:dev'
alias ysd='yarn sign:dev'
alias ywd='yarn website:dev'

# base
PROMPT_DIRTRIM=3
bindkey -e
# bindkey -v
# bindkey '^P' up-line-or-history
# bindkey '^N' down-line-or-history
autoload -Uz edit-command-line
zle -N edit-command-line
# bindkey -M vicmd 'v' edit-command-line

# fzf
export FZF_DEFAULT_OPTS=$'
    --gutter=\'\ \'
    --color=fg:-1,bg:-1,hl:yellow
    --color=fg+:-1,bg+:-1,hl+:green
    --color=border:bright-black,header:blue,gutter:-1
    --color=spinner:yellow,info:cyan,separator:bright-black
    --color=pointer:bright-yellow,marker:magenta,prompt:-1
'

# functions
vm() {
  local -a files
  files=(${(f)"$(fd --type f \
    --exclude node_modules \
    --exclude .next \
    --exclude .nx \
    --exclude dist \
    --exclude build \
    | fzf -m --preview='bat --color=always {}')"})
  (( ${#files[@]} )) && vim "${files[@]}"
}

export HISTFILE="$HOME/.local/state/zsh/history"
export HISTSIZE=100000
export SAVEHIST=100000
setopt inc_append_history
setopt share_history
setopt hist_ignore_all_dups
setopt HIST_REDUCE_BLANKS
setopt HIST_IGNORE_SPACE

setopt MULTIOS
setopt EXTENDED_HISTORY
setopt IGNORE_EOF
setopt INTERACTIVE_COMMENTS

fzf-history-insert() {
  local sel left=$LBUFFER right=$RBUFFER
  sel=$(builtin fc -nrl 1 | fzf --no-sort --query="$LBUFFER") || return
  BUFFER="$left$sel$right"
  CURSOR=$(( ${#left} + ${#sel} ))
  zle redisplay
}
zle -N fzf-history-insert
bindkey -M viins '^R' fzf-history-insert
bindkey -M vicmd '^R' fzf-history-insert
bindkey -M emacs '^R' fzf-history-insert
bindkey -M viins '^?' backward-delete-char
bindkey -M vicmd '^?' backward-delete-char
bindkey -M viins '^H' backward-kill-word
bindkey -M viins '^D' delete-char

# sources
source "$ZDOTDIR/prompt.zsh"
source "$ZDOTDIR/completions.zsh"

# tmp
[ -d ~/.claude ] && [ ! -L ~/.claude ] && {
  mkdir -p "${XDG_CONFIG_HOME:-$HOME/.config}/claude"
  cp -a ~/.claude/* "${XDG_CONFIG_HOME:-$HOME/.config}/claude/" 2>/dev/null
  # Remove original and replace with symlink
  command rm -r ~/.claude
  ln -s "${XDG_CONFIG_HOME:-$HOME/.config}/claude" ~/.claude
}

# hooks
eval "$(direnv hook zsh)"
