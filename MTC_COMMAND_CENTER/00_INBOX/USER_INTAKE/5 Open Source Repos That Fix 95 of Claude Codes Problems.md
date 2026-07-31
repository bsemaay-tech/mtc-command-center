5 Open Source Repos That Fix 95% of Claude Code's Problems
Chase AI
https://youtu.be/IRPEfl2BD_c?si=wip9M_xCEf002jTH

These are the five open source tools
that I wish I knew about when I first
started using Claude Code. Because as
good as Claude Code is out of the box,
it still has some weak spots. Namely,
video, front-end design, memory,
research, and token output. These are
five areas that Cloud Code is naturally
sort of weak in, and we can improve it
drastically by bringing in these outside
tools. So, in this video, I'm going to
show you all five, how you use them, why
you should care, and the best part is
they're all free. Now, the first tool on
our list is Claude Video from Brad
Automates. This is at a little over
5,000 stars, so it's a bit smaller, but
this is one that's actually trending
pretty hard lately. And this is all
about giving Claude the ability to
ingest video. I don't care about
generating AI video. I want Claude to be
able to watch videos that I give it
because this is a functionality it does
not have out of the box. In fact, the
only major AI video model that sort of
does is Gemini. And if you're someone
who deals with video, you know what a
big deal this is because normally we're
stuck only looking at transcripts. And
transcripts are great, but sometimes we
need the context of what's literally
happening on the screen. The transcript
isn't enough. But this skill is the best
of both worlds because we not only get
the transcript, it's able to
intelligently pull screenshots or frames
out of the video itself when it deems
appropriate. And better yet, if a
transcript doesn't exist, it will
actually route it through Grock's
whisper model, which is totally free to
generate the transcript. So, if you're
watching some sort of video that's like
a Loom or something and doesn't come
with a transcript or whatever it is,
we're still okay. Now, the obvious
question here is, okay, well, like, how
does this actually work? How are we
dealing with video? Because we can't
just magically have Claude watch videos.
Every video is essentially a frame. So,
am I throwing it 24 screenshots times
every second of the video? The answer is
no. that would get crazy expensive.
Instead, the skills uses a pretty
elegant approach where it changes how
many frames it's going to grab from the
video based on what mode you put it in.
So, we have four different modes from
transcript to token burner. Transcript,
we're not grabbing any frames. We're
just taking the captions. For efficient,
it's just taking the key frames. So,
those are already dictated by the video
itself. And we take up to 50 depending
on the length of the video. We have
balance, which is where a lot of people
sit and will take up to 100 frames from
a video. and it's going to be based on
the scene changes, which is also taking
a look at the transcript to see if
certain words are being used. So,
balance probably makes the most sense.
But we also have token burner, which is
essentially the same as balance, but we
have no frame cap. You know, you could
take a,000 frames. The problem with this
obviously is time it takes to do this
and the amount of money we're going to
be spending. Now, Brad, the guy who
created this skill, also has his own
YouTube channel where he goes into much
more technical detail than I am. So, if
you really want to get, you know, into
the down and dirty of how this is
operating, definitely take a look at his
stuff. As for the installation, it's
really simple. You're able to install it
into the marketplace or you can just
give Claude Code the URL to this skill.
I'll put that in the comment. But big
picture, what is this bias? It gives us
a entirely new capability that Claude
Code normally does not have without us
having to do some janky routing through
Gemini and essentially pay a Gemini API
on top of Claude. This keeps it all
inhouse and is a great addition to your
cloud code stack. Now before we jump
into the next tool, a quick word from
today's sponsor, me. So I just released
my cloud code masterass and is the
number one way to go from zero to AI
dev, especially if you don't come from a
technical background. I assume you have
no knowledge coming in. We focus on real
use cases and it also includes a codeex
masterass. So if you're someone who
wants to get a little bit more serious
about AI, make sure to check it out.
There will be a link to it in the pin
comment. Now, tool number two is all
about research because out of the box,
the simple web search cloud code gives
us is fine, but it's pretty surface
level and there's really nothing when it
comes to a middle ground because the
opposite end of the spectrum is let's do
dynamic workflows, let's do deep
research, let's spin up 105 sub agents
and burn up 10 million tokens. I don't
want to do that. You probably don't
either. So, in comes Notebook LM-PI. For
all intents and purposes, this tool
gives us notebook LM inside of Claude
Code. I can call on Notebook LM through
the terminal. Everything I can do in
Notebook LM from the web version and
more can be done through Claude Code
because of this skill. It's not just a
skill, it's also a CLI. And so it's
essentially like an unofficial API into
Notebook LM. Now, the cool thing about
this isn't just like, oh, cool. We get
notebook LLM functionality, but when you
think about it, you're kind of getting
free LLM calls doing this. Now, it's
Gemini. It's not as powerful as
something like Opus and certainly Fable,
but you can offload some research and
some synthesis onto the Google servers
for free when you use Notebook LM.
Whether that's just asking questions
about videos or whatever. On top of the
fact that we can just create, you know,
whatever we want using Notebook LM,
whether that's, you know, slide decks,
whether that's infographics, whether
that's podcast, etc., etc., etc. And
like I alluded to before, we get stuff
that goes beyond the web UI itself. And
we have a full list right here inside of
the readme. In terms of the
installation, it has a pretty thorough
guide, but I'm going to be honest, all
you need to do, copy the URL, throw it
into a cloud code. It's going to do the
rest. It's going to require some things
like Playright, which is you've never
used before, is simply a browser
automation that's going to be completely
invisible to you when it's running. And
lastly, if you really can't think of any
use cases of notebook LM, there's a
whole list of them right here. For me,
the biggest one is simply looking at
YouTube videos. And this kind of goes
handinhand with what we were talking
about before with being able to watch
the videos. The notebook LM is going to
be just transcript only, but because
it's under the Google umbrella, like
it's it's a very seamless process of
supplying it with YouTube URLs, tons of
them on a particular topic and then
being able to synthesize all that
information at once. Now, tool number
three is all about memory. And I'll be
throwing in an additional tool here as
well. Now, when we talk about memory,
what we're really talking about is how
can I have clawed code quickly and
effectively answer questions about very
large code bases or very large corpuses
of documents. I want to be able to give
Claude Code a map that it can very
easily traverse to find answers for me
about a bunch of different questions
that are related to my documents, my
work, my code. Well, that is exactly
what Graphy does. It essentially creates
a knowledge graph of whatever code base
you give it. And you see that right
here. It breaks out all the parts. It
turns them into nodes. It clusters them
according to what they're actually
about. That way, again, we're handing
Cloud Code a map. So, when we ask
questions about things about this
codebase, there's a very clear path
forward from your question to the
answer. The thing you need to know,
though, is Graphify is not a rag system.
There's no vector index. There's no
embedding. This is not light rag. This
is somewhere in between obsidian and a
true rag system. But we can kind of get
like a light version of graph rag if
that kind of makes sense. It's not as
complicated as traditional rag yet we're
able to get a lot of the same benefits
in terms of the memory. Now the other
cool thing about Obsidian versus
something like Graphify is it can handle
a number of different files. Like we're
not talking just markdown. We can handle
stuff like PDFs. We can do images. We
can do video and audio on and on and on.
So it's very very flexible. But speaking
of Obsidian and knowledge graphs and
this sort of thing, let's kind of talk
about that bonus tool I alluded to
earlier. And that is the Obsidian skills
repo. I don't see enough people talking
about this. This is actually created by
the CEO of Obsidian. It's very simple.
It's just a handful of skills, but if
you're someone who uses Obsidian with
Claude Code, this is a easy way to
supercharge it. You're essentially
teaching Cloud Code the best practices
by the people who actually created
Obsidian. So, don't sleep on this repo
even though it's super simple. That'll
be linked below as well. Now, tool
number four is all about front-end
design, and that is impeccable. This is
quickly becoming my favorite front-end
design skill, and tons of people are
noticing it. It's not just that it has a
ton of stars. It's actually like
officially part of GitHub's AI package
itself. And what we're looking at right
here is Impeccable's website, and it's
here. I'll explain how this tool
actually works. So, Impeccable is one
skill, but it has 23 different commands.
And you can see all those commands over
here on the left that I'm going through.
Things like craft, shape, critique,
layout, colorize. and they're
essentially having the skill do certain
things with your claude code setup. So
colorize, for example, if I do
impeccable colorize, what's going to
happen? It's going to add strategic
color to monochrome interfaces. What's
nice here on the website is I can see a
before versus an after. And so you can
see, all right, here's what it would
normally look like with clawed code and
the standard cloud code front-end design
skill versus impeccable. And you can see
there's a bit more going on here. It
looks a bit nicer. Same thing for, you
know, boulder, right? Clawed code,
impeccable boulder. And there's 23
different commands here, which are
obviously like kind of difficult to
explain, and it's much easier just to
see them in action. So, highly suggest
you do that. The other really cool thing
with impeccable is the live mode. And
this definitely gives you shades of claw
design. The idea is that if I run
impeccable live, what's going to happen
is it's actually going to bring up my
web page on the local host on my
browser. So instead of trying to edit
everything through the terminal via
code, I will now have the page up on my
browser. I can click on different
components. I can see what it looks like
with and without impeccable. And it
becomes a visual design tool, which is
way better when we're talking about
front design versus like, hey,
impeccable, make that look nicer. Uh,
okay, try again. Uh, make it more
premium, right? So you can actually see
it before you commit it. I think this is
a huge step above the anthropic
front-end design skill and also a huge
step above things like UIUX Pro Max.
Now, last but not least is Ponytail and
this is all about token consumption.
Tokens, tokens, tokens. You hear about
this all the time and how expensive they
are, especially with Fable. So, it only
makes sense we look outside of Claude
code to see are there any skills or
frameworks that can reduce the amount of
tokens we are spending while still
maintaining the same level of
effectiveness. you know, it does us no
good if we reduce our token count, but
it gets worse. Well, Ponytail claims to
be able to do this. In fact, it claims
that it makes Claude Code 20% cheaper,
27% faster, while still giving the same
results, which is kind of wild. Now, the
way Ponytail essentially works is it's
saying, "Hey, we're going to give Claude
code these series of, you know, gates it
needs to pass where essentially we ask
it, hey, do you actually need to build
it? Does that feature you're trying to
create already exist? is it a library
etc etc etc before finally saying okay
you want to build this great thumbs up
just use the least amount of code that's
kind of how it works in a nutshell gets
a little more complicated than that but
I wanted to have you take a look here at
the benchmarks because this is what we
care about in the gray what do we have
we have the baseline and then in the
green we have ponytail and you can see
way less lines of code way less tokens
way cheaper and way less time now what
is the catch catch. Well, the catch is
they did these benchmarks with Haiku.
You at this point are using Opus or
you're using Fable. So, does this hold
up? Well, I actually did test I did a
whole video on Ponytail with Opus and it
actually was even cheaper and quicker
than what we see with Haiku. So, the
benefits were greater with Opus. I then
tried it again with Fable and same
thing. So, across the board when I ran
these same benchmarks and anyone can if
you go on this repo, they have all the
benchmarks listed here. So you can test
this yourself. Ponytail reduced it and
it was the same output. Now benchmarks
versus real life. Is it the same? Who's
to say? It probably depends on your
particular use case and how complicated
it is. But any chance we can make cloud
code faster and cheaper and have the
same level of effectiveness. I think we
should try it out. Worst case scenario,
you do a couple runs, you don't like it,
you get rid of it. But I think this is
worth your time. There's other ones in
the same vein like Caveman that I also
think you should take a look at. So,
those are the five open source tools
that I wish I knew about when I first
started with Claude Code. And if you're
brand new, I hope I was able to at least
point you in the right direction in a
few of these areas. As always, let me
know what you thought in the comments.
Make sure to check out Chase AI Plus if
you want to get your hands on the
masterass. And besides that, I'll see
you