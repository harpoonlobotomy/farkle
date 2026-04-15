
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
