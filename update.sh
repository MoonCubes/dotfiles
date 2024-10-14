#!/bin/sh

mkdir -p ./.config
mkdir -p ./.local/bin
mkdir -p ./.local/share/backgrounds/unsplash

cp -r ~/.config/betterlockscreen/  ./.config/
cp -r ~/.config/nvim/              ./.config/
cp -r ~/.config/picom/             ./.config/
cp -r ~/.config/qtile              ./.config/
cp -r ~/.config/rofi/              ./.config/
cp ~/.local/share/backgrounds/unsplash/johannes-plenio-hvrpOmuMrAI-unsplash.jpg ./.local/share/backgrounds/unsplash/

cp ~/.local/bin/gpg-clip ./.local/bin/
cp ~/.local/bin/is-media-playing ./.local/bin/
cp ~/.local/bin/timer ./.local/bin/
cp ~/.local/bin/toggle-media ./.local/bin/

