# Minecraft Icons

Icons scraped from https://minecraft.fandom.com/wiki/Category:Icons

**Why?** It sounded fun

## Running Locally

This will recursively check the root Icons page on minecraft fandom, downloading all links that have `class="image"`.

All files can be found under `./downloads`.

**The script does the following:**

1. Check all links & images starting from https://minecraft.fandom.com/wiki/Category:Icons
2. Batch download all files
3. Profit

```sh
$ poetry install
$ poetry run python mc_assets/main.py
  >Block_icons/Animated_block_icons
  >Block_icons/Block_action_animations
  >Block_icons/Fence-like_blocks
  ...
Progress Pulling MC Swag: |████████████████████████████████████████████------| 89.0% Dank
💦 Scraped 😩 2196 images totalling 268 megabytes
```
