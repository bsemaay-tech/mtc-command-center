Claude Fable 5 Just Built the Ultimate Agent Harness
Pat Simmons
https://youtu.be/HhWwllcbc2g?si=XMCBp74vJF7WWCNI

AI agents are everywhere. But there are
two problems. First, pick one and you're
stuck with it inside their model or
inside their platform. Second, it is
complete chaos. You might have a pile of
chat windows inside different apps like
Telegram and Slack, different repos
inside Cloud Code and Codeex, and
absolutely no system to any of it. If
you're using an agent platform, the
context switching alone is killing your
productivity. But what if I told you
there's one app that will run all of
them? Any agent, any model, all in a
single place? That is exactly what we're
going to build today. And no, this isn't
Hermes or Open Claw. It runs on the
subscriptions you already pay for. We're
not going to get into any toos gray
areas and all of your agents, all of
your chat windows can be accessed inside
this platform we're about to build. So,
in this video, I'll show you how to
build out this agent harness completely
from scratch with Fable 5. We'll get it
running in a single command. And by the
end, you'll have the whole system ready
to start building out your own team of
agents, even if you've never built an
agent before. So, not wasting any more
time, let's dive right in to the build.
But first, let me explain what I'm
envisioning for this harness. So here is
the mockup I sketched out. Please ignore
the chicken scratch. But the basic idea
is we have a category on the left for
each one of these agents. A good
category could be say YouTube. And under
the category we have different agents
assigned to different parts of YouTube.
The first agent could be a script writer
agent. This second agent could be a
motion graphic creator agent. Another
agent might monitor analytics. And the
big idea here is if I select an agent,
once I select that agent under the
category, then I can open tabs here
almost like Chrome browser tabs. And
each one of these will be a terminal
session that will allow me to connect to
different models, whether it's Opus,
GPT, or any open- source model. And each
one of these terminal tabs could be
three different scripts I'm working on
at one time. I, for one, I'm incredibly
scatterrained. You might be, too. And I
want a system that can keep all of the
different things I'm working on nice and
organized because typically I'm working
on multiple scripts at a time. And the
same will probably be true for editing
or motion graphics for analytics as
well. So that's the basic premise and
this is not a whole lot different than
how they've architected codecs. If we
look at codecs, we could in theory in
these projects organize it in a way
where each project has a folder assigned
to each agent. However, we still run
into issues when I want to create new
tabs at the top. The tabs are on the
lefth hand side here instead and I could
be chatting with different agents at one
time. But if I have say, I don't know,
15 agents, it starts to get really
cumbersome when I have all the different
projects I have to scroll through. If
that's confusing at all, let me show you
a few examples that get closer to what
I'm thinking. They are called ADES or
agentic development environments. There
are a bunch of them. Semox is a good
example. The way they have architected
this is they have these repos or agent
tabs on the left and then they have tabs
within each agent. However, these tabs
are kind of all over the place. It it
starts to get really confusing, but this
is more like the general premise. There
is another healthc conductor.build that
to me is a little less confusing. Agents
on the left, tabs at the top. But each
of these still feel more like aic coding
environments. And a lot of these agents
that I want to build out aren't
necessarily focused on coding. So, we're
going to take pieces from each of these.
And the beauty is they are open source.
So, I can go to their GitHub repos and
start to duct tape my own customized
version together into something that I'm
actually happy with. So, that being
said, let's now go back to Fable and
start brainstorming this.
So, we will open up a new session in
terminal here with Fable 5 model Fable.
I'm going to paste in this prompt. I
will put it on screen. Essentially what
I am saying is I'm building an ADE. I
run agents for everything. Writing,
content, coding. I want one app where
all of them will live. I give some
examples like the ones we discussed. I
say start from superset actually because
I take that back as I looked further
into this. Conductor.build is not open
source. So what we're going to do is
we're going to use superset instead
which is very similar looking. Here is
superset. Same kind of idea. They have
an open source repo I can pull from. And
then I'm going to take some screenshots
from the actual conductor interface,
paste that into Fable as well. And then
the rest of the prompt is basically just
describing what I already went through.
So the rails, the terminal tabs, each
workspace is its own repo. And I talked
about onboarding as well, which we'll
get into once we actually get the the UI
set up. But the basic idea of onboarding
is I want it to be as simple as possible
for the user. So the minute they open
the application, they are asked to
create agents, agent categories, and
then agents under those categories. So
that's the idea. And what we're doing as
well is we're using a fable
orchestration skill that I put together
based on this anthropic documentation
here titled prompting fable 5. They get
into a lot of the details around this.
So I fed this into a separate agent and
we built out a skill based on this and
that skill can be found here. I will
include this in the description below
but it is more or less what anthropic
details and their docs here just
organize into a nice easy use skill for
an agent.
And in about 20 minutes, we have our
first mockup alive. Interestingly, it
used colada artifacts here. I'm not
exactly sure why. Maybe that's a fable
thing, but I mean, it should work just
as well as a local host. So, if we go to
this link here, and here it is. It's
looking pretty good. I fed it a
screenshot of conductor. And you can see
how similar it is to conductor. We have
categories on the left. Under those, the
actual agents, these emojis, of course,
are obnoxious. I don't think we need
changes. It basically just matched
exactly what I gave it the screenshot.
So, it added changes, checks, run
terminal setup. We don't need all of
that. A lot of this is superfluous. It
also added a light mode, so that needs
to be fixed. These emojis, of course,
are driving me absolutely nuts, but I
like the little tab here. I like the
loading indicators. It's organized by
agents. We can add a new category. We
can name it, but create category. And
that actually works. Nice. And then you
can add an agent test. Cool. And you can
go different models, which we will get
into setting up. So, this is not a bad
first pass. I'm going to give it
feedback. One big thing that I see is
it's not actually showing terminal,
which it needs to actually connect to a
terminal window, as in it needs to run
directly through the CLI. And it looks
like it's just like its own interface
right now, especially when I go light
mode. You can see it's like got its own
little interface. So, I'm going to give
Fable all of that feedback and then
we'll come back for version two. And
just in case you're curious, here is the
follow-up feedback that I gave. I will
put this on screen now, but it's
basically describing exactly what I
said. Getting rid of emojis and ability
to add a profile photo, connecting the
CLIs, stripping back some of these
extraneous designs and functions here.
And while that builds, Claude and I just
thought of the name of this application,
which is going to be Damon, D- A M O N,
which comes from a play off of Demon,
Dae M O N, which if you're not familiar,
is a computer program that runs in the
background as an independent process.
And actually back in the day they came
up with this term based on the Greek for
d aim o n which in Greek was a
supernatural entity often seen as a
guardian or spirit. So it's kind of like
a like a little helper which is fitting
for this agent application. Anyway, back
to the build and v3 is now live. So
let's check out this latest version. It
is looking pretty good. Looks like most
of my feedback is in agent files on the
right. We've got these tabs at the top.
We've got our categories and then under
that is agents. We have these nice
little loading indicators. New category.
Upload photo. Oh, does this actually
work. Just use this random photo for my
Fable 5 video game. Uh test. Oh yeah,
look at that. Works. Okay, cool. So, we
are all set up, ready to go. I'm going
to go back to this agent and tell it now
to build this out into a proper Mac
application.
Okay. And in about I'd say an hour and a
half of building, we have something
ready to go. A Mac application of this
agents platform for us to react to.
Fable is not fast, but it is incredibly
thorough. It had spawned a ton of
different agents and just went through
this entire build process. So let's see
what this app is looking like. It's
telling me to run this install command.
I'm just going to say, can you run this
yourself? Okay, so it looks like we have
our Mac app up and running. We've
migrated over from that mockup. So,
let's check how the Mac app is looking.
How do I see this? And here it is. So,
it's looking pretty good. It's pretty
bare bones, but we should be able to add
teams here. What I was calling category
before. Upload a photo. We're going to
do YouTube first. I have this image
YouTube. We're going to call this
YouTube. Create a category. And then we
have an ability to under this exactly
like I described. Looks like this is
working. Adding a new agent. We'll call
this uh it's a good script writer name.
Then I can just add a photo here. Just
going to do a random photo of something.
Here we go. This uh video game
screenshot for my Unreal Engine MCP
video. Good enough. And then right now
it's only working for Claude. So the
runtime is going to be Clawed as in
we're using our Claude subscription. And
this actually didn't even ask for this.
Maybe this came from Conductor or
Superset. But this is really nice
because you can if you'd like bring in
an existing GitHub repository. Say you
have an agent living in a GitHub
repository. Maybe you already have
agents and they're not in GitHub yet.
You could theoretically put those in the
cloud on GitHub, then upload them
directly from here with this URL and
just clone them and automatically upload
them into our Damon app here. So I'm
just going to do new empty repo and then
I believe it's going to create a folder
locally. Oh wow. Okay, it already opens
up claude. So okay, yeah, here is the
folder that it's opening up locally. ad
default agents and then it's just this
string and then /worktree and I can go
yes I trust this folder and boom so we
have earnest our script writing agent
all set up you can also go new tab
create a new session here another
session with nest we should be able to
if I go command I yep change the name of
this so say this is a video about AI
tools and then and this other one could
be about say codecs so we have two
different scripts being written we've
got Earnest our script writing agent all
in there we keep track of this we can
another agent in a new empty repo. And
then we have all of our agents here
assigned to different tasks related to
YouTube. And the way it does that is if
I just go command T. It's just doing the
claw dangerously skip permissions
command. This is just a terminal here
and I'm already logged into my cloud
subscription. So it automatically just
opens this up. So if you were to open
this up yourself, you just need to a one
time and it'll allow you to do the same.
At the end of the video, I'll get into
onboarding and actually setting this up
from scratch to make sure that people
have access to this and can start this
up themselves. But for now, this is
looking good. And this is the beauty of
Fable, by the way. You give it feedback
and it just does it. There have been no
revisions off camera. All it took was
what, three iterations to get here. It
is very fun working with such a capable
model like this. Now, the problem with
this is we're only able to access Claude
code like I just showed. And the whole
point was running any model I want as
well as my Claude subscription. So, how
do I get any model I want accessible
within our Damon agent application?
Well, honestly, I don't even know. So,
we're going to go back to Fable and
we're going to tell Fable. All right,
this is looking good. Everything is
approved. Now, what I want to do is have
an ability to add my chatbt subscription
as well and log into I guess it would be
technically codecs and use GPT55 within
this as well as any open- source model.
And so, I don't know exactly how we can
set it up with these different open-
source models. I'm assuming the easiest
way to do this is through an open router
API key, but I want an ability to when I
open up the application, press that new
tab button. Below the tabs, there should
be an ability to select GBT, Collad of
course, then OpenAI logo, then some
popular open source models like Kimmy
K27, Miniax M3, and GLM52 with their
logos as well. So I can just click those
and it will automatically open a session
with that open source model. And so I
think to get those open source models,
the easiest way to do this is to just
use an open router API key and we can
just select all of these. I'll let you
be the judge of all of this. Let's go
ahead and spawn agents and do this next.
All right, our new build is live. So, we
have an ability now to choose from
different models. Claude, OpenAI, Kimmy,
Miniax, GLM, and we should have little
indicators, little icons to actually
choose from these. So, let's check this
out. Okay, looking pretty good. We've
got the actual icons here to choose
from. Miniax. Can't actually see that
logo. Change that. GLM 5.2. Not sure if
that's the right logo. Need to change
that. But what we can do, let's see if
this actually works. Give me K. Okay. So
nice. We have this. Enter your Open
Router API key. So I'm going to do that
now. This should work the exact same way
once you download this application,
which again we're going to get into how
to actually do that. But if I just go
here, if I go to Open Router right now,
sign up for Open Router if you haven't
already, but I'm going to assume that
you're signed up. Go to workspaces, API
keys. I just blurred that out, but I
went create new API key. Hit create.
Make sure you've got some credits added.
And then I can go back to our
application. Kimmy K. paste in my open
router API key. Save and launch. And
then it automatically will do this to
where it will connect. So we're using
the anthropic base URL. So this is
loaded in the cloud code harness. This
is the easiest way to do it. And I don't
want to get too in the weeds here, but
what it's doing is it's just pointing to
the open router API endpoint. We have
our open router API key that I just
added. And then it's calling this model
moonshot give me K27 via Open Router.
And then I can say, hey, and it looks
like I'm running into an issue here. 41
missing authentication header. Not sure
what's going on there. I just went back
to Fable, asked Fable to figure this
out, and I'll fix this quickly. Also,
while Fable's at it, can you change the
Miniax logo to be white mode? Find the
logo. All right, some quick revisions to
the model pickers. We have updated logos
here. And we should now have an ability
apparently to open up any model here.
KimK27. Hey, what model are you? Cool.
I'm running with the Kimk 27 coder model
backend. So now we have an ability to
use any model with any agent whether
it's claude codeex or an open- source
one straight through open router except
now we've introduced another problem
which is if I close a tab the agent's
not going to remember anything. We
haven't set up the proper markdown files
yet instructing the agent on who it is
and what it does and have some sort of
memory system and self-improving system
that makes this truly agentic. So that's
what we're going to set up next and it's
going to be stored in this file section
here. This is why I created this drawer
here to have a quick ability to click
through and see exactly how we've
configured this agent. So that's what we
got next. We're going to go back to
Fable and explain. Perfect. All
approved. Now what I need is for us to
build out agents files. So agents.mmd a
memory.mmd and anything else that Hermes
does. I need you to go through the
Hermes GitHub repo here, determine how
they have their agents self-improving,
and then I want you to just fork Hermes
and bring it right over. And that will
be our agent structure. So, it's easier
for me to just use something that
already exists. I know Hermes has
probably the best agent memory that
they've configured. And the beauty of
this is it's fully open source. So, I
can give this to my agent, have it parse
through, find how they've structured the
memory, and kind of self-improving
system with their harness, and use this
for our own agents.
All right. So, Fable grabbed the Hermes
GitHub repo, brought over exactly how
they structure this agent.mmd, userd,
memory.mmd, and this should now be set
up in our application. So if we go back
to our AD, we should now have this set
up. Yeah. So we have these files here,
claw.md, and then we also have these
agent files here. And so each one of
these are a markdown file, which
essentially makes up the agent. By the
way, if any of this is confusing at all
on the files that actually make up an
agent or you just want to learn more on
how to build your own agents from
scratch, you can check out this video.
I'll link it above. It's a full course
on building out AI agents. I'll also
link another video above which is zero
to your first AI agent in like 10
minutes. It'll give you a complete
walkthrough on all of this. But these
are essentially the files that make up
our agent. And we pulled this directly
from Hermes. So we have our agent.mmd
which just tells the agent who they are
and what their role is. So you're
earnest. This is just a template it
looks like. So it's saying you're an
autonomous coding agent which is
incorrect. And then here's the operating
brief on how to actually access the rest
of these files and update the rest of
these files. For example, memory.mmd
updating those as well which it should
do automatically after each session. But
now we have an agent that is actually up
and running. And what I would suggest
you doing because there is some
optimizations. Like I said this is just
a template. So, what you can do is just
open up your agent here. I'm going to
open this up in Claude and just say,
"Hey, I want to update your agent.MD.
You are earnest a script writer for my
YT channel. Need you to help me with
hooks and and outlines." And so, it's
updating. It's agent.mmd. And then you
can continue to chat with it. And as you
work with it, it's just going to get
better over time. All right. So, we now
have an agent configured with the proper
markdown files from an agent.mmd
identifying what it is to a memory. And
this ADE is about built. So the last
part of this is actually showing you how
to set this up yourself because I've
been building this with Fable, but we
now have a public GitHub repo for you to
access and download yourself. So that's
exactly what I'm going to walk through
next. Okay, so I need to make this
accessible in a public GitHub repo for
people to download. Make sure that you
strip away all the secret keys and
whatnot. Organize this, make it nice and
clean, have a walkthrough guide, and it
should just download this Electron app,
right? Do we need to do anything with
the Electron app to get the set up
properly? make sure this is super easy
for people and we go through that exact
same onboarding that we had previously
where we can, you know, create
categories, create agents, add profile
photos, all of that.
Okay, so Fable has set up our GitHub
repo and an ability to download this
application yourself. So, we're going to
do that now by going to this link here,
which I of course will include in the
description. We've got this GitHub repo
and I can install this. So download the
signed DMG from the latest release. Open
it and then just click this DMG here.
It'll download. Also, sorry Windows
users. This is only for Mac, but feel
free to still clone this repo and you
should be able to with Claude build out
a proper Windows application relatively
easily. Okay. And then just open this
download here. Here's the DMG. A nice
little icon here. Just drag this into
your applications. Then go to
applications. Look for AD here. Here it
is. It's going to ask you to open it.
And you will see a blank screen exactly
like we saw when we first set this up.
So you can create a new team here. Test.
Add a photo. Let's just call this
YouTube again. Add a photo. Create
category aka team. A bunch of these are
just agents I was experimenting with.
They're creating out. So you can ignore
those. They should be blank for you.
This like the whole thing should be
blank for you. And then all you need to
do is create an agent. So we're going to
say earnest use a random image. There we
go. Simmons bench badge. Create agent.
And it'll just automatically open up
claude. And then if you want to open up
say Codex or anything like that, you
just click there. You'll ask to sign
into your Codex subscription or your
OpenAI subscription and then you'll be
able to access that as well. So that is
setup. You can see really simple to do.
We have our agent files here and work
with your agent on what you want the
agent to do. But that's how simple setup
is as well. Now I could keep going with
this and building out more agents
because we've really only scratched the
surface on the different categories, the
different types of agents that you could
build, but that is beyond the scope of
this video. So, what I'm going to do is
I'm going to create a separate full
walkthrough on building out more of
these agents yourself and turning this
into a proper quote agentic operating
system. And in that video, I'll go
through every agent I actually use from
script writing to ones that help me with
content, newsletters, all of that cuz I
have a ton. That was also the purpose of
this video was creating an AD for myself
to run all these agents to actually
orchestrate all these agents. But for
now, this is more than enough to get you
started building your own ADE and start
getting agents running completely for
free using your existing subscriptions.
Anyway, that is going to do it for this
one and I'll see you in the next