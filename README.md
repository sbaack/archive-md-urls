# archive-md-urls: Turn URLs into archive.org snapshots in Markdown

`archive-md-urls` scans Markdown files for URLs and if possible turns them into links to snapshots from [archive.org](https://archive.org/). If a publication date can be extracted from the file ([more info](#how-publication-dates-are-detected)), the snapshots closest to this date will be used. If no date can be found, the latest available snapshots are used instead.

This is very useful when you use a static site generator for your personal homepage that supports Markdown for writing blogposts and pages, e.g. [Pelican](https://blog.getpelican.com/), [Jekyll](https://jekyllrb.com/) or [Hugo](https://gohugo.io/). Older content published years ago is likely to contain [link rot](https://en.wikipedia.org/wiki/Link_rot): links that are simply broken or now point to a different target compared to when you wrote the content. In an ideal scenario, `archive-md-urls` will not only fix these URLs, but also link to a snapshot that shows how a website or social media profile/post looked like when you wrote the content.

`archive-md-urls` tries to be smart and does not simply replace every URL it finds. Instead, it uses a [list of URLs which are considered 'stable'](https://github.com/sbaack/archive-md-urls/blob/ca28f9ef06d2e872ef57612322cd7232b6caa88d/src/archive_md_urls/scan_md.py#L10) and are therefore ignored: URLs that already point to archive.org snapshots, intra-site links (e.g. a link to another blogpost on the same homepage) and URLs that contain [persistent identifiers](http://en.wikipedia.org/wiki/Persistent_identifier).

## Example showcase

Input file `example_blogpost.md`:

```
Tile: Example blog post
author: Stefan
date: 2013-11-06

This fake blog post from 2013 links to [example.com](http://www.example.com/), a homepage that has dramatically changed in the meantime.

But it also links to URLs which can be considered 'stable':

- [here](https://web.archive.org/web/20000622042643/http://www.google.com/) we already link to an archive.org snapshot
- [here](https://doi.org/10.1080/32498327493.2014.358732798) the link contains a persistent identifier
- and [here]({filename}/blog/2012/2012-02-05-an-even-older-blogpost.md) we link to a different post on our own homepage (Pelican format, Jekyll and Hugo intra-site links are supported too)

In addition, google.com is mentioned but not explicitly linked.

And finally, [here](www.some-madeup-link-that-hasnt-been-archived.com) we link to a homepage that doesn't have any corresponding archive.org snapshots.
```

Output from `archive-md-urls example_blogpost.md`:

```
Tile: Example blog post
author: Stefan
date: 2013-11-06

This fake blog post from 2013 links to [example.com](http://web.archive.org/web/20131106211912/http://www.example.com/), a homepage that has dramatically changed in the meantime.

But it also links to URLs which can be considered 'stable':

- [here](https://web.archive.org/web/20000622042643/http://www.google.com/) we already link to an archive.org snapshot
- [here](https://doi.org/10.1080/32498327493.2014.358732798) the link contains a persistent identifier
- and [here]({filename}/blog/2012/2012-02-05-an-even-older-blogpost.md) we link to a different post on our own homepage (Pelican format, Jekyll and Hugo intra-site links are supported too)

In addition, google.com is mentioned but not explicitly linked.

And finally, [here](www.some-madeup-link-that-hasnt-been-archived.com) we link to a homepage that doesn't have any corresponding archive.org snapshots.
```

Note how only the first link to example.com has been altered and points to a snapshot close in time to the publication date of this fake blog post (6th November 2013). Also note that URLs which are mentioned but not explicitly linked are ignored.

## Install

You can install `archive-md-urls` via pip:

```sh
pip install archive-md-urls
```

However, using [Pipx](https://pypa.github.io/pipx/) is recommended:

```sh
pipx install archive-md-urls
```

## Usage

**Important**: `archive-md-urls` modifies your files directly in-place. It is recommended that the files you want to change are under version control so you can review the changes.

Once installed, you can pass any number of Markdown files or directories containing Markdown files to `archive-md-urls`:

```sh
# Update two files
archive-md-urls my-file.md another-file.md
Updated 13 links in 2 files.
# Update files in a directory
archive-md-urls myblog/content/blog/2014
Updated 97 links in 20 files.
# You can also combine files and directories
archive-md-urls myblog/content/blosg/2014 my-file.md
Updated 103 links 21 files.
```

By default, directories are not searched recursively for Markdown files. For recursive search, use the `-r` flag (use this with caution!):

```sh
# Update URLs in all Markdown files of myblog
archive-md-urls -r myblog/content
Updated 160 links in 32 files.
```

Note that Markdown files are identified by the file ending `.md`, other file endings are ignored.

## How publication dates are detected

First, `archve-md-urls` checks for a `date` field in Markdown metadata blocks (see [Python Markdown's format](https://python-markdown.github.io/extensions/meta_data/#syntax) and [YAML front matter](https://jekyllrb.com/docs/front-matter/)). If that fails, it tries to extract a date from the name of the file following [Jekyll's naming convention](https://jekyllrb.com/docs/structure/) where blog posts are named `YEAR-MONTH-DAY-title`.

Currently, `archive-md-urls` recognizes dates in the formats `YYYY-MM-DD` and `YYYY-DD-DD hh:msm`.

## A note about speed

`archive-md-urls` uses [asyncio](https://docs.python.org/3/library/asyncio.html) with [HTTPX](https://www.python-httpx.org/) to make asynchronous API calls. However, do not expect to get fast results, especially (but not only) when you try to change a larger amount of URLs. The [Wayback Machine API](https://archive.org/help/wayback_api.php) can be slow or even unavailable. If `archive-md-urls` has to cancel the operation because of that, just re-run it on the same files again later. Links that have already been updated before will be skipped because archive.org links are considered stable.