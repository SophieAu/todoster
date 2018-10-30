2018-08-30

On the train from Hamburg to Berlin and this is the first time I'm actually writing down all the specs for one of my asteriskster projects (which I decided is the umbrella term for all my *ster projects). You'd think there's not much to it but damn, actually writing proper specs trying to get everything on paper/into the text file is not that easy. It did help with figuring out the coupling between tasks and projects though. Note to self: Never allow the original of a foreign key to be changed. So now the projects will all have an id. And since they're potentially a foreign key, they cannot be deleted through the app. Of course manual deletion always works so it's not that big a deal.

Showing the tasks in different configurations (by date, project, location, ...) also showed its challenges. I have to figure out how to sub-sort the entries: First by the block-value, then differentiate between high-priority and normal priority, and then sort those by due date. But location plays into there too sometimes... Well, the rough plan is up but knowing myself it'll change a tonne until the first release...

And then there's the point around statistics-y things. Simple things like how many tasks done per block, total tasks done, ... How should I display those in the show commands?


2018-08-31

After starting on the implementation yesterday, I continued today and adding projects is almost done. The cli input did drive me insane though. I had like 2 or 3 endless loops which was kinda shitty. But in the end it just came down to the wrong exit condition. The worst thing was that it took me a while to figure out that `range()` needs a `list()` wrapper to be able to be used like a list. So doing `if 9 in range(0,10)` does not return true whereas `if 9 in list(range(0,10))` does. Argh! So annoying!!!!


2018-09-01

So I really ugly version of adding projects is done. The code is a fucking mess but it works! So exciting! Even saving and loading projects works fine. Pretty cool! To be fair, it worked out this faste because I was able to copy and paste from habitster and todoster. But why not? I'm only copying my own code so I don't feel bad about it.

So, while starting work on "show" I ran into a huge question: (How) am I going to display completed/past tasks? Right now I'm considering adding two toggles: --completed and --all. And out of these two toggles, I whole bunch of new specs came up which will probaby make the code a whole lot messier... Ah well, I'm doing this to myself so I shouldn't complain about it.

Another point that came into play, now that I started implementing `show` was the styling... What do I want bold, coloured, underlined, is there supposed to be aline under the headline, ... All good stuff that means changung the specs for all shows. Urgh, shouldn't have done specs beforehand! Just kidding, they're pretty cool actually.

At the end of the day, the specs had changes a bit regarding the styling but the contents were pretty solid. And I am pretty close to finishing the default show, with the project show being done completely. That was my whole Saturday but it is quite nice actually.


2018-09-02

Because I promised myself yesterday that I wouldn't do any todoist now, I only started work on the cli parsing, differentiating between show by project and show default. It only took 5 minutes so it wasn't too bad.

What was annoying though: I started actually using todoster and of course I found bugs. Including one pretty big one when it comes to parsing dates for new tasks... It wasn't a hard to fix bug but turns out copy pasting isn't always a good idea... For validating the date entry I was checking if the project value was empty which of course doesn't help the situation. At least it led me to add a tiny improvement where entering `-d "W40"` would work too.

In the evening after most of the other tasks were done, I got back to working on todoster and did mostly method extraction, as well as some stylistic refactoring for the show default "page".


2018-09-07

After doing the minimal thing yesterday (showing overdue tasks), I got around to doing ore today because I was on the train to Hamburg. Move number one: Don't show the backlog in default show. It's just way too long. After that (which was a pretty fast fix, literally commenting out two lines), I implemented checking tasks which worked pretty well too. Loading and saving I could copy paste and the functionality wasn't that hard. So nice.


2018-09-13

After quite a while of doing nothing/not much I'm back to working on todoster. Task one: Change `isDone` to `doneDate` since that makes it easier to check for when stuff got done in the end. As in analyze when I was most productive and all.

After starting on that: Nevermind. I did it for a few actions and then changed it back. Number one: I"m lazy. Number two: Chances are I won't check off a task the day I actually do it so the date would have to be entered manually which I'm not keen on. So back to a simple boolean it is.

On the train ride I did quite well I think, finishing the editing of a task (which admittedly could fail more gracefully) and I found and fixed a bug in the default show where completed tasks were marked as overdue. I actually managed to clean up the code a bit which made me happy. Clean code is pretty nice.


2018-09-15

After creating an alias for todoster yesterday and actually using it, I found quite a few small things that could be improved. Like: show the id when creating a task if you want to edit a task by its id. OTherwise it's kinda annoying to show all the tasks only to find the id of one of them. Also, changing the date by command line instead of interactive is really nice. And it works now, after not being implemented correctly either yesterday or the day before.

Also, I should seriously consider starting a git repo since the project is not getting any smaller. Also, I think my architecture is not the best after sitting in that meeting on Thursday. But then again, it's a side project and I understand my codebase. I might look into refactoring when I find the time. Right now I like it. And since I'm not even using object-orientation it feels like most of the architectures out there don't work anyways. Which might beg the question: Should I made use object orientation instead of essentially passing structs around? Ah, not thinking about this today, at least now, in the morning. Maybe later when all other tasks are done.

So in the afternoon, I read through 'The Goodies' in Think Python and `defaultdicts` are so nice! I used them right away in one of the 'show's. I also added a 'show backlog' view because I'm tired of calling show projects everytime I just wanna see what's in the backlog. It's not a perfect solution but it works for now.

Even later I got around to implementing task deletion which was pretty easy. But looking at my code after being told about architecture, I really see how messy my code base is. I could've used a few classes or so but for now it works I guess. Not looking forward to the huge rewrite in a year or so though. Or actually I am. I love refactoring.


2018-09-16

Back on the train, which means back to train-work. I didn't get too much done though because I was tired as hell. Some things did happen though: Turns out the way I saved the weeks of tasks was kinda shitty. So in I went and changed them. It wasn't as hard as I thought it was gonna be but still. I've also come to the point where I'm seriously considering moving to objects for my projects and tasks. But I haven't come any further than considering.
Aside from that week thing, I've been doing some more bug fixing but nothing too exciting.
By the way, all of this came out of trying to implement show by date. Didn't finish that todo though because of all the side-tracking.


2018-09-20

So yeah, I think I've come to the point where I really want to have objects. I now have to filter tasks by wether or not they're done and/or in the past and with the copy pasting I've been doing it's gonna be a major pain in the arse. Also, outside of the project view, tasks that belong to an inactive project are not hidden.

On the good side: It took me less than an hour to implement the last two missing views due to some very simple copy pasting. It's still an extremely shitty codebase but stuff works.

Before finishing everything I'm actually gonna sit down with pen and paper and write down exactly what I want, what makes the views different and what algorithms I could use to make everything easier to adapt and extend. And maybe I will introduce objects... But who knows.

At home I did more bug fixing, especiall on show_default and started putting the isoweek package everywhere. it's so much nicer than calculating eveything by hand. I also changed the requirements for the flags so that the flags do the same thing in every view. Makes it a lot easier for me to implement and hopefully also makes it easier to use.

Also, I started writing down requirements and the sorting and grouping on paper. It was super helpful. I really should do this more often. When I started implementing my notes it turned out that the code is actually even simpler than on paper which was lovely. My guinee pigs for the while new show setup are show_default and show_by_project and I think they're shaping up really well.

On a slightly different note, I decided on a new view which is `td list projects`. It kinda sucks to do a show_by_project everytime just to see all the projects. And I have way too many projects anyways. Having a list of them would be nice to see which ones I should eliminate.


2018-09-21

After work (and shopping) I continued pulling stuff apart and making things reusable. I'm passing along a lot more parameters now but the whole codebase is becoming so much nicer that I almost don't care anymore. And I'm sure that when the glaring bullshit is cleaned up, a few of the parameters will leave again.


2018-09-22

Just like the last few days, I've continued cleaning up and show_backlog is now super clean. 6 lines of code and 1 import statement are all that's left. It's amazing <3

So yeah, aside from deleting projects I'm done with everything. Outside the shows, the code is still a mess but I'm done. It's pretty cool actually. So exciting. I wrote up the specs for deleting projects though so I'll never actually finish this project. And the refactoring for the add/delete/edit suff is gonna be such a pain in the ass. But I think I can get there fairly soon-ish. Definitely before going to Sylt!


2018-09-23

Guess who thinks they have finished all the specs! This person. I got the project deletion done in half an hour and all I need to do now is go through all specs again and then do some refactoring. Then I'm done! Party Emoji!

The only annoying part: Using todoster and finding week-related bugs because I changed the format like 3 times... Even worse: Thinking that's the issue when it isn't. Turns out it really was a bug around that. Because I was checking for a yyyy-ww format when I had a yyyyWww format. Awkward. You know what would really help: Unit tests. Or any tests really. Ah well....

And all the other minor issues like the week date format parser not working when you're going for lower case letters. I really should write some tests after the fact.

Or when you want to add a new task and the formatter expects task["project"] to be the shortcode when you changed it to the id a few weeks back it feels like but you never tested for that...


2018-09-24

Just some more refactoring for a bit on the train. Nothing special. I'm planning on doing better argument parsing though and I decided that I need to really do some testing. Bookmarked a lot but didn't act on it (yet)


2018-09-25

After Monday's bookmarking spree, I started using argparse to parse all the cli parameters and while it's kind of a lot of work it's really nice and potentially super useful in handling defaults and edge cases. All the old code is breaking at the moment but once everything is set up it should run as smooth as warm butter.

Funny thing while going through everything: I had a spec for deactivating a project which in retrospect was super unnecessary. I can just deactivate a project using the edit function...

I also made listing all project the default command of `todoster p` because lazyness and why not. It does make sense so hey.


2018-09-27

Back on the train and back to working on todoster, Now that the new cli parser is up and running, I've cleaned up adding tasks. I've also started actually using pylint which is actually pretty helpful. Makes code miuch simpler generally and I just liek cleaning thigs up in general so all bueno.

Fun fact: Cleaning up the add_task code led to a reduction of a ton of code. I deleted some over-the-top functionality admittedly but still, the code is much nicer now. I don't think I even learned that much in the last few week but apparently I did something right... Ah well, there's still a ton to go and I don't think it's gonna get done before November so I better get cracking as much as possible.

Maybe I can get everything done by the end of the post-Sylt week so that I can invest all my time into the spicy site and peopster. Those are my two big goals until the end of the year anyways.


2018-09-29

Finally got all the task-related stuff done. Literally at the last second. And oh my god, I hate my life! I really should've started off with tests. Number one was how I'm checking tasks for their projects and number two was for how to differentiate between a field not being set and a field being deleted.

Regarding number one: Because efficiency I sometimes assigned the right project to a task but other times I just left the project id which messed up the formatter. In the end, now all tasks should have  while project assigned to them when they go into the formatter.

And regarding number two: I messed around with None vs empty string until it worked.


2018-10-06

Turns out those fucking Nones are more work than it's worth really. But I don't know any better options right now... I fixed them somehow, but don't ask me how safe this is. I really need to write those tests soon.


2018-10-07

Back on the train. Which means back to coding time. No internet though since this is an IC so I'll have to guess a lot of stuff instead of being able to use the amazing ICE wifi /s.

This time, I was working on all the project-related stuff and turns out the code I wrote last (the project deletion) was much cleaner than the code I wrote first. Go me! still, tests would be nice. But that's not for today. Today I'm all about that refactoring.

And I did get all the refactoring round 1 done. Yay me. I mean it still got 0% test coverage but aside from that it looks pretty decent. actually quite happy about everything. Could've been a lot worse. But copy-pasting to the rescue. I really should test though. Like seriously. Otherwise I'm gonna murder someone probably.

One last-second change of heart though: All the show_* should be in one file. There's no reason for them to be in like 6 different files (aside from the date-related shows being really long maybe...). But that's a task for not-now since I'm arriving in like 5 minutes.


2018-10-10

Back on the train and with that back to working on todoster. I've been using it the last few days and it was going pretty well actuall. I'm considering adding a new show method though which shows all the plans for the current week. I'd be nice for my over-planning but I'm not sure if I should actively encourage planning for more than tomorrow. I'm not deciding this right now though, so....

Anyways, I started writing tests and fixed a few date formats I wanted to be valid but they weren't which is nice. I started testing regex though so the tests were a fucking hassle to write. I had to have like 15 assertions to check if a input date has the right format. And I'm not even properly testing all negative cases. I'm just hoping/making sure that if an invalid format makes it through, it's caught later.

At least I realized that formerly `is_valid_date` is really only checking for the format and renamed it to `is_valid_date_format`. Same with week by the way.

Also, so many tiny bugs were fixed in the evening (more like 2 and a half). Tests might have actuallt caught them but who knows...

Oh, and I just realized that mocking the file actions won't be that big a deal probably. I'll have to mock all the functions and that's it. I'll only have to see how I'm gonna do file operations when I get to testing all that stuff. But that's gonna be last probably. Mocking the arguments from argparse might be a bigger issue. But chanced are that someone else already figured that one out. So I should be fine.

Both of the above things won't happen this week though because I'm pretty sure there's some required googleing involved and that's hard to do without internet...


2018-10-13

So, turns out there were a few more bugs. The ones I found got fixed though. Other than that, I'm happily refactoring and testing away. The datetime_handler is done and renamed to date_handler and I think I'm getting the hang of it. I won't be getting done this weekend I think but next week is very much realistic. The refactoring is probably gonna be more time-intense than the testing but that's the more fun part so I don't mind.

On a semi-related side note: Turns out, todoster is the most complex of my python tools so I should be fine when I get to snipster and lifester. I mean I'm even cutting some features so getting them done in 2 weeks max is doable.

2018-10-14

After writing tests almost all day and getting done I decided to switch to bug-driven testing from now on. I think I have a decent baseline of tests and I honestly just can't be bothered anymore. From now on, tests will only be written when something goes wrong.


2018-10-25

After taking a break from todoster dev for a while to almost finish the imp-splen-site (damn those last minute issues) I'm back to hating unit testing for output. The good thing is, that during the last two weeks of non-dev but lots of usage I couldn't find too many issues and actually really liked working with the app. So it can't be too bad.


2018-10-26

So... The "I'll only write tests for bugs" strategy didn't go down too well. I wrote all the tests. At least the ones that didn't involve mocking the input. So task and project deletion are going to be finished on Monday. Still, in the end, writing all the tests wasn't too much of a hassle. The tests are ugly as hell but at least they seem to do their job.


2018-10-27

After finishing up all the tests yesterday I worked through the 12 Factor CLI App today. Which mostly involved writing the help messages. Made me reconsider quite a few of my command though. E.g. I've decided to remove the edit prompt for both tasks and projects. Don't really need it. And I changed the commands here and there a bit too. Renaming, remove default stuff and the biggest change: Task actions are now gonna be `td task something` instead of ``td something`. With the abbreviated version it's two characters more but it does make for a clean interface.

Turns out that 12 Factor CLI App thing was pretty awesome. Gave me a lot of cool ideas and helped me struture my app better. With that new structure come more changes though. But that's what I have tomorrow for.


2018-10-28

Today I finally managed to work through most of my todoster todo list (so meta). Turns out, setting that TODOSTER_DIR as an env var: Not that easy. In the end, setting the default path looked like this: `os.getenv("HOME") + "/.todoster"` Kinda ugly but at least it works.

With the prompt-editing gone, I also got around to cleaning up the parsing code and turns out there's one neat little helper:  `a = b or c`. Learned it at work in javascript, works in python too. So nice! Unfortunately, I'm not done yet though because urgh, so much todo. It's fun though so I'm not really complaining that much. The only thing I'm complaining about: The readme. I am so not looking forward to creating all those gifs. I don't feel like doing them but I also feel weirdly compelled to do them. Go me!, not being schezophrenic at all.


2018-10-29

So, after leaving early from work because I didn't feel too well I of course didn't relax but instead finished everything except the readme and the change/delete/nothing issue around editing fields. Turns out, subclassing argparse is not a cool move and the people will just have to live with a shitty help message. At least the readme will have all the fancy help messages so that's where people can look up how to use things. If there are people. I also got the tests running again after moving everything into sub-folders and it involves a lot of adding module names but it wasn't too complicated...


2018-10-30

Done! Finished copy pasting the help into the readme, found a bug to fix and did the editing/... thing with a bit of resistance but that's it. I'm done. Now I only need to release tomorrow and that's it for now. There's probably still a few bugs here and there but that's it. On to the next project.