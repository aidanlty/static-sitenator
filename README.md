# static-sitenator

A static site generator written in Python. Converts Markdown content files into a complete HTML site using a shared template.

## How it works

On page generation:

1. Removes all files in `docs/`
2. Static assets (CSS, images) are copied from `static/` into `docs/`
3. Markdown files in `content/` are converted to HTML and written to `docs/`
4. All pages are rendered using `template.html`

## Requirements

- Python 3.12

## Usage

### Run locally

```bash
./main.sh
```

Generates the site and serves it at `http://localhost:8888`.

### Build only

```bash
./build.sh
```

Generates the site with an absolute base path of `/static-sitenator/` (for deployment on GitHub Pages).

### Run tests

```bash
./test.sh
```

## Project structure

```
content/        # Markdown source files
static/         # Static assets (CSS, images)
src/            # Generator source code
template.html   # HTML template for page generation
docs/           # Generated site output
```

## Adding user content (`content/` and `static/`)

Add Markdown files anywhere under `content/`. The directory structure is mirrored in the output; 
<br>e.g. `content/blog/my-post/index.md` -> `docs/blog/my-post/index.html`.

Likewise for assets under `static/`. 
<br>e.g. `static/images/tolkien.png` -> `docs/images/tolkien.png`

Each Markdown file must have at least one `#`/`<h1>` heading. The page title will be set to the first one found.