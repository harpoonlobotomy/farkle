
starting this one a bit late, already made a pretty full-functioned TUI version and am a decent way into the GUI version (though it's not that pretty yet, working on function first).
Started at the start of this month, so it's been a little over a week.

Current issues:

(* points from this roll for comp adds turn_score, not the recent roll.)
* ^ done


(* player: if all dice selected, 'reroll' doesn't reroll
    Well no, that's not true: if some of the dice aren't actually viable selections to take the value from, it /does/ reroll what it should. But if all options are viable, it rerolls none (ie if all 6 die can be viably taken and then rerolled)
    Same thing whether they're all rerollable in a single roll or if some are used and others are held.

    It's because I changed
    mark_used(held_dice)
    to
    mark_used(new_used_dice) - the change made it stop holding things it shouldn't (ie if I select '1, 2' and reroll, it would keep the '2' despite it not being a viable selection.) But because it was exclusively marking new dice for some reason it didn't correctly hit the 'if all 6 die are used' mark. Not sure why that'd happen.

    Oh - it's because it only makes /those/ as used, so anything added in the most recent roll won't be re-marked)
* ^ done

* i wish the npc player's dice value showed up before it rerolls.
    The timing is just a bit off. Doesn't matter functionally but it's less than ideal.

* oh, and I need to re-setup the output to JSON at some point, that was useful.

(working on the 'all held dice' issue.
    new_used_dice and held_dice are identical. Why is it breaking then?

    OH - it's not that, it's this:
    roll_dice(used_dice, do_refresh=True)
    It /does/ correctly recognise that all dies are able to be rerolled, but because I'm sending 'used_dice' it doesn't actually reroll any die - because inside roll_dice it's told to:
        *if die_inst in used_dice:*
            *continue*
    Okay. can fix that.)
* ^ Fixed now.

* fixed the issue of an error popup is the titlebar is enabled and you closed the window using it. Now it doesn't error at all. (It was trying to update the dice after the window had been closed.)

* Oh, interesting followup - the comp player's dice are rerolling even when used.
    Hm. So - fixed a line that required a die to be /both/ used and held to not roll, which is good. but now they're never marked as Used, they stay held.

Another minor note: the comp's dice don't roll from left to right. So if all dice are 'held', on 'roll' they become 'used' in a random order. V minor but annoying.

Hm. Currentl;y, comp wins with "2750 points!" if they win, because the score isn't applied to their gamescore before the winner announcement is output. Need to fix that. Makes it confusing as to what's happened if you don't know the bones of it.

* fix spacing for points line - needs more space below or less above to even out

`points from this roll` needs to update for npc before it takes score. Feels slow when you don't see it update first.

player should have all held dice 'used' before the reroll does, instead of applying 'used' as part of the same loop. Again, doesn't matter but feels wrong.

fixed minor bug where deselecting the only selected dice would make get_score throw a fit.

14/4/26
Have worked on all of the above, will need to double check but think they're all done.
Today working on re-implementing both the outputter to json and the farkle_settings.json, and saving user settings to the JSON.
* also, need to add a 'restore to defaults' settings option if they want the original settings back.

Things I need to add to settings to make this work (so it always grabs from settings, user settings if found else default settings):
 - player colours - added to settings as 'playerx_col
 - keep on top

Removed 'used_dice' as a global var, I don't think it was used anymore.

11.35am

Can now save user settings to JSON to be restored on next run, as well as an option to restore default settings.

About to add a theme class so I can better manage it, currently it doesn't properly update as the vars are instituted before the settings are applied so it doesn't properly change theme etc without a full restart.

Partway through adding the json play output back in.

8.49pm
basically calling it done for now. Need a break and it's mostly what I wanted it to be.

1.01pm 15/4/26
two things:
1: error on exit which I hadn't found before but happened when mum played it.
    - 'ln 1643, 'NoneType obj has no attr 'startswith' in settings_window
2: make explicit what 'standard' and 'harpoon' modes do/mean.

The error on line 1643 happens if you click the 'x' to close the settings window. I guess I'd never tested it.
Settings really shouldn't have the 'x' anyway, you have to either close it by saving or not-saving. closing by the x makes it unclear what you wanted.

Also, this wasn't reported but I want to make the 'settings' window a stable size whether a subsection is open or not, so it doesn't flicker and expand like it does now. It's just really unpleasant looking when it redraws itself like that.

10.29am 29/4/26
Oops. Stopped updating this apparently.
Farkle is basically done, have just done some minor bugfixes etc since the last update. I did make the settings window stable and fix the above bug.
Today I'm experimenting with animated gifs for the dice.

Huh. Why is
    if not window.is_closed():
        window.close()
    return "exit", None
unreachable? It wasn't in the prior version of the script and I can't see why it's become unreachable now. There are a few minor changes in the above while loop but I can't see how it makes it unreachable...

Oh, it's because there's no 'break' to actually exit that while loop from, only returns. Okay.

3.28pm 30/4/26
working on the animated dice still. Realised I need coloured versions, so am doing that.

Can't see why it isn't finding "still" key in the base64 dict. Will look again tomorrow. Struggling to read the text on screen so maybe time to rest.

11.10am 1/5/26
Okay, figured it out. I was rebuilding the dict each time, and  that was the only entry that had 'anim' and 'still' both. So it was added but immediately overwritten. Should have seen that.

1.15pm
Have the basics sorted. It writes the characters to each applicable frame, and from there I should be able to combine them together into gifs as needed.

Getting the gifs to /play/ is a more difficult thing, but it's a start. And better than having to re-export them wholecloth every time.

Current issue is the outgoings - with no char in the upper section it's just left blank. But I guess that's solved by the x-in y-out. Should work on that now.

Oh, at least for the farkle letters, I can have the numbers transition to blanks, and then to the charcters. Instead of needing 1>f, 2>f, 3>f, etc. All numbers to  blank, and blank to farkle chars. That'd work.

10.18am 2/5/26
Just realised all the farkle letters were 1 pixel off centred. Fixed now.

God that 's' is awful in 'bust'. Needs more... structure.

Reorganised the main 'make contained sequence in single image' section so now it works through the list automatically, so I can feed it any list. Much better than having to specify the outgoing/incoming for each section.


Ooooh. I should just make all the combinations in greyscale then colour them per player. Goddamn why was I not doing that?


3.38pm
working on the automated recolouring now. For some reason blank>letter works, but letter>blank doesn't, will need to check.

Okay fixed it, had the wrong colour assigned on one of the lines.

1.17am
kinda sort of working. Ish. Not very well though. Will work on it again tomorrow.

10.59am 3/5/26
So. I sort of have it working, but it's rough.
The farkle intro bit is the neatest so far, the numbers rolling are glitchy.

For the farkle bit, this is what I have now:

accumImage = sg.tk.PhotoImage(file=chain[char], format=f'gif -index 0')
for i in range(0, frames):
    deltaImage = sg.tk.PhotoImage(file=chain[char], format=f'gif -index {i}')
    accumImage.tk.call(accumImage, 'copy', deltaImage)
    window[farkle_to_no[char]].update(data=accumImage)

If I just try to play deltaImage it is visually tearing, like in the version where I tried to use update_animation.

Also, while they visually light up as held, dice aren't held. Though for some reason it does recognise it if you select all dice as a large straight.

it always prerolls place_1 for player_1.

I need to get default images for each of the characters, because they're all on the wrong frame. Just by one or two but it's a pain. Originally I had the rotation start and end with the good frame but that put a pause in the middle of every multiple-face roll so I removed it. Need to save a still like I originally planned so I can use that at the end of any roll and the opening of the game.

Also, it marks die as 'used' /after/ rolling the others. I want to mark it first, then roll what's left.

Okay, got it to stop prerolling the first die. That's nice.

I want the intro farkle dice to start from blank, I think.

Ohh. Interesting. If I tell it to redo the colours before taking the score, all the non-held dice move on a frame. They were in the right place initially.

So this:
filename=gif_data.player_1_gifs[str(die_inst.value)][0]
is a frame too late

The pause between clicking roll and the roll starting (where it makes the combined gif) isn't too long, but it's present. Going to try just playing those gif segments in sequence instead of combining them.

It is actually playable now, though, with the gifs. Needs a lot of refinement for sure but, it's functioning. Which is nice.

12.52pm 4/5/26
Okay. So -
today I need to sort out getting the frame[0] for each char. Which sholdn't be hard to do, I just can't think, my brain is broken today. But can confirm that the default rotation gifs always start on frame 1, not frame 0. This was intentional, because it avoids having the 'good' frame duplicate mid roll, but means that a die at rest needs a different face, not to just start with the gif. Ending with the gif is fine as it ends on the perfect face.

Also:
Oddly, my 'e to blank' anims start on a blank farkle colour frame. Need to fix that. Oh, and half the other ones - 'blank_to_a' starts on 0, 'blank_to_blank_e' starts on 1. What?

Okay. Yeah, so - nothing uses frame 0 in 'movement' dict in make_dice_images, so the animations should only use 1-11.


Also, the start of the random roll should be 'farkle>number', not just start with number.

Need to be able to determine whether it's currently a farkle graphic or not. Thinking of just allocating the value of '9' to farkle graphic dice, because there's never a value 9 die

Marking places I need to alter with `#CHANGEME:`

I make this:
dice_dict[key_str] = get_die_inst(key_str)
but there's no reason for it, I can just call get_die_inst and it looks it up mostly the same but slightly more reliably.

Okay, finally fixed it so it starts rolling away from the farkle char first, not just harsh swapping out.

Used die are not being properly converted, their colour remains 'held'.

3.00pm
Okay, now a bust rolls into a bust neatly.

3.15pm
Fixed the issue of it not correctly recolouring used dice. Now it quickly rolls them from 'held' to 'used' before rolling the remainder.

next:
After a bust, roll to farkle before rerolling.

Note: rerolling all 6 dice currently starts with 'farkle', when it should start from current val.

TODO: Add roll speed to settings.

After bust, it should't return to 'banked score 0', it should display 'Starting player_x's turn'.

Also when going to a new turn, again it plays the farkle anim from the f start, not the number start. <-- now works for player 1, but computer player now rolls the farkle intro twice.
- more detail on this:
    when busting, it rolls to bust correctly.
 It seems to be running farkle_from_bust and then farkle_from_current.
 -- 5.16pm okay so now it just runs updating and then full farkle. So i need to make full farkle contingent on not-already-farkle.
  -- 5.30pm done.

When rolling to farkle/bust, it uses the player skin whether the die was held or used. Needs to account for die state. <-- DONE

player_2's dice show the wrong value when held. It seems to correct itself when used, but held is wrong. <-- done. Was die_inst instead of inst and using a value from elsewhere.

when pc player rerolls all, still starts from farkle frame.

Oh - 'take' after rerolling all doesn't correctly show the graphics anymore. Oh, found it. Forgot I need to loop the die externally.

player 2 loops all die to 'used' before rerolling all. Unnecessary and visually busy.

??? It just bust and showed all dashes. What?

Oh. Okay, so it goes to bust, but then goes again but makes them all dashes. Why the fuck...

Fixed the above.
player 2 rerolling all still starts from farkle, though. Don't know how to stop that.

Also rerolling all as p1 makesit go from used > player colour without a transition roll. <-- fixed now.

p2 does not update the rolled dice if it's about to bust, so it often looks like they had usable dice as the dice are still showing from the previous throw.

want to add dice skins. Just a layer over the top to give it some wear, or extra shading, etc. also alt die faces.

6.34pm
when p2 rerolls, it still rolls from farkle frames. Need to fix that.

4.56pm 5/5/26
Need to make a new list of what from the 'list' yesterday still applies.
 * Intros do not start on the correct frame but on frame+1. Need stills for all chars except bust.

* rerolling all still has weird animations. Need to put the forced die rolls back in for testing. <- fixed
    - the weirdness specifically: It rolls everything to 'used', then rolls everything to 'usable', then rolls the random die. It should roll to random directly from 'used'.

* starting a new game should roll a fresh farkle animation. So after someone wins and the game starts over, regardless of what die are showing and in what state it should do the full farkle roll. <- done

* button mouseover colour is dark green. Should be something that fits the theme better. Maybe a chestnut for navy and a deep blue for Arcade? <-- done

* clicking 'no' to start a new game after winning makes the window resize in an unpleasant way. <-- fixed, now it just closes.

Have set forced rolls on. Now it's just 1-6 every time.

Select all, they roll to grey, then roll 1-6 again with no transition. Then it rolls /again/, but it busts immediately - now that I can't explain.

Same for player 2?
No, because they didn't reroll, they just took the 1500.

So yeah. It rolls all, rolls all /again/, then busts immediately, despite me having 1500 more points to take if it let me. That's... odd.

Oh, maybe they weren't properly marked as unused?

Oh, it was rerolling twice because I literally had the command in twice, that one's on me.

Hm. Okay so the autobust seems to be... at some point it's being reassigned val of 9, which should only happen after farkling.

Okay, fixed that part. Now it rerolls mostly properly, I just need to change it so it rerolls from the used state to the fresh reroll, like it does when you end turn and it rolls to farkle.
Okay. There's a very brief pause in those rolls which I'm not super keen on.

4.24pm
Okay, fixed. Now it rolls cleanly without that pause, and simply replaces the first roll with a transition roll and then continues with the rest. So the randomness and roll count isn't changed, it just adds a transition if the die was used/held.

Now just going to make those single resting frames.

Should I have it just sit there until you hit 'roll' the first time?

4.45pm
Okay, single frames are made. So, the number frames are to be used if un-held, as the rest of the time it ends on frame 11 correctly. And the farkle frames are to be used on startup. Otherwise the rolling frames are fine.

5.00pm
Okay, much much nicer now. Un-held die stick to the right frame, and the farkle anim starts from frame 11/0, which looks far nicer.
