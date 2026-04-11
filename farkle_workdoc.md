
starting this one a bit late, already made a pretty full-functioned TUI version and am a decent way into the GUI version (though it's not that pretty yet, working on function first).
Started at the start of this month, so it's been a little over a week.

Current issues:

* points from this roll for comp adds turn_score, not the recent roll. <- possibly fixed


* player: if all dice selected, 'reroll' doesn't reroll
    Well no, that's not true: if some of the dice aren't actually viable selections to take the value from, it /does/ reroll what it should. But if all options are viable, it rerolls none (ie if all 6 die can be viably taken and then rerolled)
    Same thing whether they're all rerollable in a single roll or if some are used and others are held.

    It's because I changed
    mark_used(held_dice)
    to
    mark_used(new_used_dice) - the change made it stop holding things it shouldn't (ie if I select '1, 2' and reroll, it would keep the '2' despite it not being a viable selection.) But because it was exclusively marking new dice for some reason it didn't correctly hit the 'if all 6 die are used' mark. Not sure why that'd happen.

    Oh - it's because it only makes /those/ as used, so anything added in the most recent roll won't be re-marked

i wish the npc player's dice value showed up before it rerolls. The timing is just a bit off. Doesn't matter functionally but it's less than ideal.


