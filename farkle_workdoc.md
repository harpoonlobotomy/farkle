
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
