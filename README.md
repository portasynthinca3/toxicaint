# toxicAInt
Protect your copyright by poisoning AI crawlers.

### How?
Toxicaint takes a static website and generates a copy of it with all text
replaced by generated text-like slop. It's an active measure against AI crawlers
that don't respect `robots.txt`. If your website is not statically generated,
then I'm sorry, this tool won't be able to help you out here. If you're a web
developer, you're free to port this idea to your framework of choice.

This tool does not detect AI, it only generates a slop version of your website
that can be fed to AI instead of the real one. Probably the simplest way to
detect these crawlers is via their reported User-Agent[^1].

### Why?
  - AI crawlers are known to disrespect `robots.txt`.
  - Poisoning, as opposed to simple denial of access, is an active measure that
    has more of a long term effect.
  - Artists have already been using poisoning tools such as Nightshade; it's
    time for us techies to join them.

## Usage
Clone the repo:
```
git clone https://github.com/portasynthinca3/toxicaint.git
cd toxicaint
```

Install dependencies:
```
poetry install
```

Run:
```
poetry run ./toxicaint.py source_directory destination_directory
```

It's as simple as that!

[^1]: See [ai.robots.txt](https://github.com/ai-robots-txt/ai.robots.txt) for a
      list. Because some of these crawlers disrespect `robots.txt` already, I
      guess it's only a matter of time before before they start misreporting the
      User-Agent, if they don't do so already. Discussions about how to best
      detect the crawlers are, although outside of the scope of the tool itself,
      welcome.
